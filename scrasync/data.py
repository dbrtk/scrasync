
import re

from celery.contrib import rdb

from .parser import WebParser

SPECIAL_TAGS = ['img']
MEDIA_TAGS = ['img', 'video', 'canvas', 'audio']
BLOCK_TAGS = MEDIA_TAGS + ['meta', 'button', 'nav']

# miscellaneous tags are basically difficult tags.
MISCELLANEOUS_TAGS = ['div', 'a', 'ul', 'li', 'span']


class DataToTxt(object):

    def __init__(self, url: str = None, http_resp: str = None):

        self.url = url
        self.data = []
        self.http_resp = http_resp
        self.links = None

        self.parser = WebParser(url=self.url)

        self.parser.feed(str(self.http_resp))
        self.out_data = []

    def __call__(self):

        self.data = self.parser.get_struct_data()
        self.links = self.parser.get_links()

        # del self.parser

        self.data_to_corpus()

    def data_to_corpus(self):
        """ Dumping data into a corpus file. """
        head = ''
        if head.strip():
            self.out_data.append(head)
        for item in self.data:

            if item[0] in BLOCK_TAGS:
                continue

            elif item[0] in MISCELLANEOUS_TAGS:
                if not re.match(r'\s\w+\b', item[1]):
                    continue
                if not len(re.findall(r'\s[a-zA-Z]+\b', item[1])) > 4:
                    continue
            else:
                _data = clean_tagcontent(str(item[1]))

            if not isinstance(_data, str):
                continue
            self.out_data.append(_data)
        head = '{}\n\n'.format(head or self.url)
        self.out_data.append(head)
        del self.data


def clean_tagcontent(txt):
    """ Cleaning up the tag content from newlines and tabs. """
    txt = re.sub(r'[\t\n]', ' ', txt)
    return re.sub(r'\s+', ' ', txt)
