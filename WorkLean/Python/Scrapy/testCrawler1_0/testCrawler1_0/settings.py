# -*- coding: utf-8 -*-
# import random

# Scrapy settings for testCrawler1_0 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'testCrawler1_0'

SPIDER_MODULES = ['testCrawler1_0.spiders']
NEWSPIDER_MODULE = 'testCrawler1_0.spiders'

# 用户自定义代理库
# USER_AGENT_LIST = [
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
#     "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
#     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
#     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
#     "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
#     "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
#     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
#     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
#     "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
#     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
#     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
# ]

# USER_AGENT = random.choice(USER_AGENT_LIST)			#每次运行爬虫会使用不同的用户代理,但每次运行中的请求都是不变的

# 用户自定义I代理P池
# 免费代理IP[西刺]是你的好选择！(手滑) 网址：https://www.xicidaili.com/wt
IPPOOL_LIST = [
    {"ipaddr": "124.16.75.212:8080"},
    {"ipaddr": "101.231.234.38:8080"},
    {"ipaddr": "218.64.69.79:8080"},
    {"ipaddr": "144.123.70.252:9999"},
    {"ipaddr": "113.121.21.199:9999"},
    {"ipaddr": "171.35.161.147:9999"},
    {"ipaddr": "27.204.84.42:9999"},
]

# 是否服从 robots.txt 规则,服从为Teur,不服从为False,服从规则有些网站是爬取不到的
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'testCrawler1_0.middlewares.Testcrawler10SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'testCrawler1_0.middlewares.Testcrawler10DownloaderMiddleware': 543,
    # 自定义IP代理池中间件，优先级要高于HttpProxyMiddleware中间件
    'testCrawler1_0.middlewares.IPPOOLS': 747,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 748,
    # 自定义用户代理池中间件，优先级要高于UserAgentMiddleware中间件
    'testCrawler1_0.middlewares.USERAGENTS': 749,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 750,
    # 这里要替换为自己的项目名称,重写的优先级一定要高（数字仅代表优先级，数字越小，优先级越高）

    'scrapy_splash.SplashCookiesMiddleware': 744,
    'scrapy_splash.SplashMiddleware': 745,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'

SPLASH_URL = "http://192.168.99.100:8050/"  # 自己安装的docker里的splash位置
DUPEFILTER_CLASS = "scrapy_splash.SplashAwareDupeFilter"
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html

ITEM_PIPELINES = {
   'testCrawler1_0.pipelines.Testcrawler10Pipeline': 201,
   'testCrawler1_0.pipelines.Testcrawler10ImagePipeline': 200,
}

IMAGES_STORE = 'D:/GitRepository/STAWZW2.0/WorkLean/Python/Scrapy/core-scrapy-master/img/' # 图片存储路径
IMAGES_URLS_FIELD = "image_urls"  # 对应item里面设定的字段，取到图片的url
IMAGES_RESULT_FIELD = "image_path"
# 30 days of delay for images expiration
IMAGES_EXPIRES = 30
# # 图片缩略图
# IMAGES_THUMBS = {
#     'small': (50, 50),
#     'big': (270, 270),
# }
# # 图片过滤器，最小高度和宽度
# IMAGES_MIN_HEIGHT = 110
# IMAGES_MIN_WIDTH = 110


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPERROR_ALLOWED_CODES ——> HTTP请求允许的错误：[code]
HTTPERROR_ALLOWED_CODES = [301]
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# # 是否启用日志
# LOG_ENABLED=True
# # 日志使用的编码
# LOG_ENCODING='utf-8'
# # 日志文件(文件名)
# LOG_FILE='testScrapyLog.log'
# # 日志格式
# LOG_FORMAT='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
# # 日志时间格式
# LOG_DATEFORMAT='%Y-%m-%d %H:%M:%S'
# # 日志级别 CRITICAL, ERROR, WARNING, INFO, DEBUG
# LOG_LEVEL='DEBUG'
# # 如果等于True，所有的标准输出（包括错误）都会重定向到日志，例如：print('hello')
# LOG_STDOUT=True
# # 如果等于True，日志仅仅包含根路径，False显示日志输出组件
# LOG_SHORT_NAMES=False










