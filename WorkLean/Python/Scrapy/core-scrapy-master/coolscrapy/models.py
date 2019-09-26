# -*- encoding: utf-8 -*-
"""
Topic: 定义数据库模型实体
Desc : 
"""
import datetime

from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from coolscrapy.settings import DATABASE
from sqlalchemy.ext.declarative import declarative_base

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**DATABASE))

def create_news_table(engine):
    """"""
    Base.metadata.create_all(engine)

Base = declarative_base()

class ArticleRule(Base):
    """自定义文章爬取规则"""
    # 数据库规则表-表名：scrapy_test1
    __tablename__ = 'scrapy_test1'

    id = Column(Integer, primary_key=True)
    # 规则名称
    name = Column(String(30))
    # 运行的域名列表，逗号隔开
    allow_domains = Column(String(100))
    # 开始URL列表，逗号隔开
    start_urls = Column(String(100))
    # 解析规则选择
    selectors = Column(String(100))
    # 下一页的xpath
    next_page = Column(String(100))
    # 文章链接正则表达式(子串)
    allow_url = Column(String(200))
    # 文章链接提取区域xpath
    extract_from = Column(String(200))
    # 文章标题xpath
    title_path = Column(String(100))
    # 文章发布时间xpath
    releaseTime_path = Column(String(100))
    # 文章图片xpath
    image_path = Column(String(100))
    # 文章内容xpath
    body_path = Column(String(100))
    # 文章来源
    source_site_path = Column(String(100))
    # 规则是否生效
    enable = Column(Integer)

class Article(Base):
    """文章类"""
    # 数据库数据表-articles
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    url = Column(String(100))
    title = Column(String(100))
    releaseTime = Column(String(100))
    image_urls = Column(Text)
    images = Column(String(1000))
    image_paths = Column(String(1000))
    body = Column(Text)
    source_site = Column(String(100))
