[![](https://travis-ci.org/jaywink/python-opengraph.svg?branch=master)](https://travis-ci.org/jaywink/python-opengraph)

# opengraph

Python module to parse Open Graph metadata on web pages. For more information on the Open Graph Protocol, see http://ogp.me/.

Fork of [HenrikOssipoff/python-opengraph](https://github.com/HenrikOssipoff/python-opengraph).

## Compatability

Python 3.10+

Other versions may work, but testing is only done against the above versions.

## Installation

Note the correct name of the fork when installing.

    pip install python-opengraph-jaywink

## Usage

### Using URL

    from opengraph import OpenGraph

    og = OpenGraph(url="http://someurl.com")
    og.title  # would yield the "title" open graph element
    
### Using different parser

Any parser supported by BeautifulSoup can be passed in, assuming it is installed.

    from opengraph import OpenGraph

    og = OpenGraph(url="http://someurl.com", parser="lxml")
    
### Using HTML document

    from opengraph import OpenGraph
    
    document = '<html><head><meta property="og:title" content="Test title"></head><body></body></html>'
    og = OpenGraph(html=document)

## Development

Create a Python 3.10+ virtualenv and then:

    pip install -r dev-requirements.txt

## Testing

    py.test

## License

MIT

## Author

This fork by Jason Robinson (@jaywink / https://jasonrobinson.me).

Original author Henrik Ossipoff Hansen (@HenrikOssipoff).
