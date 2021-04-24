# -*- coding: UTF-8 -*-
import os
import sys
import requests
import re
import json

"""
Just only for Windows
"""


"""
定义控制台命令执行函数
需传入参数(命令)
"""
def console_command(command):
    old_stdout = sys.stdout  # 保存默认的 Python 标准输出
    os.system(command)
    sys.stdout = old_stdout  # 恢复 Python 默认的标准输出


"""
配置文件加载
"""
try:
    config = json.load(open(file="config.json"))
except FileNotFoundError:
    print("配置文件未找到!已重新生成!\n\n")
    console_command('curl https://gitee.com/MSDNicrosoft/blogstorge/raw/master/conf/config.json -O')
    print("请重启程序!")
    sys.exit()
except json.decoder.JSONDecodeError:
    print("配置文件格式错误!请检查!\n")
    input("按下回车退出程序")
    sys.exit()
else:
        ffmpeg_config = config['ffmpeg_in_variables']
        download_config = config['uninterrupted']


"""
定义程序整体函数
"""
def file_get():
    """
    获取视频链接
    """
    video_id = input()
    console_command('cls')
    request_url = "https://www.bilibili.com/video/" + video_id

    """
    请求网页
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Referer': request_url
    }
    html_data = requests.get(request_url, headers=headers).text

    try:
        url_data = json.loads(re.findall('<script>window\.__playinfo__=(.*?)</script>', html_data)[0])
    except Exception:  # 定义 BV / AV 号输入错误处理方法
        console_command('cls')
        print("您输入的 BV / AV 号有误!请重新输入：")
        file_get()  # 调用 file_get 函数
    else:
        console_command('title Bilibili Video Get - 获取文件')
        console_command('cls')
        video_url = url_data['data']['dash']['video'][0]['backupUrl'][0]
        audio_url = url_data['data']['dash']['audio'][0]['backupUrl'][0]
        print("正在获取文件, 请稍等...")
        video_file = requests.get(video_url, headers=headers).content
        audio_file = requests.get(audio_url, headers=headers).content

    def done_action():
        console_command('title Bilibili Video Get - 合并完成')
        print(" 合并完成!")
        if download_config == True:
            print("按下回车键以继续爬取其他视频")
            input()
            console_command("cls")
            file_get()
        else:
            print("按下回车键退出程序")
            input()
            sys.exit()

    try:
        with open('audio.mp3', 'wb') as f:
            f.write(audio_file)
        with open('video.mp4', 'wb') as f:
            f.write(video_file)
    except IOError:  # 定义文件无权限写入错误处理方法
        console_command('cls')
        print("文件保存失败!\n请手动删除以下文件：\nvideo.mp4 audio.mp3 output.mp4")
        input("\n按下回车键以关闭程序")
    else:
        console_command('cls')
        print("\n正在执行合并操作, 请稍等...")
        console_command(
            'ffmpeg -y -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -strict experimental output.mp4')
        console_command('cls')
        done_action()


def config_process():
    console_command('title Bilibili Video Get - 运行前环境检查')
    if ffmpeg_config == True:
        console_command('title Bilibili Video Get - 请输入 BV / AV 号')
        print("请输入 BV / AV 号:")
        file_get()
    else:
        print("找不到 ffmpeg.exe!\n请将 ffmpeg.exe 放到此程序同目录下\n\n请重新打开程序\n按下回车键以退出程序")
        input()
        sys.exit()


console_command('title Bilibili Video Get')
config_process()
