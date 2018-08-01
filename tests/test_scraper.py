

from scrasync.scraper import Scraper


def test_scraper_simple():

    urls = [

        'example.com',
        'http://www.example.com',
        'pferdle',
        'piower///.54t',
        '243423',
        'http://booohooo.com/horrors'
    ]

    expected = [
        'http://booohooo.com/horrors',
        'http://www.example.com'
    ]

    scrap = Scraper(endpoint=urls)
    assert set(scrap.endpoint_list) == set(expected)


def test_filter_ctype():

    urls = [

        'https://edition.cnn.com/',
        'https://www.lemonde.fr/',
        'http://www.liberation.fr/'
    ]

    obj = Scraper(endpoint=urls)
    obj.filter_on_ctype()
    assert urls == obj.endpoint_list


def test_headers():

    urls = [

        'https://edition.cnn.com/',
        'https://www.lemonde.fr/',
        'http://www.liberation.fr/'
    ]
    obj = Scraper(endpoint=urls)
    for resp, err, url in obj.head():
        assert url in urls
        assert resp.content_type == 'text/html'
        assert err is None
