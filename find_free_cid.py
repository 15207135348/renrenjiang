import json
import os
import util
from config import session, head, user_id, current_milli_time, root_path


def list_video(cid):
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
        url = url_format.format(cid, page)
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


def pay_for_video(video):
    """
    购买视频
    :return: 是否成功
    """
    url = "https://api.renrenjiang.cn/api/v3/activities/{0}/reservation".format(video["id"])
    res = session.post(url, headers=head, data={
        "type": "password",
        "password": video["password"],
        "shareId": 0
    })
    res = json.loads(res.content)
    if "result" in res and res["result"] == "ok":
        return True
    else:
        return False


def get_m3u8_by_pay(vid):
    url = "https://api.renrenjiang.cn/api/v3/activities/{0}/stream_url?user_id={1}&timestamp={2}"
    url = url.format(vid, user_id, current_milli_time())
    res = session.get(url, headers=head)
    res = json.loads(res.content)
    if "status" in res.keys() and res["status"] == 2:
        hls_url = res["hls_url"]
        return hls_url
    return None


def write_m3u8_to_file(cid, vid, m3u8_value):
    path = root_path + os.sep + str(cid)
    path = path + os.sep + str(vid)
    path = path + os.sep + "m3u8.txt"
    with open(path, "w") as file:
        file.write(m3u8_value)
        file.close()


def is_m3u8_exist(cid, vid):
    # 创建专栏文件夹
    path = root_path + os.sep + str(cid)
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
    # 创建专栏下的视频文件夹
    path = path + os.sep + str(vid)
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)

    path = path + os.sep + "m3u8.txt"
    is_exists = os.path.exists(path)
    if is_exists:
        return True
    return False


def show(cid):
    videos = list_video(cid)
    if videos is None:
        return False
    m3u8_list = []
    for v in videos:
        pay_for_video(v)
        m3u8 = get_m3u8_by_pay(v["id"])
        if m3u8 is not None:
            m3u8_list.append(m3u8)
    if len(videos) == 0 or len(m3u8_list)== 0:
        return False
    if len(m3u8_list) == len(videos):
        print("专栏{0}下有{1}个视频，其中有{2}个视频是免费的".format(cid, len(videos), len(videos)))
        return True
    for m in m3u8_list:
        if m.find("videocdn.renrenjiang.cn") < 0:
            return False
    print("专栏{0}下有{1}个视频，其中有{2}个视频是免费的，其余是付费的".format(cid, len(videos), len(m3u8_list)))
    return True


if __name__ == '__main__':

    file = open("免费专栏.txt", "r")
    start = 20002
    end = 50000
    for line in file:
        start = int(line)
    file = open("免费专栏.txt", "a")
    for cid in range(start+1, end, 1):
        util.show_process2(cid - 20002, end - 20002)
        if show(cid):
            content = str(cid) + os.linesep
            file.write(content)
            file.flush()
    file.close()

