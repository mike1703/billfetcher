# -*- coding: utf-8 -*-

# Scrapy settings for billfetcher project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'billfetcher'

SPIDER_MODULES = ['billfetcher.spiders']
NEWSPIDER_MODULE = 'billfetcher.spiders'

ARCHIVE_DIR = '/path/to/archive'
USERNAME = ''
PASSWORD = ''

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'billfetcher (+http://www.yourdomain.com)'
