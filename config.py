import platform

import requests
import time


def is_window():
    system = platform.system()
    if system == "Windows":
        return True
    else:
        return False

user_id = "14134251"
authorization = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9" \
                ".eyJ1c2VyX2lkIjoxNDEzNDI1MSwiZXhwIjoxNTg3NDUzNjUxLCJpYXQiOjE1ODYyNDQwNTF9" \
                ".J8k70gSEmS9rcqaXIYmUtpQz66yjWTiwCoNmnbCxawY "

root_path = "F:\\人人讲视频" if is_window() else "/Users/yy/Documents/照片/renrenjiang"

head = {
    "Referer": "http://ke.renrenjiang.cn/",
    "Authorization": authorization
}
session = requests.session()
current_milli_time = lambda: int(round(time.time() * 1000))