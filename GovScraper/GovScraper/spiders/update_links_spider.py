import scrapy
from scrapy import Selector
import json
from ..items import LinkItem
from model.link import ReturnLinks
import datetime
import time
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from GovScraper.spiders.update_articles_spider import GovUpdateArticleSpider


class GovUpdateLinkSpider(scrapy.Spider):
    name = "govUpdateLinks"
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'GovScraper.pipelines.GovUpdateLinkPipeline': 200,
        }
    }
    
    def start_requests(self):
        url='https://gov.bg/bg/prestsentar/novini?page=1'
        links=ReturnLinks()
        for x in range(0, 1000):
            yield scrapy.Request(url=url, callback=self.parse, meta={'links':links})
            time.sleep(6*1)
            

    def parse(self, response) -> LinkItem:
        sel = Selector(response)
        errorMessage=sel.xpath("//div[@class='error404']")
        if not errorMessage:
            allLinks=sel.xpath("//div[@class='articles']/div[@class='item no-padding']/div[@class='col-lg-5']/a/@href").getall()
            print(allLinks)
            if not allLinks[0] in response.meta['links']:
                for url in allLinks:
                    if url in response.meta['links']:
                        #stop=True
                        break
                    item=LinkItem(
                        link=url, 
                        datetime=datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S%z"),
                    )
                    yield item
                    process = CrawlerProcess(get_project_settings())
                    process.crawl(GovUpdateArticleSpider, url=url)
                    process.start()

                #if not stop:
                    #next_page = response.url[:42]+str(int(response.url[42:])+1)
                    #if next_page is not None:
                       # yield response.follow(next_page, callback=self.parse, meta={'lastLink':response.meta['lastLink']})
    