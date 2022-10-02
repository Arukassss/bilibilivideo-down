# -*-coding:gb2312-*-
import os
import subprocess
import requests
import time


class video(object):
    @classmethod
    def __init__(self):
        self.outpath = 'C:/Users/Arukas/Videos'  # 视频保存的目录
        self.ffmpegpath = './ffmepg.exe' #ffmpeg的目录
        self.last_date = 0
        self.top20created = []
        self.top20bvid = []
        self.mid =   # 用户的UID
        self.bvid = ''
        self.headers = {
            "Referer": f"https://space.bilibili.com/{self.mid}/video",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33",
        }

    def cr_bat(self):  # 创建下载视频的BAT文件
        if len(self.top20bvid) != 0:
            for i in range(len(self.top20bvid)):
                if not os.path.exists(f'{self.top20bvid[i]}.bat'):
                    with open(f'{self.top20bvid[i]}.bat', 'w', newline='') as f:
                        f.write(
                            f'BBdown.exe {self.top20bvid[i]} --work-dir {self.outpath} --ffmpeg-path {self.ffmpegpath}\n')
                        self.last_date = int(time.time())
                        subprocess.Popen(f'{self.top20bvid[i]}.bat', shell=True, stdout=subprocess.DEVNULL,
                                         stderr=subprocess.DEVNULL)

    def test(self):
        row_json = requests.get(
            f'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset=&host_mid={self.mid}&timezone_offset=-480',
            headers=self.headers, timeout=5).json()
        for i in range(len(row_json['data']['items'])):  # 遍历获取的动态内容
            self.top20created.append(row_json['data']['items'][i]['modules']['module_author']['pub_ts'])  # 将所有动态的发布时间遍历
            if row_json['data']['items'][i]['type'] == 'DYNAMIC_TYPE_AV':  # 判断动态类型是否为视频

                if row_json['data']['items'][i]['modules']['module_author']['pub_ts'] > self.last_date:  # 判断是发布时间是否为轮询时间之后
                    title_temp = str(
                        row_json['data']['items'][i]['modules']['module_dynamic']['major']['archive']['title'])
                    if title_temp.find('录播') == -1:  # 判断发布的标题是否含有banWord -1则未匹配到
                        bvid = row_json['data']['items'][i]['modules']['module_dynamic']['major']['archive']['bvid']
                        self.top20bvid.append(bvid)
                        print(f'发现一条新视频{bvid}并添加到列表当中')
        return row_json

    def main(self):
        print('监视已启动，当前监控的mid为：', self.mid)
        print('当前视频文件输出路径为：', self.outpath)
        self.last_date = int(time.time())  # 获取当前时间
        while True:
            print('当前时间：', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time()))))
            times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.last_date))
            print(f'上次轮询时间：{times}')
            try:
                self.test()
            except:
                continue
            self.cr_bat()
            print('等待两分钟后再轮询')
            time.sleep(120)
            self.top20created = []
            self.top20bvid = []


if __name__ == '__main__':
    video().main()
