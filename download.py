import json
import os
from m3u8 import m3u8
import util
from config import *


class download:
    def __init__(self, cid):
        self.cid = cid
        self.free_m3u8_url_list = []
        self.is_can_pojie = True
        self.free_videos = []
        self.vip_videos = []

    def _list_video(self):
        """
        列出某个专栏下的所有课程视频
        :param cid: 专栏id
        :return: 视频列表
        """
        video_list = []
        page = 0
        url_format = "https://h5.renrenjiang.cn/api/v2/columns/{0}/activities?u=1052944&activity_sort=ASC&page={1}"
        while True:
            page += 1
            url = url_format.format(self.cid, page)
            res = session.get(url, headers=head)
            res = json.loads(res.content)
            if "activities" in res.keys() and len(res["activities"]) > 0:
                activities = res["activities"]
                for activity in activities:
                    activity_id = activity["id"]
                    title = activity["title"]
                    password = activity["password"]
                    start_at = activity["started_at"]
                    description = activity["creator"]["description"]
                    video_list.append({
                        "id": activity_id,
                        "title": title,
                        "password": password,
                        "start_at": start_at,
                        "description": description
                    })
            else:
                break
        return video_list

    def _get_ts_list(self, index, video):
        """
        获取m3u3文件，并将m3u3中的ts路径解析出来
        :param video: 视频信息
        :return: ts列表
        """
        obj = m3u8(video, index, self.cid)
        hls_url = obj.get_m3u8()
        if hls_url is None:
            return None, None
        res = session.get(hls_url)
        lines = str(res.content).split("\\n")
        ts_list = []
        for i in range(1, len(lines) - 1):
            if lines[i].startswith("#"):
                continue
            ts_list.append(lines[i])
        return hls_url, ts_list

    def _download_by_ts_list(self, video, ts_list, m3u8):
        """
        根据ts文件列表下载视频，并合并
        :param cid: 专栏id
        :param video: 视频信息
        :param ts_list: ts文件列表
        :return: 视频的文件路径
        """
        # 创建专栏文件夹
        path = root_path + os.sep + str(self.cid)
        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)

        # 创建专栏下的视频文件夹
        path = path + os.sep + str(video["id"])
        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)

        # 根据ts列表下载ts文件
        url_format = m3u8[0: m3u8.rfind("/") + 1] + "{0}"
        curr = 0
        for ts in ts_list:
            curr += 1
            filename = path + os.sep + str(curr).zfill(6) + ".ts"
            is_exists = os.path.exists(filename)
            if is_exists:
                continue
            url = url_format.format(ts)
            res = requests.get(url, headers=head)
            if res.status_code != 200:
                print("下载ts文件失败:{0}".format(url))
                continue
            with open(filename, "wb") as file:
                file.write(res.content)
                file.close()
            util.show_process(curr, len(ts_list))

        # 将ts文件列表进行合并为mp4文件，并删除ts文件
        # 如果是在window下
        if util.is_window():
            exec_str = r'copy /b  "' + path + os.sep + r'*.ts" "' + path + os.sep + '{0}.mp4'.format(video["title"])
            os.system(exec_str)  # 使用cmd命令将资源整合
            exec_str = r'del  "' + path + os.sep + r'*.ts"'
            os.system(exec_str)  # 删除原来的文件
        # 如果在linux或者mac下
        else:
            exec_str = "cat {0}*.ts > {1}{2}.mp4".format(path + os.sep, path + os.sep, video["title"])
            os.system(exec_str)  # 使用cat命令将资源整合
            exec_str = "rm -rf {0}*.ts".format(path + os.sep)
            os.system(exec_str)  # 删除原来的文件
        return path + os.sep + '{0}.mp4'.format(video["title"])

    def _is_downloaded(self, column_id, video):
        """
        判断视频是否已下载，防止重复下载
        :param cid: 专栏id
        :param video: 视频信息
        :return: 是否已下载
        """
        path = root_path + os.sep + str(column_id)
        is_exists = os.path.exists(path)
        if not is_exists:
            return False
        path = path + os.sep + str(video["id"])
        is_exists = os.path.exists(path)
        if not is_exists:
            return False
        path = path + os.sep + '{0}.mp4'.format(video["title"])
        is_exists = os.path.exists(path)
        if not is_exists:
            return False
        return True

    def download(self):
        """
        根据专栏id下载整个专栏对视频
        cid的取值范围在[20002, 49999]之间
        :param cid: 专栏id
        :return: 是否成功
        """
        if not self.before_download():
            return
        count = 0
        for video in self.free_videos:
            count += 1
            if self._is_downloaded(self.cid, video):
                print("第{0}个视频已下载:{1}，忽略".format(count, str(video["title"])))
                continue
            m3u8_url, ts_list = self._get_ts_list(count, video)
            while ts_list is None:
                m3u8_url, ts_list = self._get_ts_list(count, video)
            print("下载第{0}个视频:{1}".format(count, str(video["title"])))
            self._download_by_ts_list(video, ts_list, m3u8_url)
        for video in self.vip_videos:
            count += 1
            if self._is_downloaded(self.cid, video):
                print("第{0}个视频已下载:{1}，忽略".format(count, str(video["title"])))
                continue
            if self.is_can_pojie:
                m3u8_url, ts_list = self._get_ts_list(count, video)
                if ts_list is None:
                    print("获取视频{0}的ts列表失败".format(video["title"]))
                    continue
                print("下载第{0}个视频:{1}".format(count, str(video["title"])))
                self._download_by_ts_list(video, ts_list, m3u8_url)
            else:
                print("第{0}个视频收费，且不可破解:{1}，忽略".format(count, str(video["title"])))

    def before_download(self):
        print("正在检查视频是否可以下载或者破解")
        # 列出所有视频，并将其划分为免费和收费
        res = self._list_video()
        if type(res) == dict:
            print("下载专栏{0}失败，原因：{1}".format(self.cid, res))
            exit(1)
        self._divide_videos(res)
        self._get_is_can_pojie()
        if self.is_can_pojie:
            print("专栏{0}下共有{1}的视频，有{2}个可直接下载，有{3}个需要破解".
                  format(self.cid, len(res), len(self.free_videos), len(self.vip_videos)))
            return True
        else:
            if len(self.free_videos) == 0:
                print("专栏{0}下共有{1}的视频，全部都不可以下载或者破解".format(self.cid, len(res)))
                return False
            else:
                print("专栏{0}下共有{1}的视频，有{2}个可下载，其余不可下载和破解".
                      format(self.cid, len(res), len(self.free_videos), len(self.vip_videos)))
                yes_no = input('是否下载部分视频(y|n):')
                if yes_no == "y" or yes_no == "Y":
                    return True
                else:
                    return False

    def _divide_videos(self, videos):
        count = 0
        for video in videos:
            count += 1
            obj = m3u8(video, count, self.cid)
            obj.pay_for_video()
            m3u8_url = obj.get_m3u8_by_pay()
            if m3u8_url is not None:
                self.free_videos.append(video)
                self.free_m3u8_url_list.append(m3u8_url)
            else:
                self.vip_videos.append(video)

    def _get_is_can_pojie(self):
        if len(self.free_m3u8_url_list) == 0:
            self.is_can_pojie = False
        for u in self.free_m3u8_url_list:
            if u.find("videocdn.renrenjiang.cn") < 0:
                self.is_can_pojie = False
