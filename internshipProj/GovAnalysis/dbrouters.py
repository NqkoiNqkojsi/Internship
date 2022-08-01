from .models import Articles,Entities,EntitiesInArticle

class MyDBRouter(object):
    def db_for_read(self, model, **hints):
        """ reading SomeModel from otherdb """
        if model == Articles:
            return 'articles'
        if model == Entities:
            return 'entities'
        if model == EntitiesInArticle:
            return 'entitiesInArticle'
        return None

    def db_for_write(self, model, **hints):
        """ writing SomeModel to otherdb """
        if model == Articles:
            return 'articles'
        if model == Entities:
            return 'entities'
        if model == EntitiesInArticle:
            return 'entitiesInArticle'
        return None