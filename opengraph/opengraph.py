import logging
import re
import time

import requests
from bs4 import BeautifulSoup
from requests import RequestException

from opengraph import __version__

USER_AGENT = "python-opengraph-jaywink/%s (+https://github.com/jaywink/python-opengraph)" % __version__

logger = logging.getLogger(__name__)


class OpenGraph:
    def __init__(self, url=None, html=None, useragent=None, parser="html.parser", timeout=10, max_seconds=15,
                 max_bytes=1024 * 1024):
        self._data = {}
        self.timeout = timeout
        self.max_seconds = max_seconds
        self.max_bytes = max_bytes
        self.headers = {
            "user-agent": useragent or USER_AGENT,
        }
        content = html or self._fetch(url)
        self._parse(content, parser=parser)

    def __contains__(self, item):
        return item in self._data

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(
            "Open Graph object has no attribute '{}'".format(name))

    def __repr__(self):
        return self._data.__str__()

    def __str__(self):
        return self.__repr__()

    def _fetch_content_type(self, url):
        try:
            response = requests.head(url, headers=self.headers, timeout=self.timeout)
        except RequestException as ex:
            logger.debug("_fetch_content_type - %s when fetching url %s", ex, url)
            return ""
        else:
            return response.headers.get('Content-Type', "")

    def _fetch(self, url):
        if not re.search(r"^https?://", url):
            return
        started = time.monotonic()
        content_type = self._fetch_content_type(url)
        if not content_type.lower().startswith('text/html'):
            return
        try:
            with requests.get(url, headers=self.headers, timeout=self.timeout, stream=True) as response:
                # Check the content type again due to some servers claiming text/html for HEAD only, for example
                # some audio streams.
                content_type = response.headers.get("Content-Type", "").lower()
                if not response.ok or not content_type.startswith("text/html"):
                    return
                html = b""
                # Loop through the response until we either parse through the whole response,
                # or reach max bytes or max seconds.
                while len(html) < self.max_bytes:
                    if time.monotonic() - started > self.max_seconds:
                        logger.debug("_fetch - %s took too long, skipping", url)
                        return
                    # Read a part of the data, to avoid the remote server making us hang due to
                    # trickling data, like an audio stream.
                    data = response.raw.read1(16 * 1024, decode_content=True)
                    if not data:
                        break
                    html += data
                return html
        except RequestException as ex:
            logger.debug("_fetch - %s when fetching url %s", ex, url)
            return

    def _parse(self, html, parser):
        if not html:
            return self._data
        doc = BeautifulSoup(html, parser)
        ogs = doc.html.head.findAll(property=re.compile(r"^og"))

        for og in ogs:
            if og.has_attr("content"):
                self._data[og["property"][3:]] = og["content"]
