import scrapy
from scrapy import Selector
import json
from ..items import LinkItem
from model.link import ReturnLinks
import time
import subprocess


class GovLinkSpider(scrapy.Spider):
    name = "govUpdate"
    custom_settings = {
        'ITEM_PIPELINES': {
            'GovScraper.pipelines.GovUpdatePipeline': 200,
        }
    }
    def start_requests(self):
        url='https://gov.bg/bg/prestsentar/novini?page=1'
        links=ReturnLinks()
        for x in range(0, 1000):
            yield scrapy.Request(url=url, callback=self.parse, meta={'links':links})
            time.sleep(60*10)
            

    def parse(self, response) -> LinkItem:
        sel = Selector(response)
        errorMessage=sel.xpath("//div[@class='error404']")
        if not errorMessage:
            allLinks=sel.xpath("//div[@class='articles']/div[@class='item no-padding']/div[@class='col-lg-5']/a/@href").getall()
            if allLinks[0]!=response.meta['links']:
                #stop=False
                for url in allLinks:
                    if url in response.meta['links']:
                        #stop=True
                        break
                    yield LinkItem(link=url)
                #if not stop:
                    #next_page = response.url[:42]+str(int(response.url[42:])+1)
                    #if next_page is not None:
                       # yield response.follow(next_page, callback=self.parse, meta={'lastLink':response.meta['lastLink']})