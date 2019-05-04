import base64
import uuid
import zlib

from datetime import datetime

import requests

from meituan.items import MeituanItem

simulateBrowserHeader = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'gz.meituan.com',
    'Referer': 'https://gz.meituan.com/meishi/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


# 解析token
def decode_token(token):
    # base64解码
    token_decode = base64.b64decode(token.encode())
    # 二进制解压
    token_string = zlib.decompress(token_decode)
    return token_string


# 生成token
def encode_token():
    ts = int(datetime.now().timestamp() * 1000)

    token_dict = {
        'rId': 100900,
        'ver': '1.0.6',
        'ts': ts,
        'cts': ts + 100 * 1000,
        'brVD': [1010, 750],
        'brR': [[1920, 1080], [1920, 1040], 24, 24],
        'bI': ['https://gz.meituan.com/meishi/c11/', ''],
        'mT': [],
        'kT': [],
        'aT': [],
        'tT': [],
        'aM': '',
        'sign': 'eJwdjktOwzAQhu/ShXeJ4zYNKpIXqKtKFTsOMLUn6Yj4ofG4UjkM10CsOE3vgWH36df/2gAjnLwdlAPBBsYoR3J/hYD28f3z+PpUnmJEPqYa5UWEm0mlLBRqOSaP1qjEtFB849VeRXJ51nr56AOSVIi9S0E3LlfSzhitMix/mQwsrdWa7aTyCjInDk1mKu9nvOHauCQWq2rB/8laqd3cX+adv0zdzm3nbjTOdzCi69A/HQAHOOyHafMLmEtKXg=='
    }
    # 二进制编码
    # encode = str(dict(token_dict)).encode()
    encode = str(token_dict).encode()
    # print(encode)
    # 二进制压缩
    compress = zlib.compress(encode)
    # base64编码
    b_encode = base64.b64encode(compress)
    # 转为字符串
    token = str(b_encode, encoding='utf-8')
    return token


# 替换'/+=:'这几个特殊符号，用于URL调用
def str_replace(string):
    return string.replace('/', '%2F') \
        .replace('+', '%2B') \
        .replace('=', '%3D') \
        .replace(':', '%3A')


# get category id
def get_cateId(link_url):
    splits = link_url.split('/')
    return splits[-2].replace('c', '')


# call interface to get json data
def call_interface(page, originUrl):
    cityName = '广州'
    cate_id = get_cateId(originUrl)
    originUrl = str_replace(originUrl)
    token = str_replace(encode_token())

    url = 'https://gz.meituan.com/meishi/api/poi/getPoiList?' \
          'cityName=%s' \
          '&cateId=%s' \
          '&areaId=0' \
          '&sort=' \
          '&dinnerCountAttrId=' \
          '&page=%s' \
          '&userId=' \
          '&uuid=05bf3db6-3c2f-41cd-a4ec-ed79ae0a9506' \
          '&platform=1' \
          '&partner=126' \
          '&originUrl=%s' \
          '&riskLevel=1' \
          '&optimusCode=1' \
          '&_token=%s' % (cityName, cate_id, page, originUrl, token)

    response = requests.get(url, headers=simulateBrowserHeader)
    if response.status_code == 200:
        data = response.json()['data']
        return data

    if response.status_code == 403:
        print('Access is denied by server!')
        return {}


# get food detail from poiInfos
def get_food_list(category, poiInfos):
    item_list = []
    for i in range(0, len(poiInfos)):
        item = MeituanItem()
        item.pk_id = str(uuid.uuid1())
        item.dish_type = category
        item.restaurant_name = poiInfos[i]['title']
        item.location = poiInfos[i]['address']
        item.price = 0 if poiInfos[i]['avgPrice'] is None else int(poiInfos[i]['avgPrice'])
        item.star = float(poiInfos[i]['avgScore'])
        item.img_url = poiInfos[i]['frontImg']
        item.comment_num = int(poiInfos[i]['allCommentNum'])
        item_list.append(item)
    return item_list
