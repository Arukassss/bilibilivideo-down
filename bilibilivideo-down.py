# -*-coding:gb2312-*-
import os
import subprocess
import requests
import time


class video(object):
    @classmethod
    def __init__(self):
        self.outpath = 'C:/Users/Arukas/Videos'  # ��Ƶ�����Ŀ¼
        self.ffmpegpath = './ffmepg.exe' #ffmpeg��Ŀ¼
        self.last_date = 0
        self.top20created = []
        self.top20bvid = []
        self.mid =   # �û���UID
        self.bvid = ''
        self.headers = {
            "Referer": f"https://space.bilibili.com/{self.mid}/video",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33",
        }

    def cr_bat(self):  # ����������Ƶ��BAT�ļ�
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
        for i in range(len(row_json['data']['items'])):  # ������ȡ�Ķ�̬����
            self.top20created.append(row_json['data']['items'][i]['modules']['module_author']['pub_ts'])  # �����ж�̬�ķ���ʱ�����
            if row_json['data']['items'][i]['type'] == 'DYNAMIC_TYPE_AV':  # �ж϶�̬�����Ƿ�Ϊ��Ƶ

                if row_json['data']['items'][i]['modules']['module_author']['pub_ts'] > self.last_date:  # �ж��Ƿ���ʱ���Ƿ�Ϊ��ѯʱ��֮��
                    title_temp = str(
                        row_json['data']['items'][i]['modules']['module_dynamic']['major']['archive']['title'])
                    if title_temp.find('¼��') == -1:  # �жϷ����ı����Ƿ���banWord -1��δƥ�䵽
                        bvid = row_json['data']['items'][i]['modules']['module_dynamic']['major']['archive']['bvid']
                        self.top20bvid.append(bvid)
                        print(f'����һ������Ƶ{bvid}����ӵ��б���')
        return row_json

    def main(self):
        print('��������������ǰ��ص�midΪ��', self.mid)
        print('��ǰ��Ƶ�ļ����·��Ϊ��', self.outpath)
        self.last_date = int(time.time())  # ��ȡ��ǰʱ��
        while True:
            print('��ǰʱ�䣺', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time()))))
            times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.last_date))
            print(f'�ϴ���ѯʱ�䣺{times}')
            try:
                self.test()
            except:
                continue
            self.cr_bat()
            print('�ȴ������Ӻ�����ѯ')
            time.sleep(120)
            self.top20created = []
            self.top20bvid = []


if __name__ == '__main__':
    video().main()
