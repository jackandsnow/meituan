import base64
import zlib

from datetime import datetime


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
