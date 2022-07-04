# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy_jsonschema.item import JsonSchemaItem


class ArticleItem(JsonSchemaItem):
    jsonschema = {
        "$schema": "http://json-schema.org/draft-07/schema",
        "title": "article",
        "description": "The info crawled from article",
        "type": "object",
        "properties": {
            "date": {"type": "string", "format": "date"},
            "url": {"type": "string"},
            "images": {"type": "string"},
            "videos": {"type": "string"},
            "title": {"type": "string"},
            "body": {"type": "string"}
        },
        "required": [
            "date",
            "url",
            "images",
            "videos",
            "title",
            "body"
        ],
    }

class LinkItem(JsonSchemaItem):
    jsonschema = {
        "$schema": "http://json-schema.org/draft-07/schema",
        "title": "board",
        "description": "The links for articles",
        "type": "object",
        "properties": {
            "link": {"type": "string"},
            "datetime": {"type": "string", "format": "date-time"}
        },
        "required": [
            "link", 
            "datetime"
        ],
    }
