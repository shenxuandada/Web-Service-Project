import requests
from datetime import datetime

API_URL = "https://button.pythonanywhere.com//api_root/Post/"
JWT_TOKEN = "www"

detected_hour = datetime.now().replace(minute=0, second=0, microsecond=0).isoformat()
data = {
   "title": "Example Title", 
    "text": "Example text content", 
    "author": 1, 
    "detected_hour": detected_hour,
    "count": 10
}

headers = {
    "Authorization": f"JWT {JWT_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.post(API_URL, json=data, headers=headers)
if response.status_code == 200:
    try:
        print(response.json())  
    except ValueError:  
        print("JSON 解析错误")
else:
    print(f"错误状态码: {response.status_code}")
    print("响应内容:", response.text)
