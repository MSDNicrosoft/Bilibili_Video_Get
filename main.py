# -*- coding: UTF-8 -*-
import requests
import re
import json
import subprocess

'''
获取视频链接
'''
print("请输入 BV / AV 号:")
video_id = input()  # 获取 BV / AV 号
request_url = "https://www.bilibili.com/video/" + video_id  # 补充为完整链接

'''
请求网页并输出 Json 文本
'''
headers = {  # 定义 headers
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',   # 定义 User-Agent
    'Referer': request_url  # 定义 Referer
}
html_data = requests.get(request_url,headers=headers).text  # 向 video_url 发送 GET 请求并使用定义的 headers , # 获取 HTML 源代码
video_data = json.loads(re.findall('<script>window\.__playinfo__=(.*?)</script>',html_data)[0])   # 通过正则表达式匹配 , 获取 Json 文本并解析为 Json 格式

'''
获取视频 & 音频二进制文件
'''
video_url = video_data['data']['dash']['video'][0]['backupUrl'][0]  # 获取视频文件链接
audio_url = video_data['data']['dash']['audio'][0]['backupUrl'][0]  # 获取音频文件链接
print("\n正在获取文件, 请稍等...")
video_file = requests.get(video_url,headers=headers).content  # 获取视频二进制文件
audio_file = requests.get(audio_url,headers=headers).content  # 获取音频二进制文件
with open('audio.mp3','wb') as f:
    f.write(audio_file)  # 保存音频文件
with open('video.mp4','wb') as f:
    f.write(video_file)  # 保存视频文件
print("\n正在执行合并操作, 请稍等...")

'''
合并文件为带有音频的视频
'''
merge_file = 'ffmpeg -y -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -strict experimental output.mp4'  # 定义合并命令
subprocess.Popen(merge_file,shell=True)  # 执行合并操作
