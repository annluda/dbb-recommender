# -*- coding: utf-8 -*-
import requests
import time

if __name__ == '__main__':

    url = "http://piping.mogumiao.com/proxy/api/get_ip_bs?" \
          "appKey=5ef71d2e44cb4139a99278b1215db26e&count=5&expiryDate=0&format=2&newLine=2"

    while True:
        try:
            res = requests.get(url)

            with open('/Users/ald/PycharmProjects/dbb-recommender/daq/scrapy/ips.txt', 'w') as f:
                f.write(res.text)
        except Exception:
            pass

        time.sleep(10)
