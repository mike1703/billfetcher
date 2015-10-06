# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from dateutil.parser import parse
from urlparse import urljoin
import os
import os.path

class DeutschlandsimSpider(scrapy.Spider):
    name = "deutschlandsim"
    allowed_domains = ["service.deutschlandsim.de"]
    settings = {}
    start_urls = (
        'https://service.deutschlandsim.de/',
    )

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        my_settings = {'ARCHIVE_DIR': settings.get('ARCHIVE_DIR'),
                       'USERNAME': settings.get('USERNAME'),
                       'PASSWORD': settings.get('PASSWORD'),
                      }
        return cls(my_settings)

    def __init__(self, settings):
        self.settings = settings

    def parse(self, response):
        return scrapy.FormRequest.from_response(response,
                                                formdata={'UserLoginType[alias]': self.settings['USERNAME'],
                                                          'UserLoginType[password]': self.settings['PASSWORD']},
                                                callback=self.after_login
                                                )
    def after_login(self, response):
        if 'Passwort falsch' in response.body:
            self.log('Login failed', level=scrapy.log.ERROR)
            return
        else:
            self.log('Login successful', level=scrapy.log.INFO)
            return scrapy.Request(url='https://service.deutschlandsim.de/mytariff/invoice/show',
                                  callback=self.parse_invoice_list
                                  )

    def parse_invoice_list(self, response):
        invoices = response.selector.xpath("//div[@id='rechnungen']/div/div/span")
        for invoice in invoices:
            invoice_selector = Selector(text=invoice.extract())
            # invoice_selector = invoice
            # "Rechnung vom DD.MM.YYYY" -> datetime
            date = parse(invoice_selector.xpath("//p/text()")[0].extract().split(' ')[-1])
            invoice_types = invoice_selector.xpath("//p/a")
            for invoice_type_raw in invoice_types:
                invoice_type_selector = Selector(text=invoice_type_raw.extract())
                # invoice_type_selector = invoice_type_raw
                # "Rechnung"/"Einzelverbindungsnachweis"
                invoice_type = invoice_type_selector.xpath("//a/text()")[0].extract()
                # "/mytariff/invoice/showPDF/123456478"
                invoice_link = invoice_type_selector.xpath("//a/@href")[0].extract()
                invoice_absolute_link = urljoin(response.url, invoice_link)
                self.log("Found %s for %s with url %s" % (invoice_type, date.strftime("%Y-%m-%d"), invoice_absolute_link), level=scrapy.log.INFO)

                spider_dir = "%s/%s" % (self.settings['ARCHIVE_DIR'], self.name)
                filename = "%s/%s-%s.pdf" % (spider_dir, date.strftime("%Y-%m-%d"), invoice_type)

                if not os.path.isdir(spider_dir):
                    os.makedirs(spider_dir)

                if not os.path.isfile(filename):
                    yield scrapy.Request(url=invoice_absolute_link,
                                        meta={'filename': filename},
                                        callback=self.save_pdf
                                        )

    def save_pdf(self, response):
        filename = response.meta['filename']
        self.log("Downloading %s" % (filename), level=scrapy.log.INFO)
        with open(filename, 'w') as pdf:
            pdf.write(response.body)

