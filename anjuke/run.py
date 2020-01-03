import os
import sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(__file__))

if __name__ == '__main__':
    execute(['scrapy', 'crawl', 'ningbo_community'])
