from aip import AipSpeech
from ffmpy import FFmpeg


# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

'''将本地音频文件input.wav 转化成文字 并返回'''
def voice_to_context():
    APP_ID = '23006671'
    API_KEY = 'GMclpgzxMMmOr0vTdyilgy13'
    SECRET_KEY = 'dOqh3MfMOgxRV7U0RieHAKbAc31S3hoE'

    # 将mp3转化为pcm
    ff = FFmpeg(executable='./ffmpeg-N-99980-g9208b72a38-win64-gpl-shared/bin/ffmpeg.exe',
                inputs={'audio.mp3': "-y"},
                outputs={'audio.pcm': "-acodec pcm_s16le -f s16le -ac 2 -ar 16000"})

    ff.run()

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    s = client.asr(get_file_content('input.wav'), 'wav', 16000, {
        'dev_pid': 1537,
    })
    print(s['result'][0])
    return s['result'][0]

#print(voice_to_context())