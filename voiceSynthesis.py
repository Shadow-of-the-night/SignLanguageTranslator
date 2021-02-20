import eyed3
from aip import AipSpeech
import time
from PyQt5 import QtMultimedia
from PyQt5.QtCore import QUrl
import eyed3

'''生成对应文字的音频文件保存在audio.mp3里并返回此音频的时长'''
def word_to_voice(string):
    APP_ID = '23006671'
    API_KEY = 'GMclpgzxMMmOr0vTdyilgy13'
    SECRET_KEY = 'dOqh3MfMOgxRV7U0RieHAKbAc31S3hoE'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result  = client.synthesis(string, 'zh', 1, {'vol': 5,})

    # 识别正确返回语音二进制 错误则返回dict
    if not isinstance(result, dict):
        with open('audio.mp3', 'wb') as f:
            f.write(result)
        a = eyed3.load("audio.mp3")
        time = a.info.time_secs #获取此音频的播放时间
        return time
    return 0

def bofan(time1):
    file = QUrl.fromLocalFile('audio.mp3') # 音频文件路径
    content = QtMultimedia.QMediaContent(file)
    player = QtMultimedia.QMediaPlayer()
    player.setMedia(content)
    player.setVolume(50.0)
    player.play()
    time.sleep(time1) #设置延时等待音频播放结束

'''
#测试代码
time1=word_to_voice("你好")
print(time1)
bofan(time1)
'''