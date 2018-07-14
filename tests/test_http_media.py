
import asyncio


from scrasync.async_http import ContentTypeError, run


def test_http_with_media():

    url = 'http://chroma.dbrtk.net/video/chroma_demo_2.ogg'

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run([url]))

    out = loop.run_until_complete(future)
    assert isinstance(out[0][0], ContentTypeError)


def test_fetch_head_media():

    url = 'http://chroma.dbrtk.net/video/chroma_demo_2.ogg'

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run([url], head_only=True))

    out = loop.run_until_complete(future)
    assert isinstance(out[0][0].content_type, str)
    assert isinstance(out[0][1], str)
    assert out[0][1] == url
