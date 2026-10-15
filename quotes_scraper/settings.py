BOT_NAME = 'quotes_scraper'
SPIDER_MODULES = ['quotes_scraper.spiders']
NEWSPIDER_MODULE = 'quotes_scraper.spiders'
ROBOTSTXT_OBEY = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
