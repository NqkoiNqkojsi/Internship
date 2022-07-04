import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from GovScraper.spiders.article_spider import GovArticleSpider
from GovScraper.spiders.link_spider import GovLinkSpider
from GovScraper.spiders.update_links_spider import GovUpdateLinkSpider
import model.articles as ModelArticles
import model.link as ModelLink
import sys     

def start_program():
    try:
        ModelArticles.initialize_db()
        ModelLink.initialize_db()
    except:
        return "Error with initializing DBs"

    process = CrawlerProcess(get_project_settings())
    if "twisted.internet.reactor" in sys.modules: 
        print("trying to delete reactor")
        del sys.modules["twisted.internet.reactor"]
    process.start()
    process.crawl(GovLinkSpider)
    if "twisted.internet.reactor" in sys.modules: 
        print("trying to delete reactor")
        del sys.modules["twisted.internet.reactor"]
    process.start()
    process.crawl(GovArticleSpider)
    if "twisted.internet.reactor" in sys.modules: 
        print("trying to delete reactor")
        del sys.modules["twisted.internet.reactor"]
    process.start()
    process.crawl(GovUpdateLinkSpider)
    if "twisted.internet.reactor" in sys.modules: 
        print("trying to delete reactor")
        del sys.modules["twisted.internet.reactor"]
    process.start()


if __name__=="__main__":
    start_program()