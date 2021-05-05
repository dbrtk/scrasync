
from django.db import models

from .config.appconf import HEXDIGEST_SIZE


class CrawlState(models.Model):
    """
    The model for the crawl state - this is used by scrasync to store the crawl
    status.

    `crawlid` and `urlid` store digest values of blake2b with a default size of
    64 bytes.
    """
    crawlid = models.CharField(max_length=HEXDIGEST_SIZE, null=True)
    # containerid = models.IntegerField()
    url = models.URLField()
    urlid = models.CharField(max_length=HEXDIGEST_SIZE, null=True)
    ready = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['url', 'crawlid'],
    #             name='unique_url_for_crawl'
    #         )
    #     ]

    # @classmethod
    # def create(cls, crawlid: str = None, containerid: int = None,
    #            url: str = None, urlid: str = None):
    #     """
    #     :param crawlid:
    #     :param containerid:
    #     :param url:
    #     :param urlid:
    #     :return:
    #     """
    #     # todo(): delete this
    #     container = Container.get_object(containerid)
    #
    #     obj = cls(crawlid=crawlid, container=container, url=url,
    #               urlid=urlid)
    #     obj.save()
    #     return obj

    @classmethod
    def push_many(cls, urls: list = None, crawlid: str = None):
        """
        Push many items to the crawl_state collection.
        :param urls:
        :param crawlid:
        :return:
        """
        try:
            duplicates = cls.objects.filter(
                crawlid=crawlid, url__in=[_[0] for _ in urls]
            )
        except cls.DoesNotExist:
            duplicates = []
        duplicates = [(_.url, _.urlid) for _ in duplicates]
        urls = list(set(urls).difference(duplicates))
        objs = cls.objects.bulk_create([
            cls(url=url,
                crawlid=crawlid,
                urlid=urlid)
            for url, urlid in urls
        ])
        return objs, duplicates

    @classmethod
    def state_list(cls, crawlid: str = None):
        """ For a containerid, retrieve all documents. This shows all active
            processes (scraping, html cleanup, writing to disk).
        """
        try:
            return cls.objects.filter(crawlid=crawlid)
        except cls.DoesNotExist:
            return []

    @classmethod
    def get_saved_endpoints(cls, crawlid: str = None):
        """ Returns a list of saved endpoints. """
        return [_.url for _ in cls.state_list(crawlid=crawlid)]

    @classmethod
    def delete_many(cls, crawlid: str = None):
        """
        Deletes many objects from the database.
        :param crawlid:
        :return:
        """
        try:
            cls.objects.filter(crawlid=crawlid).delete()
        except cls.DoesNotExist:
            pass
