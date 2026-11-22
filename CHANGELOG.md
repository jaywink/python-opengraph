# Changelog

## Unreleased

### Changed

* Better protection against hanging forever while fetching some urls which stream data.

## 0.2.1 (2021-11-14)

### Changed

* Feed BeautifulSoup the request raw content to give it a chance to figure out the proper character encoding.

## 0.2.0 (2018-03-20)

### Changed

* Before fetching remote document for extracting tags, a HEAD request is now made to check the content type of the document. Anything that is not `text/html` is then skipped.

## 0.1.1 (2018-03-18)

### Changed

* A failed fetch due to network errors (for example timeout) now do a `debug` level logger instead of `warning` like before.

## 0.1.0 (2017-10-14)

### Added

* Use a default user agent if none given.
* Allow passing a `timeout` that will be used with `requests.get`.

  A default timeout of 10 seconds will be used if a timeout is not passed in.

### Changed

* No longer fetch other URL's than "http" and "https" protocols.
* Catch exceptions raised by `requests.get`.

  On an exception, return an empty result and log with warning level to the logger `opengraph`.

## 0.0.3 (2017-10-12)

Released to PyPi under the name `python-opengraph-jaywink`.

### Added

* `OpenGraph` now allows passing in a `parser` argument, which defaults to `html.parser`.

  A valid `parser` is anything `BeautifulSoup` supports, for example `lxml` or `html5lib`. You must have the right parser installed when calling `OpenGraph`, except the default `html.parser` which is built-in to Python.

### Fixed

* `OpenGraph` no longer "remembers" old OG tags from previous class instances.

  Data dictionary has been moved from class to instance attributes to ensure clean data is available every time the class is used.

## 0.0.2 (2015-06-14)

First release on Pypi as `python-opengraph` with basic OG tags parsing.
