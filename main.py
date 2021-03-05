# -*- coding: UTF-8 -*-
import os
import sys
import requests
import re
import json


"""
定义控制台命令执行函数
需传入参数(命令)
"""
def console_command(command):
    f_handler = open('temp.log', 'w')  # 打开 temp.log 文件
    old_stdout = sys.stdout  # 保存默认的 Python 标准输出
    sys.stdout = f_handler  # # 将 Python 标准输出指向 out.log
    os.system(command)  # 使用传入的参数执行命令
    sys.stdout = old_stdout  # 恢复 Python 默认的标准输出


"""
定义程序整体函数
"""
def file_get():
    """
    获取视频链接
    """
    video_id = input()  # 获取 BV / AV 号
    console_command('cls')  # 调用 console_command 函数并传入参数 cls
    request_url = "https://www.bilibili.com/video/" + video_id  # 补充为完整链接

    """
    请求网页
    """
    headers = {  # 定义 headers
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',  # 定义 User-Agent
        'Referer': request_url  # 定义 Referer
    }
    html_data = requests.get(request_url, headers=headers).text  # 向 request_url 发送 GET 请求并使用定义的 headers 以获取 HTML 源代码

    try:
        url_data = json.loads(re.findall('<script>window\.__playinfo__=(.*?)</script>', html_data)[0])  # 通过正则表达式匹配 , 获取 Json 文本并解析为 Json 格式
    except Exception:  # 定义 BV / AV 号输入错误处理方法
        console_command('cls')  # 调用 console_command 函数并传入参数 cls
        print("您输入的 BV / AV 号有误!请重新输入：")
        file_get()  # 调用 file_get 函数
    else:
        console_command('title Bilibili Video Get - 获取文件')
        console_command('cls')  # 调用 console_command 函数并传入参数 cls
        video_url = url_data['data']['dash']['video'][0]['backupUrl'][0]  # 获取视频文件链接
        audio_url = url_data['data']['dash']['audio'][0]['backupUrl'][0]  # 获取音频文件链接
        print("正在获取文件, 请稍等...")
        video_file = requests.get(video_url, headers=headers).content  # 获取视频二进制文件
        audio_file = requests.get(audio_url, headers=headers).content  # 获取音频二进制文件

    def select_action():  # 定义 select_action 函数
        console_command('title Bilibili Video Get - 合并完成')  # 调用 console_command 函数并传入参数 title...
        print(" 合并完成!\n\n是否还要继续获取其他视频?\n输入 1 并回车以继续获取其他视频\n输入 2 并回车以退出程序")
        sec_info = input()
        if sec_info == '1':
            console_command('cls')  # 调用 console_command 函数并传入参数 cls
            console_command('title Bilibili Video Get - 请输入 BV / AV 号')  # 调用 console_command 函数并传入参数 title...
            print("请输入 BV / AV 号:")
            file_get()  # 调用 file_get 函数
        if sec_info == '2':
            sys.exit()  # 退出程序
        else:
            console_command('cls')
            print("您输入的选项有误!请重新输入：")
            select_action()  # 调用 select_action 函数

    try:
        with open('audio.mp3', 'wb') as f:
            f.write(audio_file)  # 保存音频文件
        with open('video.mp4', 'wb') as f:
            f.write(video_file)  # 保存视频文件
    except IOError:  # 定义文件无权限写入错误处理方法
        console_command('cls')  # 调用 console_command 函数并传入参数 cls
        print("文件保存失败!\n请手动删除以下文件：\nvideo.mp4 audio.mp3 output.mp4")
        input("\n按下回车键以关闭程序")
    else:
        console_command('cls')  # 调用 console_command 函数并传入参数 cls
        print("\n正在执行合并操作, 请稍等...")
        console_command('ffmpeg -y -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -strict experimental output.mp4')  # 调用 console_command 函数并传入参数 ffmpeg.exe
        console_command('cls')  # 调用 console_command 函数并传入参数 cls
        select_action()  # 调用 select_action 函数


def prepare_check():
    console_command('title Bilibili Video Get - 运行前环境检查')
    print("请确认您已将 ffmpeg.exe 放到此程序同目录下或添加到系统环境变量中!\n\n输入 1 并回车以确认在系统环境变量中\n输入 2 并回车以确认在此程序同目录下")
    check_select = input()
    if check_select == '1':
        console_command('cls')  # 调用 console_command 函数并传入参数 cls
        console_command('title Bilibili Video Get - 请输入 BV / AV 号')  # 调用 console_command 函数并传入参数 title...
        print("请输入 BV / AV 号:")
        file_get()  # 调用 file_get 函数
    if check_select == '2':
        ffmpeg_info = os.path.isfile("ffmpeg.exe")  # 判断 ffmpeg.exe 是否存在
        if ffmpeg_info:  # 如果存在
            print("请输入 BV / AV 号:")
            file_get()  # 调用 file_get 函数
        if not ffmpeg_info:  # 如果不存在
            console_command('cls')  # 调用 console_command 函数并传入参数 cls
            print("找不到 ffmpeg.exe!\n请下载 FFmpeg 并将 ffmpeg.exe 放到此程序同目录下")
            input("\n按下回车键以重载程序")
            console_command('cls')  # 调用 console_command 函数并传入参数 cls
            prepare_check()  # 调用 prepare_check 函数
    else:
        print("你输入的选项有误!请重新输入：")
        prepare_check()  # 调用 prepare_check 函数


console_command('title Bilibili Video Get')  # 调用 console_command 函数并传入参数 title...
prepare_check()  # 调用 prepare_check 函数
