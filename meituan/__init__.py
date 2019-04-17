import json

import requests

from meituan.util import decode_token, encode_token, str_replace

simulateBrowserHeader = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'gz.meituan.com',
    'Referer': 'https://gz.meituan.com/meishi/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

if __name__ == '__main__':

    cityName = '广州'
    originUrl = str_replace('https://gz.meituan.com/meishi/c11/')
    token_encode = encode_token()
    token = str_replace(token_encode)

    url = 'https://gz.meituan.com/meishi/api/poi/getPoiList?' \
          'cityName=%s' \
          '&cateId=11' \
          '&areaId=0' \
          '&sort=' \
          '&dinnerCountAttrId=' \
          '&page=1' \
          '&userId=' \
          '&uuid=05bf3db6-3c2f-41cd-a4ec-ed79ae0a9506' \
          '&platform=1' \
          '&partner=126' \
          '&originUrl=%s' \
          '&riskLevel=1' \
          '&optimusCode=1' \
          '&_token=%s' % (cityName, originUrl, token)

    response = requests.get(url, headers=simulateBrowserHeader)
    if response.status_code == 200:
        data = response.json()['data']
        with open('data.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False)
            print('Save data into json file successfully!')
            f.close()

    if response.status_code == 403:
        print('Access is denied by server!')

    # cmdline.execute('scrapy crawl food'.split())
