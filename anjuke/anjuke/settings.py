# -*- coding: utf-8 -*-

# Scrapy settings for anjuke project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'anjuke'

SPIDER_MODULES = ['anjuke.spiders']
NEWSPIDER_MODULE = 'anjuke.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'anjuke (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    # ':authority': 'nb.zu.anjuke.com',
    # ':method': 'GET',
    # ':path': '/fangyuan/p5/',
    # ':scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'cookie': 'sessid=B6305D5E-A8B0-E771-D19F-0BE4E3188E06; aQQ_ajkguid=126FAD93-73B6-90BF-EB8A-F1F4A68B5D60; lps=http%3A%2F%2Fnb.anjuke.com%2F%7C; ctid=32; twe=2; ANJUKE_BUCKET=pc-home%3AErshou_Web_Home_Home-a; _ga=GA1.2.2119016282.1577793913; _gid=GA1.2.1817212992.1577793913; 58tj_uuid=153d294f-082f-4bd7-b780-34f08b1ee29b; new_session=1; init_refer=; new_uv=1; als=0; wmda_uuid=9c460c668ae3469f97347c0d86df9f39; wmda_new_uuid=1; wmda_session_id_6289197098934=1577793978621-6c838d82-9096-04c4; wmda_visited_projects=%3B6289197098934; xzfzqtoken=%2BtRw%2Bwj9QjmZl%2FtsuL6e65XUvvS0eAZET38a5sUX%2FM48NcfhNRM7qF8pydGyI61qin35brBb%2F%2FeSODvMgkQULA%3D%3D',
    'pragma': 'no-cache',
    'referer': 'https://nb.zu.anjuke.com/fangyuan/p2/',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'anjuke.middlewares.AnjukeSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'anjuke.middlewares.AnjukeDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'anjuke.pipelines.MongoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'main'
MONGO_USER = None
MONGO_PWD = None
