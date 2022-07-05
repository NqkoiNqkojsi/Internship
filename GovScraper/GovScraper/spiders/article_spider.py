from re import A
import scrapy
import json
from ..items import ArticleItem
from datetime import datetime
from model.link import ReturnLinks


class GovArticleSpider(scrapy.Spider):
    name = "govArticle"
    custom_settings = {
        'ITEM_PIPELINES': {
            'GovScraper.pipelines.GovArticlePipeline': 200
        }
    }
    def start_requests(self):
        data = ReturnLinks()
        for url in data:
            yield scrapy.Request(url=url, callback=self.parse)
                

    def parse(self, response) -> ArticleItem:
        article=response.css("div.container")[1]# gets only the html of the article without navigation and such
        pageText =article.css("p::text").getall()
        #article.xpath("//div[@dir='auto']").extract()
        if len(pageText)>1:
            # using list comprehension to
            # Remove blank spaces from List
            pageText = [i for i in pageText if i != " "]
            pageTitle=article.css("h1::text").getall()
            pageImgs=article.css('img').xpath('@src').get() #gets the adresses of the displayed images
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
        