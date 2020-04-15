import json
import os
import threading
import math
from time import sleep
import util
from config import *


class m3u8:
    def __init__(self, video, index, cid):
        self.index = index
        self.video = video
        self.cid = cid
        self.vid = video["id"]
        self.start_at = int(str(video["start_at"])[0: 6])
        self.min = 0
        self.max = 10000000
        self.thread_num = 400
        self.step = math.floor((self.max - self.min) / self.thread_num)
        self.threads = []
        self.success = False
        self.result = None
        self.lock = threading.Lock()
        self.try_count = 0
        self.total_count = self.max - self.min

    def _func(self, a, b):
        for pos in range(a, b):
            if self.success:
                return None
            self.try_count += 1
            stk_code = str(pos).zfill(7)
            ss = "{0}_{1}{2}".format(self.vid, self.start_at, stk_code)
            url_ff = "http://videocdn.renrenjiang.cn/Act-ss-m3u8-sd/{0}/{1}.m3u8".format(ss, ss)
            try:
                res = session.get(url_ff, headers=head)
                if res.status_code == 200:
                    self.lock.acquire()
                    self.success = True
                    self.lock.release()
                    self.write_m3u8_to_file(url_ff)
                    return url_ff
            except requests.exceptions.ReadTimeout:
                pos -= 1
            except requests.exceptions.ConnectionError:
                pos -= 1
            except ConnectionResetError:
                pos -= 1

    def get_m3u8_by_force(self):
        start = time.time()
        for i in range(self.thread_num):
            t = threading.Thread(target=self._func, args=(self.min + self.step * i, self.min + self.step * (i + 1)))
            self.threads.append(t)
            t.start()
        while True:
            sleep(1)
            util.show_process2(self.try_count, self.total_count)
            for t in self.threads:
                if not t.is_alive():
                    self.threads.remove(t)
            if len(self.threads) == 0:
                break
        end = time.time()
        print("获取到结果:{0} 总共耗时：{1}s".format(self.result, end - start))
        return self.result

    def pay_for_video(self):
        """
        购买视频
        :return: 是否成功
        """
        url = "https://api.renrenjiang.cn/api/v3/activities/{0}/reservation".format(self.vid)
        res = session.post(url, headers=head, data={
            "type": "password",
            "password": self.video["password"],
            "shareId": 0
        })
        res = json.loads(res.content)
        if "result" in res and res["result"] == "ok":
            return True
        else:
            return False

    def get_m3u8_by_pay(self):
        url = "https://api.renrenjiang.cn/api/v3/activities/{0}/stream_url?user_id={1}&timestamp={2}"
        url = url.format(self.vid, user_id, current_milli_time())
        res = session.get(url, headers=head)
        res = json.loads(res.content)
        if "status" in res.keys() and res["status"] == 2:
            hls_url = res["hls_url"]
            return hls_url
        return None

    def is_m3u8_exist(self):
        # 创建专栏文件夹
        path = root_path + os.sep + str(self.cid)
        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)
        # 创建专栏下的视频文件夹
        path = path + os.sep + str(self.vid)
        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)

        path = path + os.sep + "m3u8.txt"
        is_exists = os.path.exists(path)
        if is_exists:
            return True
        return False

    def read_m3u8_from_file(self):
        path = root_path + os.sep + str(self.cid)
        path = path + os.sep + str(self.vid)
        path = path + os.sep + "m3u8.txt"
        with open(path, "r") as file:
            res = file.readline().replace("\n", "").replace("\r\n", "")
            file.close()
            return res

    def write_m3u8_to_file(self, m3u8_value):
        path = root_path + os.sep + str(self.cid)
        path = path + os.sep + str(self.vid)
        path = path + os.sep + "m3u8.txt"
        with open(path, "w") as file:
            file.write(m3u8_value)
            file.close()

    def get_m3u8(self):
        if self.is_m3u8_exist():
            print("第{0}个视频的m3u8已存在，直接下载".format(self.index))
            return self.read_m3u8_from_file()
        if self.pay_for_video():
            print("第{0}个视频购买成功，直接下载".format(self.index))
            hls_url = self.get_m3u8_by_pay()
            self.write_m3u8_to_file(hls_url)
        else:
            print("第{0}个视频购买失败，正在暴力破解...".format(self.index))
            return self.get_m3u8_by_force()
