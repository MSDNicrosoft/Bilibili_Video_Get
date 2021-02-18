# -*- coding: UTF-8 -*-
import os
import sys
import requests
import re
import json

'''
定义程序整体函数
'''
def file_get():

    """
    定义控制台命令执行函数
    需传入参数(命令)
    """
    def console_command(command):
        f_handler = open('out.log', 'w')  # 打开 out.log 文件
        old_stdout = sys.stdout  # 保存默认的 Python 标准输出
        sys.stdout = f_handler  # # 将 Python 标准输出指向 out.log
        os.system(command)  # 使用传入的参数执行命令
        sys.stdout = old_stdout  # 恢复 Python 默认的标准输出

    """
    获取视频链接
    """
    video_id = input()  # 获取 BV / AV 号
    console_command('cls')  # 调用 clean_console 函数并传入参数 cls
    request_url = "https://www.bilibili.com/video/" + video_id  # 补充为完整链接

    """
    请求网页
    """
    headers = {  # 定义 headers
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',  # 定义 User-Agent
        'Referer': request_url  # 定义 Referer
    }
    html_data = requests.get(request_url, headers=headers).text  # 向 video_url 发送 GET 请求并使用定义的 headers 以获取 HTML 源代码

    """
    定义 BV / AV 号输入错误处理方法
    """
    try:
        file_data = json.loads(re.findall('<script>window\.__playinfo__=(.*?)</script>', html_data)[0])  # 通过正则表达式匹配 , 获取 Json 文本并解析为 Json 格式
    except Exception:
        console_command('cls')  # 调用 clean_console 函数并传入参数 cls
        print("您输入的 BV / AV 号有误!请重新输入：")
        file_get()  # 调用 file_get 函数
    else:
        console_command('cls')  # 调用 clean_console 函数并传入参数 cls
        video_url = file_data['data']['dash']['video'][0]['backupUrl'][0]  # 获取视频文件链接
        audio_url = file_data['data']['dash']['audio'][0]['backupUrl'][0]  # 获取音频文件链接
        print("正在获取文件, 请稍等...")
        video_file = requests.get(video_url, headers=headers).content  # 获取视频二进制文件
        audio_file = requests.get(audio_url, headers=headers).content  # 获取音频二进制文件

        """
        定义文件无权限写入处理方法
        """
        try:
            with open('audio.mp3', 'wb') as f:
                f.write(audio_file)  # 保存音频文件
            with open('video.mp4', 'wb') as f:
                f.write(video_file)  # 保存视频文件
        except IOError:
            console_command('cls')  # 调用 clean_console 函数并传入参数 cls
            print("文件保存失败!\n请手动删除以下文件：\nvideo.mp4 audio.mp3 output.mp4")
            console_command('pause')  # 调用 clean_console 函数并传入参数 pause
        else:
            console_command('cls')  # 调用 clean_console 函数并传入参数 cls
            print("\n正在执行合并操作, 请稍等...")
            console_command('ffmpeg -y -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -strict experimental output.mp4')  # clean_console 函数并传入参数 ffmpeg...
            console_command('cls')  # 调用 clean_console 函数并传入参数 cls
            print("已合并完成!")
            console_command('pause')  # 调用 clean_console 函数并传入参数 pause


print("请输入 BV / AV 号:")
file_get()  # 调用 file_get 函数
