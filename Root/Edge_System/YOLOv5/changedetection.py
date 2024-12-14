import os
import cv2
import pathlib
import requests
from datetime import datetime

class ChangeDetection:
    result_prev = []
    HOST = 'https://button.pythonanywhere.com'
    username = 'button'
    password = 'shenxuan0206'
    token = ''
    title = ''
    text = ''
    def __init__(self, names):

        self.result_prev = [0 for _ in range(len(names))]
        res = requests.post(self.HOST + '/api-token-auth/', {
            'username': self.username,
            'password': self.password,
        })
        res.raise_for_status()
        self.token = res.json()['token']  
        print(self.token)
    def add(self, names, detected_current, save_dir, image):
        self.title = "" 
        self.text = ""   
        change_flag = 0  
        i = 0            
        while i < len(self.result_prev):
            if self.result_prev[i] == 0 and detected_current[i] == 1:
                change_flag = 1 
                self.title = names[i] 
                self.text += names[i] + ", " 
            i += 1  
        self.result_prev = detected_current[:]

        if change_flag == 1:
            self.send(save_dir, image) 

    def send(self, save_dir, image):
        now = datetime.now()

        save_path = os.path.join(
            save_dir,
            'detected',
            str(now.year),
            str(now.month),
            str(now.day)
        )
        pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)

        full_path = os.path.join(
            save_path,
            f"{now.hour}-{now.minute}-{now.second}-{now.microsecond}.jpg"
        )

        dst = cv2.resize(image, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        cv2.imwrite(full_path, dst)
        print(f"Saved resized image to: {full_path}")

        headers = {
            'Authorization': f'JWT {self.token}',
            'Accept': 'application/json',
        }

        data = {
            'title': self.title,
            'text': self.text,
            'author': '1',
            'created_date': now.isoformat(),
            'published_date': now.isoformat(),
        }

        try:
            with open(full_path, 'rb') as file:
                files = {'image': ('filename.jpg', file, 'image/jpeg')}
                print("POST URL:", self.HOST + '/api_root/Post/')
                print("POST Headers:", headers)
                print("POST Data:", data)
                print("POST Files:", full_path)

                res = requests.post(
                    url=self.HOST + '/api_root/Post/',
                    data=data,
                    files=files,
                    headers=headers
                )

                print("Response Status Code:", res.status_code)
                print("Response Content:", res.content)
                res.raise_for_status()  # 如果发生 HTTP 错误，抛出异常

                print("Successfully sent detection result to server!")
        except Exception as e:
            print("Failed to send detection result:", str(e))
