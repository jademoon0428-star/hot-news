import requests
import json
import os
import re
from datetime import datetime
import time
import hashlib
from bs4 import BeautifulSoup

# ========== 配置 ==========
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
OUTPUT_DIR = "每日热点简报"

# ========== 清理文件名 ==========
def clean_filename(text):
    text = text.replace('\n', '').replace('\r', '').replace('\t', '')
    illegal_chars = r'[<>:"/\\|?*]'
    text = re.sub(illegal_chars, '', text)
    if len(text) > 30:
        text = text[:30]
    return text.strip() or "未命名"

# ========== 分类函数 ==========
def classify_event(title):
    keywords = {
        "国家大事": ["中国", "国家", "外交", "峰会", "主席", "总理", "国务院", "中央", "国际", "联合国"],
        "政策变化": ["政策", "发改委", "财政部", "央行", "监管", "法规", "条例", "通知", "意见", "改革"],
        "科技": ["AI", "人工智能", "芯片", "量子", "航天", "卫星", "互联网", "5G", "算法", "模型", "华为", "腾讯", "阿里"],
        "重大灾害": ["地震", "洪水", "台风", "暴雨", "山洪", "火灾", "事故", "救援", "应急"],
        "娱乐八卦": ["明星", "演员", "歌手", "电影", "综艺", "结婚", "离婚", "官宣", "粉丝"],
        "体育": ["世界杯", "NBA", "CBA", "足球", "篮球", "决赛", "冠军", "晋级"],
        "商业财经": ["油价", "股市", "基金", "投资", "融资", "上市", "财报", "营收", "并购"],
        "重要人物": ["主席", "总统", "首相", "总理", "CEO", "创始人"],
        "民生教育": ["民生", "教育", "就业", "医保", "养老", "物价", "消费", "学生", "减负"]
    }
    for category, words in keywords.items():
        for word in words:
            if word in title:
                return category
    return "综合新闻"

# ========== 1. 新浪新闻热榜 ==========
def fetch_sina_hot():
    events = []
    try:
        print("  📡 新浪新闻热榜...")
        url = "https://news.sina.com.cn/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            titles = []
            for tag in soup.find_all(['h1', 'h2', 'h3']):
                link = tag.find('a')
                if link:
                    title = link.get_text().strip()
                    if title and 10 < len(title) < 80 and '专题' not in title:
                        titles.append(title)
            seen = set()
            for title in titles:
                key = title[:20]
                if key not in seen:
                    seen.add(key)
                    events.append({
                        'title': title,
                        'category': classify_event(title),
                        'source': '新浪热榜',
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
            if events:
                print(f"  ✅ 新浪热榜: {len(events)}条")
    except Exception as e:
        print(f"  ❌ 新浪热榜: {str(e)[:30]}")
    return events

# ========== 2. 腾讯新闻热榜 ==========
def fetch_tencent_hot():
    events = []
    try:
        print("  📡 腾讯新闻热榜...")
        url = "https://news.qq.com/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            titles = []
            for tag in soup.find_all(['h1', 'h2', 'h3', 'h4']):
                link = tag.find('a')
                if link:
                    title = link.get_text().strip()
                    if title and 10 < len(title) < 60:
                        if '广告' not in title and '专题' not in title:
                            titles.append(title)
            seen = set()
            for title in titles:
                key = title[:20]
                if key not in seen:
                    seen.add(key)
                    events.append({
                        'title': title,
                        'category': classify_event(title),
                        'source': '腾讯热榜',
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
            if events:
                print(f"  ✅ 腾讯热榜: {len(events)}条")
    except Exception as e:
        print(f"  ❌ 腾讯热榜: {str(e)[:30]}")
    return events

# ========== 3. 今日头条热榜 ==========
def fetch_toutiao_hot():
    events = []
    try:
        print("  📡 今日头条热榜...")
        url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.toutiao.com/"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            items = data.get('data', [])
            for item in items[:15]:
                title = item.get('Title', '') or item.get('title', '')
                if title and len(title) > 5:
                    events.append({
                        'title': title,
                        'category': classify_event(title),
                        'source': '今日头条',
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
            if events:
                print(f"  ✅ 今日头条热榜: {len(events)}条")
    except Exception as e:
        print(f"  ❌ 今日头条热榜: {str(e)[:30]}")
    return events

# ========== 4. 百度热榜 ==========
def fetch_baidu_hot():
    events = []
    try:
        print("  📡 百度热榜...")
        url = "https://top.baidu.com/board?tab=realtime"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            titles = []
            for item in soup.find_all('a', class_=re.compile(r'title|list|item')):
                title = item.get_text().strip()
                if title and 8 < len(title) < 60:
                    titles.append(title)
            for tag in soup.find_all(['h1', 'h2', 'h3']):
                link = tag.find('a')
                if link:
                    title = link.get_text().strip()
                    if title and 8 < len(title) < 60:
                        titles.append(title)
            seen = set()
            for title in titles:
                key = title[:20]
                if key not in seen:
                    seen.add(key)
                    events.append({
                        'title': title,
                        'category': classify_event(title),
                        'source': '百度热榜',
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
            if events:
                print(f"  ✅ 百度热榜: {len(events)}条")
    except Exception as e:
        print(f"  ❌ 百度热榜: {str(e)[:30]}")
    return events

# ========== 5. 网易新闻热榜 ==========
def fetch_163_hot():
    events = []
    try:
        print("  📡 网易新闻热榜...")
        url = "https://news.163.com/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            titles = []
            for tag in soup.find_all(['h1', 'h2', 'h3', 'h4']):
                link = tag.find('a')
                if link:
                    title = link.get_text().strip()
                    if title and 10 < len(title) < 80:
                        if '专题' not in title and '广告' not in title:
                            titles.append(title)
            seen = set()
            for title in titles:
                key = title[:20]
                if key not in seen:
                    seen.add(key)
                    events.append({
                        'title': title,
                        'category': classify_event(title),
                        'source': '网易热榜',
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
            if events:
                print(f"  ✅ 网易热榜: {len(events)}条")
    except Exception as e:
        print(f"  ❌ 网易热榜: {str(e)[:30]}")
    return events

# ========== 6. 备用聚合API ==========
def fetch_hot_api():
    events = []
    try:
        print("  📡 热点聚合API...")
        response = requests.get("https://api.03c3.cn/api/hot", timeout=8)
        if response.status_code == 200:
            data = response.json()
            for item in data.get('data', [])[:10]:
                title = item.get('title', '')
                if title and len(title) > 5:
                    events.append({
                        'title': title,
                        'category': classify_event(title),
                        'source': '热点聚合',
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
            if events:
                print(f"  ✅ 热点聚合API: {len(events)}条")
    except:
        pass
    return events

# ========== 采集所有热点 ==========
def fetch_all_hot_events():
    all_events = []
    print("  📡 多平台热榜抓取...")
    print()
    fetchers = [
        fetch_sina_hot,
        fetch_tencent_hot,
        fetch_toutiao_hot,
        fetch_baidu_hot,
        fetch_163_hot,
        fetch_hot_api
    ]
    for fetcher in fetchers:
        events = fetcher()
        all_events.extend(events)
        time.sleep(0.5)
    unique = []
    seen = set()
    for e in all_events:
        key = e['title'][:15]
        if key not in seen:
            seen.add(key)
            unique.append(e)
    print(f"\n✅ 共获取 {len(unique)} 条热点")
    return unique

# ========== 调用DeepSeek ==========
def call_deepseek(prompt):
    if not DEEPSEEK_API_KEY:
        return "❌ 错误：未设置 DEEPSEEK_API_KEY"
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"❌ API失败: {response.status_code}"
    except Exception as e:
        return f"❌ 请求失败: {e}"

# ========== 生成文章 ==========
def generate_article(event):
    style_map = {"国家大事": "严肃客观", "政策变化": "深度解读", "科技": "前瞻技术", 
                 "重大灾害": "人文关怀", "娱乐八卦": "轻松有趣", "体育": "激情专业",
                 "商业财经": "专业客观", "民生教育": "贴近生活"}
    style = style_map.get(event['category'], "客观中立")
    prompt = f"""
根据以下热点，写一篇200-300字的短文，Markdown格式。
标题：{event['title']}
分类：{event['category']}
风格：{style}
要求：
1. # 一级标题
2. 💡 提炼2个要点
3. 正文2-3段
4. 插入 [图片：配图建议]
5. 结尾 # 3个标签
直接输出Markdown。
"""
    return call_deepseek(prompt)

# ========== 保存 ==========
def save_article(event, content):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    safe_title = clean_filename(event['title'])
    path = os.path.join(OUTPUT_DIR, f"{today}_{event['category']}_{safe_title}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

# ========== 生成索引 ==========
def generate_index(articles):
    today = datetime.now().strftime("%Y年%m月%d日")
    idx = f"# 📰 每日热点简报 - {today}\n\n共 {len(articles)} 条\n\n"
    cats = {}
    for info in articles:
        cat = info.get('category', '其他')
        cats.setdefault(cat, []).append(info)
    for cat, items in cats.items():
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
    print("=" * 55)
    print("📰 每日热点内容工厂 v7.0（多平台热榜版）")
    print("   支持：新浪、腾讯、今日头条、百度、网易")
    print("=" * 55)
    events = fetch_all_hot_events()
    if not events:
        print("❌ 未获取到任何热点")
        return
    
    # ====== 限制生成数量：只取前20条 ======
    events = events[:20]
    
    print("\n📋 热点列表（将生成以下20条）:")
    for i, e in enumerate(events, 1):
        src = e.get('source', '未知')
        print(f"  {i}. [{e['category']}] {e['title'][:50]}... ({src})")
    
    print("\n✍️ 生成文章中...")
    articles = []
    for i, e in enumerate(events, 1):
        print(f"  [{i}/{len(events)}] {e['title'][:25]}...")
        content = generate_article(e)
        path = save_article(e, content)
        articles.append({'title': e['title'], 'file': path, 'category': e['category']})
        time.sleep(0.3)
    
    idx = generate_index(articles)
    print(f"\n✅ 完成！共 {len(articles)} 篇文章")
    print(f"📁 {os.path.abspath(OUTPUT_DIR)}")
    print(f"📋 索引: {idx}")

if __name__ == "__main__":
    main()