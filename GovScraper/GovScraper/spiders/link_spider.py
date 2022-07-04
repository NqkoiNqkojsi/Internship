from datetime import datetime
import scrapy
from scrapy import Selector
import json
from ..items import LinkItem


class GovLinkSpider(scrapy.Spider):
    name = "govLink"
    custom_settings = {
        'ITEM_PIPELINES': {
            'GovScraper.pipelines.GovLinkPipeline': 200,
        }
    }
    def start_requests(self):
        url='https://gov.bg/bg/prestsentar/novini?page=1'
        yield scrapy.Request(url=url, callback=self.parse)
            

    def parse(self, response) -> LinkItem:
        sel = Selector(response)
        errorMessage=sel.xpath("//div[@class='error404']")
        if not errorMessage:
            links=sel.xpath("//div[@class='articles']/div[@class='item no-padding']/div[@class='col-lg-5']a/@href").extract()
            for url in links:
                item=LinkItem(
                    link=url, 
                    datetime=datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S%z"),
                    )
                yield item
            
            next_page = response.url[:42]+str(int(response.url[42:])+1)
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
        
