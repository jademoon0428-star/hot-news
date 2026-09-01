import requests
import json
import os
from datetime import datetime
import time
import xml.etree.ElementTree as ET

# ========== 配置 ==========
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
OUTPUT_DIR = "每日热点简报"

# ========== 分类函数 ==========
def classify_event(title):
    keywords = {
        "国家大事": ["中国", "国家", "外交", "峰会", "主席", "总理", "国务院", "中央", "国际", "联合国", "习近平", "李克强"],
        "政策变化": ["政策", "发改委", "财政部", "央行", "监管", "法规", "条例", "通知", "意见", "改革"],
        "科技": ["AI", "人工智能", "芯片", "量子", "航天", "卫星", "互联网", "5G", "算法", "模型", "OpenAI", "华为", "腾讯"],
        "重大灾害": ["地震", "洪水", "台风", "暴雨", "山洪", "火灾", "事故", "救援", "应急"],
        "娱乐八卦": ["明星", "演员", "歌手", "电影", "综艺", "结婚", "离婚", "官宣", "粉丝", "八卦"],
        "体育": ["世界杯", "NBA", "CBA", "中超", "足球", "篮球", "决赛", "冠军", "晋级", "奥运"],
        "商业财经": ["油价", "股市", "基金", "投资", "融资", "上市", "财报", "营收", "并购", "港股", "美股"],
        "重要人物": ["主席", "总统", "首相", "总理", "CEO", "创始人", "董事长", "院士"],
        "民生教育": ["民生", "教育", "就业", "医保", "养老", "物价", "消费", "学生", "减负", "高考"]
    }
    for category, words in keywords.items():
        for word in words:
            if word in title:
                return category
    return "综合新闻"

# ========== 采集真实新闻（国内可访问） ==========
def fetch_real_news():
    events = []
    
    # 使用国内可访问的RSS源
    rss_sources = [
        {"name": "科技", "url": "https://rsshub.app/36kr/news"},
        {"name": "科技", "url": "https://rsshub.app/ithome"},
        {"name": "科技", "url": "https://rsshub.app/sspai"},
        {"name": "商业", "url": "https://rsshub.app/jisilu"},
        {"name": "娱乐", "url": "https://rsshub.app/douban/realtime"},
        {"name": "体育", "url": "https://rsshub.app/dongqiudi/hot"},
    ]
    
    for source in rss_sources:
        try:
            response = requests.get(source['url'], timeout=8)
            if response.status_code == 200:
                try:
                    root = ET.fromstring(response.content)
                    items = root.findall('.//item')
                    count = 0
                    for item in items[:3]:
                        title_elem = item.find('title')
                        if title_elem is not None:
                            title = title_elem.text
                            if title and len(title) > 10 and 'http' not in title[:10]:
                                title = title.replace('[36氪]', '').replace('36氪', '').strip()
                                if len(title) > 8:
                                    events.append({
                                        'title': title,
                                        'category': source['name'],
                                        'source': 'RSS',
                                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
                                    })
                                    count += 1
                    if count > 0:
                        print(f"  ✅ {source['name']}: {count}条")
                except:
                    print(f"  ⚠️ {source['name']}: 解析失败")
        except Exception as e:
            pass
    
    # 如果获取不到，使用内置热点
    if len(events) < 5:
        print("  📋 使用内置热点数据...")
        builtin = [
            ("中国成功发射卫星互联网试验卫星", "国家大事"),
            ("发改委发布新政策支持民营经济", "政策变化"),
            ("OpenAI发布新一代多模态AI模型", "科技"),
            ("某地发生地震救援正在进行", "重大灾害"),
            ("顶流明星官宣结婚", "娱乐八卦"),
            ("中国男足晋级世界杯", "体育"),
            ("教育部发布减负新政策", "民生教育"),
            ("中国科学家量子计算突破", "科技"),
            ("国际油价大幅波动", "商业财经"),
            ("某国领导人宣布访华", "重要人物"),
        ]
        for title, cat in builtin:
            if not any(e['title'] == title for e in events):
                events.append({
                    'title': title,
                    'category': cat,
                    'source': '内置',
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
                })
    
    return events

# ========== 采集所有热点 ==========
def fetch_all_hot_events():
    print("  📡 获取新闻...")
    events = fetch_real_news()
    print(f"\n✅ 共 {len(events)} 条")
    return events

# ========== 调用DeepSeek ==========
def call_deepseek(prompt):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"❌ API失败: {response.status_code}"
    except Exception as e:
        return f"❌ 请求失败: {e}"

# ========== 生成文章 ==========
def generate_article(event):
    style_map = {
        "国家大事": "严肃客观的新闻报道风格",
        "政策变化": "深度解读风格",
        "科技": "前瞻性技术报道风格",
        "重大灾害": "人文关怀风格",
        "娱乐八卦": "轻松有趣的娱乐报道风格",
        "体育": "激情专业的体育报道风格",
        "商业财经": "专业客观的财经报道风格",
        "民生教育": "贴近生活的报道风格"
    }
    style = style_map.get(event['category'], "客观中立")
    
    prompt = f"""
根据以下热点事件，写一篇200-300字的新闻短文，Markdown格式。

标题：{event['title']}
分类：{event['category']}
风格：{style}

要求：
1. # 一级标题（要吸引人，不要照抄原标题）
2. 💡 提炼2个核心要点
3. 正文2-3段，每段60-80字
4. 插入 [图片：配图建议]
5. 结尾用 # 添加3个标签

直接输出Markdown内容。
"""
    return call_deepseek(prompt)

# ========== 保存 ==========
def save_article(event, content):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    safe = event['title'][:10].replace('/', '_').replace('\\', '_')
    path = os.path.join(OUTPUT_DIR, f"{today}_{event['category']}_{safe}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

# ========== 生成索引 ==========
def generate_index(articles):
    today = datetime.now().strftime("%Y年%m月%d日")
    idx = f"# 📰 每日热点简报 - {today}\n\n共 {len(articles)} 条热点\n\n"
    categories = {}
    for info in articles:
        cat = info.get('category', '其他')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(info)
    for cat, items in categories.items():
        idx += f"## 📌 {cat}\n"
        for item in items:
            idx += f"- [{item['title']}]({item['file']})\n"
        idx += "\n"
    path = os.path.join(OUTPUT_DIR, f"INDEX_{datetime.now().strftime('%Y%m%d')}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(idx)
    return path

# ========== 主程序 ==========
def main():
    print("=" * 50)
    print("📰 每日热点内容工厂 v3.0")
    print("=" * 50)
    events = fetch_all_hot_events()
    
    if not events:
        print("❌ 未获取到热点")
        return
    
    print("\n📋 热点列表:")
    for i, e in enumerate(events, 1):
        print(f"  {i}. [{e['category']}] {e['title'][:40]}...")
    
    print("\n✍️ 生成文章中...")
    articles = []
    for i, e in enumerate(events, 1):
        print(f"  [{i}/{len(events)}] {e['title'][:25]}...")
        content = generate_article(e)
        path = save_article(e, content)
        articles.append({'title': e['title'], 'file': path, 'category': e['category']})
        time.sleep(0.5)
    
    idx = generate_index(articles)
    print(f"\n✅ 完成！共 {len(articles)} 篇文章")
    print(f"📁 {os.path.abspath(OUTPUT_DIR)}")
    print(f"📋 索引: {idx}")

if __name__ == "__main__":
    main()