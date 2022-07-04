# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from dateutil import parser
from model.articles import ArticleModel
from model.link import LinkModel
from GovScraper.items import ArticleItem, LinkItem
from pprint import pprint


class GovArticlePipeline:
    def process_item(self, item, spider) -> ArticleModel:
        #checks if the item is for this pipeline
        try:
            article = ArticleModel.create(**item)
            return article
        except:
            pass

class GovLinkPipeline:
    def process_item(self, item, spider) -> LinkModel:
        # __import__("ipdb").set_trace()
        try:
            link = LinkModel.create(**item)
            return link
        except:
            pass

class GovUpdateLinkPipeline:
    def process_item(self, item, spider) -> LinkModel:
        # __import__("ipdb").set_trace()
        try:
            link = LinkModel.create(**item)
            return link
        except:
            pass

class GovUpdateArticlePipeline:
    def process_item(self, item, spider) -> ArticleModel:
        #checks if the item is for this pipeline
        try:
            article = ArticleModel.create(**item)
            return article
        except:
            pass