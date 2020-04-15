> 人人讲是一款教育类的app，里面有大量的学习视频，包括音乐、书法、服装、瑜伽等等。有一部分视频是免费的，但是大部分是付费的。这里，我们要通过抓包分析人人讲的接口，然后破解和下载这些视频。



**申明：该教程只做学习使用，爬取的视频为人人讲所有，严禁将爬取的视频用来商业化。**



# 1. 人人讲接口分析

首先，使用人人讲APP，选择感兴趣的视频，将视频的链接复制，在电脑上打开（以下面链接作示范）

```html
http://ke.renrenjiang.cn/#/video?activityId=1147066&su=0
```

打开后的样子是这样的

![F580F1F2-5365-43AA-8BF0-AEEAD5CABEE2](/Users/yy/Library/Containers/com.tencent.qq/Data/Library/Application Support/QQ/Users/1365733349/QQ/Temp.db/F580F1F2-5365-43AA-8BF0-AEEAD5CABEE2.png)



我们使用charles抓包工具，看看打开页面时发生了哪些请求

![5A1BD51A-9E33-428C-BFD0-E9C58DD28795](/Users/yy/Library/Containers/com.tencent.qq/Data/Library/Application Support/QQ/Users/1365733349/QQ/Temp.db/5A1BD51A-9E33-428C-BFD0-E9C58DD28795.png)

可以看到，有两个请求，如下所示。

 ```shell
#获取视频的详细信息
https://api.renrenjiang.cn/api/v3/activities/1147066/show?include=creator,columns,service
#获取视频所在专栏下的所有视频的详细信息
https://api.renrenjiang.cn/api/v2/columns/20890/activities
 ```

这里，我们只需要第二个接口，即获取视频专栏，该请求会返回观看视频所需要的密码。

**简要描述：** 

- 获取视频所在专栏下的所有视频的详细信息

**请求URL：** 

- `https://api.renrenjiang.cn/api/v2/columns/20890/activities`

- **请求方式：**

- GET 

**请求header：** 

```js
head = {
    "Referer": "http://ke.renrenjiang.cn/",
    "Authorization": "如下所示，需要根据自己抓包结果来获取认证"
}
```

![A9D8D11D-2316-48E1-9666-D15E9162C47B](/Users/yy/Library/Containers/com.tencent.qq/Data/Library/Application Support/QQ/Users/1365733349/QQ/Temp.db/A9D8D11D-2316-48E1-9666-D15E9162C47B.png)

**参数：** 

| 参数名        | 必选 | 类型   | 说明                       | 示例        |
| :------------ | :--- | :----- | -------------------------- | ----------- |
| u             | 是   | int    | 用户id                     | 1022949     |
| activity_sort | 是   | string | 视频排序方式               | ASC或者DESC |
| page          | 否   | int    | 如果视频很多，需要分页查询 | 1           |

 **返回示例**

``` javascript
{
	"activities": [{
		"id": 1147066,
		"title": "国画技法课——撞水撞粉（第四讲）",
		"status": "结束",
		"video_status": 2,
		"background": "http://image.renrenjiang.cn/uploads/activity/background/1147066/2020_af9598e950780754cdee6956684f9524.jpeg@640w",
		"password": "7939",
		"started_at": 1550883600,
		"charge": true,
		"price": 29.90,
		"reservation_count": 6,
		"reservation": null,
		"user_id": 5011557,
		"creator": {
			"user_id": 5011557,
			"uid": "29269207",
			"nickname": "麦芽老师的艺术课堂",
			"displayname": null,
			"description": "       麦芽老师有着近十年的一线教学经验，所开设课程秉着“艺术美化生活，生活滋养艺术”的课程理念。直播间主要开设课程有儿童趣味水墨画、初级国画、线描、色彩等课程，在这里有专业老师的讲解，课题解答，课后作业辅导。\n      麦芽直播课堂诚邀每一位喜欢画画的朋友一起分享，这里没有年龄界限，只有您对生活、对艺术满满的热爱和期待。老师喜欢与学员交流互动，在轻松愉悦的课堂中，\n感受传统绘画艺术的魅力。\n咨询课程，请扫文末二维码，加微信，老师会耐心解答。麦芽老师的艺术课堂诚邀您随时加入我们！",
			"avatar": "https://image.renrenjiang.cn/uploads/user/avatar_url/5011557/2019_db0d6a4906c039fdc9d9b4b5aea3c880.jpg",
			"background": "https://image.renrenjiang.cn/uploads/user/background/5011557/2019_4f69866d6d9825fc127827cdcfe28098.jpg",
			"channel_name": "无",
			"user_level": 2,
			"proposal_status": 2,
			"fans_count": 26
		},
		"column_id": 20890,
		"column": {
			"column_id": 20890,
			"title": "试听课系列（不定时更新）",
			"price": 20.00,
			"background": "https://image.renrenjiang.cn/uploads/column/background/20890/2019_117d5b509ad52b726bf58089f002dbc4.jpg@640w",
			"activities_count": 5,
			"ctype": 1,
			"max_subscription": 0,
			"subscriptions": 0,
			"activity_allow_buy": true,
			"activity_sort": "DESC"
		},
		"isinvited": false,
		"locked": true,
		"share_url": "https://h5.renrenjiang.cn/#/activity?aid=1147066&su=14134251",
		"description": "课程简介\n本节课衔接上节课程，首先，将花头部分处理完整，莲蓬可以和叶子一起处理。其次，本节课将学习撞水撞粉系列课程荷花叶子的画法，调色调墨技巧，其中将色、墨、水的用法在画面中展现出来。<img src=\"http://image.renrenjiang.cn/uploads/files/2019_0a131051936bd7227843b52a5e8707ab.jpg\"/>本节课适合人群：\n1、零基础国画爱好者；2、少儿美术培训机构教师；3、有绘画基础且能独立上课的小朋友；\n\n如需咨询课程请扫码入群\n<img src=\"http://image.renrenjiang.cn/uploads/files/2019_37d369479071f67b1bd1f2d617431c57.jpg\"/>",
		"popularity": 22,
		"replay": null,
		"reprinted_switch": null,
		"reprint_user_id": null,
		"media_type": null,
		"detail_name": null,
		"detail_nickname": null,
		"rtype": null,
		"wxtype": null,
		"group": null,
		"share_scale": 0.0000,
		"share_amount": 0.00,
		"visible": false,
		"acm_id": null,
		"position": null,
		"task": null,
		"pt_id": null
	},
  ...
  ],
	"total": null
}
```



利用该接口，我们可以从返回结果中得到视频的id、标题、简介和密码（如果没有的话需要暴力破解，后面再来讨论）。

然后，我们输入密码7939，进入观看视频

![89847C9C-0B3A-4A80-B841-B16227F23258](/Users/yy/Library/Containers/com.tencent.qq/Data/Library/Application Support/QQ/Users/1365733349/QQ/Temp.db/89847C9C-0B3A-4A80-B841-B16227F23258.png)



既然可以观看视频了，那么前端必定是获取到了视频的地址了，我们使用Charles抓包分析一下。

![B423478A-5058-4A08-8854-C1DF3795CE05](/Users/yy/Library/Containers/com.tencent.qq/Data/Library/Application Support/QQ/Users/1365733349/QQ/Temp.db/B423478A-5058-4A08-8854-C1DF3795CE05.png)

![FF348789-0E4A-430E-A361-D00A3ECB105A](/Users/yy/Library/Containers/com.tencent.qq/Data/Library/Application Support/QQ/Users/1365733349/QQ/Temp.db/FF348789-0E4A-430E-A361-D00A3ECB105A.png)

![4795F06E-1612-4935-A850-E1837886D9E0](/Users/yy/Library/Containers/com.tencent.qq/Data/Library/Application Support/QQ/Users/1365733349/QQ/Temp.db/4795F06E-1612-4935-A850-E1837886D9E0.png)

![854ED36F-BC92-4181-8986-A59E1B3871FC](/Users/yy/Library/Containers/com.tencent.qq/Data/Library/Application Support/QQ/Users/1365733349/QQ/Temp.db/854ED36F-BC92-4181-8986-A59E1B3871FC.png)

可以看到，从输入密码到获取视频，总共需要4个接口，如下所示。

```
#验证密码是否正确
https://api.renrenjiang.cn/api/v3/activities/1147066/reservation
#获取视频的m3u8地址
https://api.renrenjiang.cn/api/v3/activities/1147066/stream_url?user_id=14264889&timestamp=1586920041105
#获取m3u8文件
http://video.renrenjiang.cn/record/alilive/2726981393-1550845168.m3u8
#根据m3u8文件，获取一段一段的小视频
http://video.renrenjiang.cn/record/alilive/2726981393/1550841839_1.ts
```

这里，我就不把每个接口的请求参数和返回数据写出来啦，