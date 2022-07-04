from re import A
import scrapy
import json
from ..items import ArticleItem
from datetime import datetime


class GovUpdateArticleSpider(scrapy.Spider):
    name = "govUpdateArticle"

    start_url = ""
    def __init__(self, url=''):
        self.start_url = [url]
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'GovScraper.pipelines.GovUpdateArticlePipeline': 200
        }
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)
                

    def parse(self, response) -> ArticleItem:
        article=response.css("div.container")[1]# gets only the html of the article without navigation and such
        pageTitle=article.css("h1::text").getall()
        pageText =[]
        for p in article.css("p::text").getall():
            #should clean the body of useless blank spaces
            if not p == " ":
                pageText.append(p)
        pageImgs=article.css('img').xpath('@src').getall() #gets the adresses of the displayed images
        pageVideo=article.css('iframe').xpath('@src').getall() #gets the link to an embedded video if it has otherwise returns null
        item=ArticleItem(
            date="".join(pageText[0]),
            url=response.url,
            images="".join(pageImgs),
            videos="".join(pageVideo),
            title="".join(pageTitle),
            body="".join(pageText[1:])
        )
        yield item