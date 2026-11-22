from unittest.mock import patch

import pytest
import requests_mock
from requests import Timeout

from opengraph import OpenGraph
from opengraph.opengraph import USER_AGENT, logger

DEFAULT_HEADERS = {"user-agent": USER_AGENT}
URL = "https://example.org"
HTML = {"Content-Type": "text/html; charset=utf-8"}


class TestOpenGraph:
    def test__fetch(self, document):
        with requests_mock.Mocker() as m:
            m.head(URL, headers=HTML)
            m.get(URL, text=document, headers=HTML)
            og = OpenGraph(url=URL)
        assert og.title == "Test title"

    def test__fetch__only_http_protocols(self, document):
        with requests_mock.Mocker() as m:
            m.head("http://foo.bar", headers=HTML)
            m.get("http://foo.bar", text=document, headers=HTML)
            assert OpenGraph(url="http://foo.bar")._data != {}
            m.head("https://foo.bar", headers=HTML)
            m.get("https://foo.bar", text=document, headers=HTML)
            assert OpenGraph(url="https://foo.bar")._data != {}
            m.get("mailto:jay@foo.bar", text=document)
            assert OpenGraph(url="mailto:jay@foo.bar")._data == {}
            m.get("ftp://foo.bar", text=document)
            assert OpenGraph(url="ftp://foo.bar")._data == {}

    def test__fetch__content_type__html_fetched(self, document):
        with requests_mock.Mocker() as m:
            m.head(URL, headers=HTML)
            m.get(URL, text=document, headers=HTML)
            og = OpenGraph(url=URL)
        assert og.title == "Test title"

    def test__fetch__content_type__non_html_skipped(self, document):
        with requests_mock.Mocker() as m:
            m.head(URL, headers=HTML)
            m.get(URL, text=document, headers={'Content-Type': 'video/mp4'})
            og = OpenGraph(url=URL)
        assert og._data == {}

    def test__fetch__head_and_get_content_type_differ(self, document):
        # Some servers, like audio streams, return text/html on HEAD and then stream audio on GET
        with requests_mock.Mocker() as m:
            m.head(URL, headers=HTML)
            m.get(URL, text=document, headers={'Content-Type': 'audio/mpeg'})
            og = OpenGraph(url=URL)
        assert og._data == {}

    def test__fetch__error_response_skipped(self, document):
        with requests_mock.Mocker() as m:
            m.head(URL, headers=HTML)
            m.get(URL, text=document, status_code=404, headers={'Content-Type': 'text/html'})
            og = OpenGraph(url=URL)
        assert og._data == {}

    def test__fetch__max_bytes(self, document):
        og = OpenGraph(html=document, max_bytes=20 * 1024)
        with requests_mock.Mocker() as m:
            m.head(URL, headers=HTML)
            m.get(URL, content=b"x" * 100 * 1024, headers={'Content-Type': 'text/html'})
            html = og._fetch(URL)
        assert 20 * 1024 <= len(html) < 100 * 1024

    @patch("opengraph.opengraph.time.monotonic", side_effect=[0, 1, 1000])
    def test__fetch__max_seconds(self, mock_monotonic, document):
        with requests_mock.Mocker() as m:
            m.head(URL, headers=HTML)
            m.get(URL, text=document * 10000, headers={'Content-Type': 'text/html'})
            assert OpenGraph(url=URL)._data == {}

    def test_contains(self, document):
        og = OpenGraph(html=document)
        assert "title" in og

    def test_get_attr(self, document):
        og = OpenGraph(html=document)
        assert og.title == "Test title"
        with pytest.raises(AttributeError):
            # noinspection PyStatementEffect
            og.attribute_does_not_exist

    @patch("opengraph.opengraph.requests.get", side_effect=Timeout)
    @patch("opengraph.opengraph.requests.head")
    @patch.object(logger, "debug", autospec=True)
    def test_returns_none_on_get_exception(self, mock_logger, mock_head, mock_get):
        mock_head.return_value.headers = HTML
        assert OpenGraph(url=URL)._data == {}
        assert mock_logger.called

    def test_str_repr(self, document):
        og = OpenGraph(html=document)
        text_of_data = og._data.__str__()
        assert str(og) ==  text_of_data

    @patch("opengraph.opengraph.BeautifulSoup", autospec=True)
    def test_uses_right_parser(self, mock_bs, document):
        try:
            OpenGraph(html=document)
        except AttributeError:
            pass
        mock_bs.assert_called_once_with(document, "html.parser")
        mock_bs.reset_mock()
        try:
            OpenGraph(html=document, parser="spam")
        except AttributeError:
            pass
        mock_bs.assert_called_once_with(document, "spam")

    @patch("opengraph.opengraph.requests.get")
    @patch("opengraph.opengraph.requests.head")
    def test_uses_timeout(self, mock_head, mock_get):
        mock_head.return_value.headers = HTML
        # A failed response, so _fetch returns right after the request
        mock_get.return_value.__enter__.return_value.ok = False
        OpenGraph(url=URL)
        mock_head.assert_called_once_with(URL, headers=DEFAULT_HEADERS, timeout=10)
        mock_get.assert_called_once_with(URL, headers=DEFAULT_HEADERS, timeout=10, stream=True)
        mock_head.reset_mock()
        mock_get.reset_mock()
        OpenGraph(url=URL, timeout=(5, 10))
        mock_head.assert_called_once_with(URL, headers=DEFAULT_HEADERS, timeout=(5, 10))
        mock_get.assert_called_once_with(URL, headers=DEFAULT_HEADERS, timeout=(5, 10), stream=True)
