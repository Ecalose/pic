# Pixiv_crawler

###### 须在全程保持网络稳定！尤其是处于中国大陆的用户！请特别注意！
###### Must maintain network stability in the whole process! Especially in Chinese mainland users! Please pay special attention!

My English is poor, you can use Google translation XDD

这是我第一次在Github上上传项目 欢迎纠正错误！

## 关于cofing.json

# Ranklist_Maxpage
它的值应是一个数组，如果该数组的第0个元素的值为 ALL 则下载所有数据
如果想自定义下载的页数，则从左到右分别为: Daily Daily_r18 Weekly Weekly_r18 R18g Monthly Rookie Male Male_r18 Female Female_r18
如果超过限定的页数则会取最大值 所以不必担心会出问题

# User-Agent
顾名思义 这个是每次访问时使用的 User-Agent 可自行获取
这个的值同样为一个数组 如果数组内有多个值 则会在每次请求时随机获取一个 User-Agent

# Cookie
这个是你的访问 cookie ，每个人的访问 cookie 可自行获取
具体获取方式如下:
进入 https://www.pixiv.net/rank.php
按下键盘上 F12 键
点击Network选项
接着将页面滑到最底端 等待刷新
就可以在Network选项卡中找到向 https://www.pixiv.net/ranking.php?&format=json&p=2 发送的Get请求
在这个请求的请求头中找到 "Cookie"
将其值复制进 Cookie 的值中

# Download-Path
下载图片的路径 会自动创建各个列表的文件夹
