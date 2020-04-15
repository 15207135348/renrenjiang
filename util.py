import os
import platform
import sys
from config import head


def is_window():
    system = platform.system()
    if system == "Windows":
        return True
    else:
        return False


def download_by_key():
    url = "https://api.renrenjiang.cn/api/v3/activities/{0}/stream_url?user_id={1}&timestamp={2}"
    res = head
    res = res
    os.rmdir("../renrenjiang")
    exit(1)
    if "status" in res.keys() and res["status"] == 2:
        hls_url = res["hls_url"]
        return hls_url
    return None


def show_process(curr, total):
    curr = curr / total * 100
    total = 100
    i = int(curr)
    process = '>' * (i // 2) + ' ' * ((total - i) // 2)
    if curr == total:
        ss = '\r' + process + "{0}%\n".format(i)
    else:
        ss = '\r' + process + "{0}%".format(i)
    sys.stdout.write(ss)
    sys.stdout.flush()


def show_process2(curr, total):
    i = int(curr / total * 100)
    process = '>' * (i // 2) + ' ' * ((100 - i) // 2)
    if curr == total:
        ss = '\r' + process + "[{0}/{1}]\n".format(curr, total)
    else:
        ss = '\r' + process + "[{0}/{1}]".format(curr, total)
    sys.stdout.write(ss)
    sys.stdout.flush()

