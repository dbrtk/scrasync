# Scrasync (asynchronus web scraper)

It is a web scraper built on top of Asyncio and Aiohttp.

## Use of scrasync

Scrasync will not save the web-pages on the hard disk; it will send text extracted from html pages to rmxbot.

### Instantiating and calling the Scraper class
```
from scrasync.scrasper import Scraper


scraper_instance = Scraper(
    endpoint='http://www/example.com',
    depth=1,
    corpusid='corpusid',
    corpus_file_path=''
)
scraper_instance()

```

The parameters required by the Scraper: 
* endpoint - a valid URL;
* depth - crawler's depth;
* corpusid - the id of the corpus (these are defined within rmxbot);
* target_path - the path where files are stored on the remote or local machine.

The parameters corpusid and corpus_file_path are specific to rmxbot.

## Configuration of scrasync

The following variables in the config (https://github.com/dbrtk/scrasync/blob/master/scrasync/config/__init__.py) should be updated:
* PROXIMITY_BOT_HOST - the host of the server that contains rmxbot;
* PROXIMITY_USER- - the username on the server that contains rmxbot (used by rsync/ssh);
* HTTP_TIMEOUT - the timeout set on aiohttp' http getter;

Other config variables are of interest, i.e. CORPUS_MAX_PAGES, AIOHTTP_MAX_URLS. 
