#!/usr/bin/env python

import bs4, crayons, httpx, os, packaging.version, re, requests, string, sys
import urllib.parse, urllib.request

from pbs.version import InvalidVersion, Version

import pbs

def retrieve_url(url):
    headers = {
        'User-Agent': pbs.USER_AGENT
    }

    scheme, *_ = urllib.parse.urlparse(url)

    if scheme == 'http' or scheme == 'https':
        response = requests.get(url, headers = headers)
        if not response.ok:
            raise Exception('failed to get %s' % url)

        content = response.content
    else:
        response = urllib.request.urlopen(url)
        content = response.read()

    if 'Content-Type' in response.headers:
        content_type = response.headers['Content-Type'].split(';')[0].strip()
    else:
        content_type = 'text/plain'

    return content, content_type

class Client(httpx.Client):
    def __init__(self, base_url):
        headers = {
            'User-Agent': pbs.USER_AGENT
        }
        transport = None

        try:
            import hishel, hishel.httpx

            headers['Cache-Control'] = 'max-age=3600'

            storage = hishel.SyncSqliteStorage(database_path = pbs.srctree / '.cache')
            transport = httpx.HTTPTransport()
            transport = hishel.httpx.SyncCacheTransport(next_transport = transport,
                                                        storage = storage)
        except Exception as e:
            raise e

        self.client = httpx.Client(base_url = base_url, headers = headers,
                                   transport = transport)

    def get(self, *args, **kwargs):
        return self.client.get(*args, **kwargs)

class PackageWatcher:
    DEFAULT_KEYWORDS = {
            'version': r'((?:\d+)(?:\.\d+)*(?:[\w-]*))',
            '_version': r'((?:\d+)(?:_\d+)*)',
            'version_': r'(?:(?:\d+)(?:_\d+)*)',
            'major': r'(?:\d+)',
            'minor': r'(?:\d+)',
            'micro': r'(?:\d+)',
            'patch': r'(?:\d+)'
        }

    def __init__(self, url, *, keywords = None, pattern = None):
        self.url = url
        self.pattern = pattern
        self.keywords = keywords or PackageWatcher.DEFAULT_KEYWORDS

    @staticmethod
    def open(url, keywords = None):
        for watcher in [ IgnoreWatcher, AnityaWatcher ]:
            if watcher.match(url):
                return watcher(url, keywords = keywords)

        raise Exception('no watchers for URL %s' % url)

class IndexWatcher(PackageWatcher):
    def __init__(self, url, *, keywords = None, pattern = None):
        super().__init__(url, keywords = keywords, pattern = pattern)

    @staticmethod
    def match(url):
        return True

    def watch(self, *, prerelease = False, verbose = False):
        result = []

        if verbose:
            print('trying pattern:', self.pattern)

        # use only the filename part of the URL to match, which is useful if
        # the download location differs from the one specified in the index
        # page (different mirror, or github/gitlab instance)
        pattern = self.pattern.split('/')[-1]

        scheme, *_ = urllib.parse.urlparse(self.url)
        template = string.Template(pattern)
        regex = template.substitute(self.keywords)
        # anchor regex at the end
        regex = re.compile(regex + '$')

        content, content_type = retrieve_url(self.url)

        if verbose:
            print('Content-Type:', content_type)

        if content_type == 'text/html':
            soup = bs4.BeautifulSoup(content, 'html.parser')
            links = soup.find_all('a', attrs = { 'href': regex })

            for link in links:
                if verbose:
                    print('link:', link['href'])

                link = link['href'].split('/')[-1]

                match = regex.match(link)
                if match:
                    match = match.group(match.lastindex)

                    if match not in result:
                        result.append(match)
        else:
            print('%s: unknown content: %s' % (crayons.red('ERROR', bold = True),
                                               content_type))

        versions = []

        for version in result:
            try:
                version = Version(version)

                # do not consider prerelease versions unless explicitly requested
                if prerelease or not version.is_prerelease:
                    versions.append(version)
            except InvalidVersion as e:
                print('%s: failed to parse version: %s' % (crayons.red('ERROR', bold = True), e))

        return sorted(versions, reverse = True)

class IgnoreWatcher(PackageWatcher):
    def __init__(self, url, *, keywords = None, pattern = None):
        super().__init__(url, keywords = keywords, pattern = pattern)

    @staticmethod
    def match(url):
        return url == 'ignore://'

    def watch(self, *, prerelease = False, verbose = False):
        return None

class AnityaWatcher(PackageWatcher):
    REGEX = re.compile(r'https://release-monitoring\.org/api/v2/versions/\?project_id=(.*)')
    REGEX_SHORT = re.compile(r'anitya://(.*)')
    BASE_URL = 'https://release-monitoring.org/api/v2/versions/'

    def __init__(self, url, *, keywords = None, pattern = None):
        super().__init__(url, keywords = keywords, pattern = pattern)

    @staticmethod
    def match(url):
        match = AnityaWatcher.REGEX.match(url)

        if not match:
            match = AnityaWatcher.REGEX_SHORT.match(url)

        return match is not None

    def watch(self, *, prerelease = False, verbose = False):
        result = []

        match = AnityaWatcher.REGEX.match(self.url)

        if not match:
            match = AnityaWatcher.REGEX_SHORT.match(self.url)

        if not match:
            raise Exception(f'failed to find a match for URL: {self.url}')

        project = match.group(1)

        response = httpx.get('https://release-monitoring.org/api/v2/versions/',
                             params = { 'project_id': project })
        response.raise_for_status()

        project = response.json()

        if not prerelease:
            releases = project['stable_versions']
        else:
            releases = project['versions']

        versions = []

        for release in releases:
            try:
                version = Version(release)
                versions.append(version)
            except InvalidVersion:
                # ignore versions that cannot be parsed
                pass

        return versions
