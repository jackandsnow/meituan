# meituan
Crawl Meituan Food Data

This project is aiming to crawl food data from meituan's website.

1. Environment you need:
  Python 3, MySQL 5.7(or later), PyCharm(not necessary)

2. Python packages needed:
  scrapy, pymysql

3. Attention:
  Please remember to create database 'meituan' in MySQL frist, and create table 'TB_RESTAURANTS' of 'meituan'.
  Otherwise, this project won't work successfully on your computer.

4. Run project:
  After your environment is ready, you just need to run "scrapy crawl food" in terminal or cmd window.
  Also, you can run 'python3 meituan/\_\_init__.py' in the project directory.
  And then you can get the food data of meituan in your database.
