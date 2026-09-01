import requests
import json

def get_hot_events():
    """获取今日热点事件"""
    apis = [
        "https://api.03c3.cn/api/hot",
        "https://api.vvhan.com/api/hotlist",
        "https://api.qiqi1.cn/api/hot"
    ]
    
    for url in apis:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                events = []
                if 'data' in data and isinstance(data['data'], list):
                    for i, item in enumerate(data['data'][:10], 1):
                        title = item.get('title', '') or item.get('name', '') or str(item)
                        events.append(f"{i}. {title}")
                    return events
                elif 'list' in data and isinstance(data['list'], list):
                    for i, item in enumerate(data['list'][:10], 1):
                        title = item.get('title', '') or item.get('name', '') or str(item)
                        events.append(f"{i}. {title}")
                    return events
        except:
            continue
    
    # 备用示例数据
    mock_data = [
        "人工智能技术取得重大突破",
        "国际油价大幅波动",
        "新能源汽车销量创新高",
        "AI 助手成为日常生活新标配",
        "全球气候变暖引发各国关注",
        "科技巨头发布最新旗舰产品",
        "体育赛事精彩瞬间回顾",
        "新政策出台影响多个行业",
        "社交媒体平台推出新功能",
        "文化展览活动受市民欢迎"
    ]
    return [f"{i+1}. {item}" for i, item in enumerate(mock_data)]


def call_deepseek(prompt):
    """调用 DeepSeek API"""
    api_key = "sk-46094269fdc04188ae91b4d5eb88576e"
    url = "https://api.deepseek.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"❌ API 调用失败: {response.status_code}"
    except Exception as e:
        return f"❌ 请求失败: {e}"


def generate_article(events):
    """用 AI 生成图文并茂的文章"""
    events_text = "\n".join(events)
    prompt = f"""
请根据以下今日热点事件列表，写一篇 400-600 字的新闻简报，要求输出为 Markdown 格式。

输出格式要求：
1. 标题：用 # 一级标题
2. 开头引言：用一段话总结今日热点趋势
3. 正文：每条热点用 ## 二级标题 + 一段描述（150字左右）
4. 结尾：用 ### 结尾总结
5. 适当使用emoji增加可读性（如 🔥 📊 💡 🏆）
6. 在适当位置插入 [图片] 占位符，标注建议配图内容

今日热点事件：
{events_text}

直接输出 Markdown 内容，不要加任何额外说明。
"""
    
    print("✍️ AI 正在创作文章...")
    article = call_deepseek(prompt)
    return article


def save_article(article):
    """保存文章到文件"""
    from datetime import datetime
    today = datetime.now().strftime("%Y%m%d")
    filename = f"每日热点简报_{today}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(article)
    
    print(f"✅ 文章已保存到: {filename}")
    return filename


if __name__ == "__main__":
    print("📰 正在获取今日热点...")
    print("=" * 50)
    
    events = get_hot_events()
    
    if events:
        print("\n🔥 今日热点 TOP 10:")
        print("=" * 50)
        for event in events:
            print(event)
        print("=" * 50)
        
        article = generate_article(events)
        
        print("\n📝 AI 生成的文章:")
        print("=" * 50)
        print(article)
        print("=" * 50)
        
        save_article(article)
    else:
        print("⚠️ 未能获取到热点数据")