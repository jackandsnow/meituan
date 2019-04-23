from scrapy import cmdline

from meituan.util import decode_token, encode_token, str_replace

if __name__ == '__main__':
    cmdline.execute('scrapy crawl food'.split())
