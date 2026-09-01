import os
import requests

api_key = os.getenv("DEEPSEEK_API_KEY", "")
url = "https://api.deepseek.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("🤖 DeepSeek 聊天机器人（输入 exit 退出）")
print("-" * 40)

while True:
    user_input = input("你: ")
    if user_input.lower() == "exit":
        print("👋 再见！")
        break
    if not user_input.strip():
        print("❌ 请输入内容")
        continue
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": user_input}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        print("AI:", result["choices"][0]["message"]["content"])
    else:
        print("❌ 请求失败:", response.status_code)
    print()