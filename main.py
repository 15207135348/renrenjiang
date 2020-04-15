import download

if __name__ == '__main__':
    cid = input('请输入人人讲的视频专栏的ID(cid): ')
    print("您输入的专栏ID等于:{0}".format(cid))
    obj = download.download(int(cid))
    obj.download()