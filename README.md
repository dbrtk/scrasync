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
* corpus_file_path - the path where files are stored on the remote or local machine.

The parameters corpusid and corpus_file_path are specific to rmxbot.
