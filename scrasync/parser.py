""" Parsing htmlm files in order to retrieve texts and images. """
import re
import uuid
from urllib import parse as urlparse

import html.parser as HTMLParser

from .misc.validate_url import ValidateURL, ValidationError
from .html_tags import HTML_TAGS


BLOCK_TAGS = ['script', 'style', 'link', 'meta']
NESTED_TAGS = ['wbr', 'a', 'b', 'abbr', 'bdi', 'dfn', 'cite', 'span', 'i',
               'font', 'strong', 'sup', 'sub']
IGNORE_TAGS = ['br', 'img', 'input', 'hr']

ENCODE_TO_JSON = 1
HIRES_IMGS = 0


def _clear_txt(_txt):
    """ Cleaning up the text (the content of tags) from unnecessary characters.
    """
    _ptrns = [
        r"^\s{0,}[\)\.\\|/,:;]",
        r"[\^|]",
        r"^\s{0,}[A-Za-z]{1}$",
        r"^[0-9\s\.\-/]+$"
    ]
    for _ptrn in _ptrns:
        if re.match(_ptrn, _txt):
            _txt = re.sub(_ptrn, "", _txt)
    return _txt.strip()


def strip_txt(txt):
    """ Removing string literals truncated with a double back-slash. """
    patterns = [
        # r"\\[abfnrtv]",
        r"\[abfnrtv]",
        r"^b'$",
    ]
    for pttrn in patterns:
        txt = re.sub(pttrn, ' ', txt)
        txt = txt.strip()
    txt = re.sub(r'\s+', ' ', txt)
    return txt


class WebParser(HTMLParser.HTMLParser):
    """ Parsing the html that is returned by the scraper. """

    def __init__(self, *args, **kwargs):
        """  """
        self.config = dict(
            with_js=0,
            with_css=0
        )
        if "url" in kwargs:
            self.url = urlparse.urlparse(kwargs.get("url"))
            kwargs.pop("url")
        else:
            raise KeyError("A url paramenter is required.")
        self.img_urls = []
        self.links = []
        self.data_is_txt = True

        self.struct_data = list()
        self.dt_buffer = []
        self.is_o = False
        self.curr_tag = ""

        self.with_nested = 0
        self.nested_tag = ""
        self.nested_is_o = 0
        self.nested_buffer = []
        self.nested_list = []
        self.nested_attrs = dict() if ENCODE_TO_JSON else ()

        self.open_tags = []
        self.tag_attrs = dict() if ENCODE_TO_JSON else ()
        try:
            super(WebParser, self).__init__(*args, **kwargs)
        except TypeError:
            HTMLParser.HTMLParser.__init__(self, *args, **kwargs)
        else:
            pass

    def get_struct_data(self):
        """ returns structured data
        """
        return self.struct_data

    def get_data(self):
        """ returns the processed data """
        return self.struct_data,

    def handle_starttag(self, tag, attrs):
        """ Actions performed when hitting a start tag. document... """
        attrs = dict(attrs) if attrs else {}

        if self.is_o and tag in NESTED_TAGS:
            if tag == 'a':
                self.nested_tag, self.nested_is_o = tag, 1
            else:
                pass
        # elif tag == "br":
        #     self._handle_newline()
        elif tag in IGNORE_TAGS:
            pass
        else:
            self.curr_tag = tag
            self.is_o = True

        # the data_is_txt attribute needs to be reset in some cases
        # we need to get the title
        if not self.data_is_txt and tag == 'title':
            self.data_is_txt = True

        if tag in BLOCK_TAGS:
            self.data_is_txt = False
        elif tag not in HTML_TAGS:
            # Some tags containing binary data are not standard.
            self.data_is_txt = False
        else:
            self.open_tags.append((tag, attrs))

        if tag == "img":
            self.__handle_img(attrs)
        elif tag == "a":
            self.__handle_a(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        """ Handling XML-style tags like: <img [...] />"""
        # if tag in BLOCK_TAGS:
        #     return False
        attrs = attrs if isinstance(attrs, dict) else dict(attrs)
        if tag == "img":
            self.open_tags.append((tag, attrs))
            self.__handle_img(attrs)

    def handle_endtag(self, tag):
        """ Actions to be performed when hitting the end of a tag. """
        if self.nested_is_o and self.nested_tag == tag == "a":
            self.__close_a(tag)
            return 1
        if self.is_o and tag not in IGNORE_TAGS and tag not in NESTED_TAGS:
            _dt = self.__to_struct_data()
            if _dt:
                self.struct_data.append(_dt)
            self.dt_buffer, self.is_o = [], False
        self.data_is_txt = True
        self.tag_attrs = {}
        if self.open_tags:
            _tag, _attrs = self.open_tags[-1]
            del _attrs
            if _tag == tag:
                self.open_tags.pop(len(self.open_tags) - 1)
        if self.nested_list and self.with_nested:
            for item in self.nested_list:
                self.struct_data.append(item)

    def _handle_newline(self):
        """
        """
        # todo(): review this method.

        # self.dt_buffer.append('\n')

        pass

    def handle_data(self, data):
        """ handling data, such as text """
        if not self.data_is_txt:
            return False

        data = strip_txt(data)

        if data:
            # todo(): review the word count algorithm
            # self.txt_dt += " %s " % data
            self.dt_buffer.append(data.strip())
        if self.nested_is_o and self.nested_tag:
            self.nested_buffer.append(data.strip())

    def __to_struct_data(self):
        """ Inserting chunks of text/string to structure data. Before insertion,
         data needs to be processed. """
        # _txt = _clear_txt(' '.join(self.dt_buffer.split()))

        _txt = _clear_txt(' '.join(self.dt_buffer))
        if _txt:
            if ENCODE_TO_JSON:
                _out = [self.curr_tag, _txt]
                if self.tag_attrs:
                    _out.append(self.tag_attrs)
                return _out
            else:
                return (self.curr_tag, _txt, self.tag_attrs) \
                    if self.tag_attrs else (self.curr_tag, _txt)
        return 0

    def __handle_script_tag(self):
        """ handling all the is contained in a script tag """
        pass

    def __handle_style_tag(self):
        """ handling all the is contained in a style tag """
        pass

    def __handle_img(self, attrs, process=False):
        """ handle image tags - there will be a way of handling data  """
        url = self.__make_url(attrs.get("src"))
        parent_tag = self.open_tags[len(self.open_tags) - 2]
        if parent_tag[0] == 'a':
            _hires = self.__make_url(parent_tag[1].get('href'))
            url = (_hires, url,)
        if url and not isinstance(url, tuple):
            url = (url,)
        if url:
            if not process and url not in self.img_urls:
                self.img_urls.append(url)
                self.struct_data.append([
                    'img', uuid.uuid4(), dict(src=url)
                ])
            if process:
                # todo(): implement immediate saving when process is true
                pass
        return 1

    def __handle_a(self, tag, attrs):
        """ processing the a tag - link/href, as a normal or nested tag """
        if self.curr_tag == tag:
            attrs_obj = self.tag_attrs
        elif self.nested_tag == tag:
            attrs_obj = self.nested_attrs
        else:
            raise RuntimeError("Problems while processing the 'a' tag.")
        _url = self.__make_url(attrs.get("href"))
        if _url:
            self.links.append(_url)
        if isinstance(attrs_obj, tuple):
            attrs_obj = (('href', _url),)
        elif isinstance(attrs_obj, dict):
            attrs_obj["href"] = _url
        return 1

    def __external_link(self, href):
        """ checking if a link is not pointing to the same page """
        _ptrn = r"^%s" % re.escape(self.url.geturl())
        return 0 if re.match(_ptrn, href) else 1

    def __close_a(self, tag):
        """ handling the closing of a nested 'a' tag """
        assert tag == "a", "'__close_a' works only with 'a' tags"
        if self.nested_tag == "a" and self.nested_attrs:
            _data = _clear_txt(' '.join(self.nested_buffer))
            _href = self.nested_attrs.get("href")

            if _href and _data and self.__external_link(_href):
                _tag = [tag, _data, dict(href=_href)]
                self.nested_list.append(_tag)
            self.nested_tag, self.nested_is_o = "", 0
            self.nested_buffer = []
            self.nested_attrs = {}
        else:
            return 0

    def get_img_urls(self):
        """ returns img urls """
        return self.img_urls

    def get_links(self):
        """ returning the urls that have been collected from links """
        return self.links

    def close(self):
        """ closing the parser """
        HTMLParser.HTMLParser.close(self)

    def __make_url(self, url, validate=True):
        """ Making a url - used for making urls pointing to media (i.e. img).
        """
        if not url:
            return False
        validator = ValidateURL(raise_error=True)

        def hosturl(_o): return urlparse.urlparse(
            "//%s" % _o.hostname, _o.scheme).geturl()

        def valurl(_url):
            """ validate else return false """
            try:
                validator(_url)
            except ValidationError:
                return False
            else:
                return _url
        if re.match(re.compile('^data:'), url):
            outurl = False
        elif re.match(re.escape("//"), url):
            outurl = urlparse.urlparse(url, scheme=self.url.scheme).geturl()
        elif not re.match('^http:|https:', url):
            if valurl(url):
                outurl = url
            else:
                outurl = valurl(urlparse.urljoin(hosturl(self.url), url)) or \
                    valurl(urlparse.urljoin(self.url.geturl(), url))
        else:
            if validate:
                outurl = url if valurl(url) else False
            else:
                outurl = url
        return outurl

    def update_structdata(self, idx, value):
        """ updating a tqag object within struct_data """
        self.struct_data[idx] = value

    def make_image_object(self, idx):
        """ given the index within structured data, makes an image object """
        pass

    def get_imgs_fromstruct(self):
        """
        """
        return [(idx, _i,) for idx, _i in enumerate(self.get_struct_data())
                if _i[0] == 'img']
