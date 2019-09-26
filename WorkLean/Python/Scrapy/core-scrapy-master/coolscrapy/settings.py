# -*- coding: utf-8 -*-
# Scrapy settings for coolscrapy project

BOT_NAME = 'coolscrapy'

SPIDER_MODULES = ['coolscrapy.spiders']
NEWSPIDER_MODULE = 'coolscrapy.spiders'

IPPOOL_LIST = [
    {"ipaddr": "124.16.75.212:8080"},
    {"ipaddr": "101.231.234.38:8080"},
    {"ipaddr": "218.64.69.79:8080"},
    {"ipaddr": "144.123.70.252:9999"},
    {"ipaddr": "113.121.21.199:9999"},
    {"ipaddr": "171.35.161.147:9999"},
    {"ipaddr": "27.204.84.42:9999"},
]
#-----------------------------------------------------------------------------------
# 爬虫管道
ITEM_PIPELINES = {
    'coolscrapy.pipelines.ArticleDataBasePipeline': 6,
    'coolscrapy.pipelines.ArticleDataImagePipeline': 5,
    # 'coolscrapy.pipelines.TestPipeline': 5,
}
#-----------------------------------------------------------------------------------
# 爬虫下载中间件
DOWNLOADER_MIDDLEWARES = {
    
    'coolscrapy.middlewares.IPPOOLS': 123,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 124,
    'coolscrapy.middlewares.USERAGENTS': 125,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 126,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
#-----------------------------------------------------------------------------------
# 爬虫中间件
# SPIDER_MIDDLEWARES = {
    # 'coolscrapy.middlewares.UrlUniqueMiddleware': 543,
# }
# -----------------------------------------------------------------------------------
# 图片配置
IMAGES_STORE = 'D:/GitRepository/STAWZW2.0/WorkLean/Python/Scrapy/core-scrapy-master/img' # 图片存储路径
IMAGES_URLS_FIELD = "image_urls"  # 对应item里面设定的字段，取到图片的url
IMAGES_RESULT_FIELD = "image_path"
# 图像过期延迟30天
IMAGES_EXPIRES = 30
# # 图片缩略图
# IMAGES_THUMBS = {
#     'small': (50, 50),
#     'big': (270, 270),
# }
# # 图片过滤器，最小高度和宽度
# IMAGES_MIN_HEIGHT = 110
# IMAGES_MIN_WIDTH = 110
# -----------------------------------------------------------------------------------
# 爬虫指定的request下载超时时间
DOWNLOAD_TIMEOUT = 20
# -----------------------------------------------------------------------------------
# 爬虫指定的request下载延迟时间
DOWNLOAD_DELAY = 2
#------------------------------------------------------------------------------------
# 爬虫Cookie
COOKIES_ENABLED = False #默认为True
# COOKIES_DEBUG默认为False
# COOKIES_ENABLES = True
# COOKIES_DEBUG = False
# -----------------------------------------------------------------------------------
# 爬虫日志
# LOG_ENABLED=True
# 日志使用的编码
# LOG_ENCODING='utf-8'
# 日志文件(文件名)
# LOG_FILE='spider.log'
# 日志格式
# LOG_FORMAT='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
# 日志时间格式
# LOG_DATEFORMAT='%Y-%m-%d %H:%M:%S'
# 日志级别 CRITICAL, ERROR, WARNING, INFO, DEBUG
# LOG_LEVEL='INFO'
# 如果等于True，所有的标准输出（包括错误）都会重定向到日志，例如：print('hello')
# LOG_STDOUT=True
# 如果等于True，日志仅仅包含根路径，False显示日志输出组件
# LOG_SHORT_NAMES=False
# -----------------------------------------------------------------------------------
# 是否服从 robots.txt 规则,服从为Teur,不服从为False,服从规则有些网站是爬取不到的
ROBOTSTXT_OBEY = False
# -----------------------------------------------------------------------------------
# windows pip install mysqlclient
# 爬虫数据库链接信息
DATABASE = {'drivername': 'mysql',
            'host': 'localhost',
            'port': '3306',
            'username': 'root',
            'password': 'root',
            'database': 'test',
            'query': {'charset': 'utf8'}}
# -----------------------------------------------------------------------------------
# CLOSESPIDER_ITEMCOUNT = 10
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS=32

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN=16
# CONCURRENT_REQUESTS_PER_IP=16

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED=False
# -----------------------------------------------------------------------------------
# 爬虫设置默认请求头固定部分
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }
# -----------------------------------------------------------------------------------
# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
# }
# -----------------------------------------------------------------------------------
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
# AUTOTHROTTLE_ENABLED=True
# The initial download delay
# AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG=False
#------------------------------------------------------------------------------------
# 启用和配置HTTP缓存（默认情况下禁用）
HTTPCACHE_ENABLED = True
# 缓存策略
HTTPCACHE_POLICY = 'scrapy.extensions.httpcache.RFC2616Policy'
# 缓存的请求的到期时间,以秒为单位,如果为零,则缓存的请求将永不过期
HTTPCACHE_EXPIRATION_SECS=0
# 缓存路径
HTTPCACHE_DIR='httpcache'
# 不要使用这些HTTP代码缓存响应
HTTPCACHE_IGNORE_HTTP_CODES=[]
# 存储位置
HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
