<<<<<<< HEAD
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

try:
    # 配置 DeepSeek
    Settings.llm = OpenAI(
        model="deepseek-chat",
        api_key="sk-46094269fdc04188ae91b4d5eb88576e",
        base_url="https://api.deepseek.com/v1"
    )

    # 发送消息
    response = Settings.llm.complete("用一句话介绍一下你自己")
    print("AI回复:", response)
except Exception as e:
=======
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

try:
    # 配置 DeepSeek
    Settings.llm = OpenAI(
        model="deepseek-chat",
        api_key="sk-46094269fdc04188ae91b4d5eb88576e",
        base_url="https://api.deepseek.com/v1"
    )

    # 发送消息
    response = Settings.llm.complete("用一句话介绍一下你自己")
    print("AI回复:", response)
except Exception as e:
>>>>>>> 64ba21b9fe987e2166e7406f7d105dda93aa4f42
    print("报错:", e)