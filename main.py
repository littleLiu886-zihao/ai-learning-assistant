import os
from dotenv import load_dotenv
import requests
import json
import os

url = "https://api.deepseek.com/chat/completions"

load_dotenv()  # 把 .env 中的变量加载进环境变量
api_key = os.getenv("DEEPSEEK_API_KEY")
print(api_key)
headers = {
    "Authorization":f"Bearer {api_key}"
}
if os.path.exists("deepseek_chat_history.json"):
    with open("deepseek_chat_history.json","r",encoding="utf-8") as f:
        messages =json.load(f)    
else:
    messages = [{
        "role":"system",
        "content": "你是一名AI应用开发学习助手,名叫虾滑不说瞎话。"
    }]        
while True:
    user_input = input("请输入：")

    if user_input == "exit":
        print("退出程序。")
        break

    if user_input == "clear":
        messages=messages[:1]
        with open("deepseek_chat_history.json", "w", encoding="utf-8") as f:
            json.dump(messages,f,ensure_ascii=False,indent=4)
        print("聊天记录已清除。")
        continue    
    messages.append({
        "role": "user",
        "content": user_input
    })
    data = {
    "model": "deepseek-chat",
    "messages": messages
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
       print("Request was successful.")
       result = response.json()
       answer = result["choices"][0]["message"]["content"]
       messages.append({
            "role": "assistant",
            "content": answer   
        })
       print(answer)
       with open("deepseek_chat_history.json","w",encoding="utf-8") as f:
            json.dump(messages,f,ensure_ascii=False,indent=4)
    else:
       print("Request failed with status code:", response.status_code)
       print(response.json()) 