#!/usr/bin/env python

import bs4, crayons, os, packaging.version, re, requests, string, sys
import urllib.parse, urllib.request

from packaging.version import Version

import pbs

def retrieve_url(url):
    headers = {
        'User-Agent': f'Platform Build System/{pbs.VERSION}'
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

class PackageWatcher:
    DEFAULT_KEYWORDS = {
            'version': '((?:\d+)(?:\.\d+)*)',
            '_version': '((?:\d+)(?:_\d+)*)',
            'version_': '(?:(?:\d+)(?:_\d+)*)',
            'major': '(?:\d+)',
            'minor': '(?:\d+)',
            'micro': '(?:\d+)',
            'patch': '(?:\d+)'
        }

    def __init__(self, url, *, keywords = None, pattern = None):
        self.url = url
        self.pattern = pattern
        self.keywords = keywords or PackageWatcher.DEFAULT_KEYWORDS

    @staticmethod
    def open(url, keywords = None):
        for watcher in [ GitHubWatcher, GitLabWatcher, PypiWatcher,
                         ListingWatcher ]:
            if watcher.match(url):
                return watcher(url, keywords = keywords)

        raise Exception('no watchers for URL %s' % url)

class IndexWatcher(PackageWatcher):
    def __init__(self, url, *, keywords = None, pattern = None):
        super().__init__(url, keywords = keywords, pattern = pattern)

    @staticmethod
    def match(url):
        return True

    def watch(self, verbose = False):
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
                versions.append(Version(version))
            except packaging.version.InvalidVersion as e:
                print('%s: failed to parse version: %s' % (crayons.red('ERROR', bold = True), e))

        return sorted(versions, reverse = True)

class ListingWatcher(PackageWatcher):
    def __init__(self, url, *, keywords = None, pattern = None):
        super().__init__(url, keywords = keywords, pattern = pattern)

    @staticmethod
    def match(url):
        return True

    def escape(self, s):
        special_chars = { c: '\\' + chr(c) for c in b'+' }

        # split up a string into the static and regex parts
        static, *regex = s.split('(', 1)

        # replace all special characters in the static part
        static = static.translate(special_chars)

        return '('.join([static, *regex])

    def resolve(self, base, component, verbose = False):
        result = []

        scheme, *_ = urllib.parse.urlparse(base)
        component = self.escape(component)
        regex = re.compile(component)

        try:
            content, content_type = retrieve_url(base)
        except Exception as e:
            if verbose:
                print('ERROR: failed to get %s: %s' % (base, e))

            return result

        def decode_match(href):
            return href and regex.search(urllib.parse.unquote(href))

        if content_type == 'text/html':
            soup = bs4.BeautifulSoup(content, 'html.parser')
            links = soup.find_all('a', href = decode_match)

            for link in links:
                href = urllib.parse.unquote(link['href'])

                if verbose:
                    print('link:', href)

                match = regex.search(href)
                if match:
                    if verbose:
                        print('  match:', match)
                        print('    groups:', match.groups())
                        print('    version:', '.'.join(match.groups()[1:]))

                    match = match.group(0)

                    if match not in result:
                        result.append(match)
                else:
                    print('  no match for %s' % regex)
        else:
            for line in content.splitlines():
                line = line.strip().decode()

                if verbose:
                    print(scheme, '>', line)

                if scheme == 'ftp':
                    line = line.split(None, 8)[-1]

                if verbose:
                    print('line:', line, 'regex:', regex)

                match = regex.search(line)
                if match:
                    if verbose:
                        print('  match:', match)
                        print('    groups:', match.groups())
                        print('    version:', '.'.join(match.groups()[1:]))

                    match = match.group(0)

                    if match not in result:
                        result.append(match)

        return result

    def watch(self, verbose = False):
        result = []

        # split up the URL so that the path can be extracted
        (scheme, netloc, path, *unused) = urllib.parse.urlparse(self.url)
        (params, query, fragment) = unused

        if verbose:
            print('path:', path)

        # initialize with the base URL
        urls = [ scheme + '://' + netloc ]
        base = ''

        # iterate over all path components
        while path:
            component, sep, path = path.partition('/')

            # replace any keywords with corresponding regular expressions
            template = string.Template(component)
            component = template.substitute(self.keywords)
            bases = []

            if verbose:
                print('checking part:', component)

            for base in urls:
                # if the component contains a regular expression, return all
                # matching links
                if re.findall('\(.*\)', component):
                    matches = self.resolve(base, component, verbose)

                    for match in matches:
                        bases.append(base + match + sep)
                else:
                    bases.append(base + component + sep)

            urls = bases

        # The regular expression for the URL earlier was not escaped to allow
        # the path to be properly split up into individual components and one
        # component after the other was escaped for matching. For the final
        # match we now need to escape the whole URL.
        template = string.Template(self.escape(self.url))
        regex = template.substitute(self.keywords)

        for url in urls:
            match = re.match(regex, url)
            if match:
                if verbose:
                    print('match:', match)
                    print('  groups:', match.groups())

                groups = match.groupdict()
                if 'version' not in groups:
                    if match.lastindex:
                        last = [ match.group(match.lastindex) ]
                        index = match.lastindex
                    else:
                        index = 1

                    for version in last + [ '.'.join(match.groups()[index:]) ]:
                        try:
                            _ = Version(version)
                            break
                        except packaging.version.InvalidVersion as e:
                            continue
                else:
                    version = groups['version']

                if not version in result:
                    result.append(version)

        versions = []

        for version in result:
            try:
                versions.append(Version(version))
            except packaging.version.InvalidVersion as e:
                print('%s: failed to parse version: %s' % (crayons.red('ERROR', bold = True), e))

        return sorted(versions, reverse = True)

class GitHubWatcher(PackageWatcher):
    REGEX = re.compile(r'https?://github.com/([^/]*)/([^/]*)/(.*)')

    def __init__(self, url, *, keywords = None, pattern = None):
        super().__init__(url, keywords = keywords, pattern = pattern)

    @staticmethod
    def match(url):
        match = GitHubWatcher.REGEX.match(url)

        return match is not None

    def watch(self, verbose = False):
        result = []

        if verbose:
            print('watching GitHub URL: %s...' % self.url)

        match = GitHubWatcher.REGEX.match(self.url)
        if match:
            project = '/'.join([ match.group(1), match.group(2) ])

            if verbose:
                print('  project:', project)

        parts = urllib.parse.urlparse(self.url)
        template = string.Template(parts.path)
        path = template.substitute(self.keywords)
        sections = parts.path.split('/')[3:5]

        if verbose:
            print('  path: %s' % '/'.join(sections))

        if sections[0] == 'releases' and sections[1] == 'download':
            if not self.pattern:
                # find the tag version pattern
                pattern = path.split('/')[5]
            else:
                pattern = self.pattern

            tags = parts._replace(path = '/'.join([ project, 'releases' ]))
            url = tags.geturl()
        elif sections[0] == 'archive':
            pattern = path.split('/')[-1]

            if not self.pattern:
                if not pattern.startswith('v'):
                    pattern = 'v?' + pattern
            else:
                pattern = self.pattern

            tags = parts._replace(path = '/'.join([ project, 'tags' ]))
            url = tags.geturl()
        else:
            print('%s: unknown path: %s' % (crayons.red('ERROR', bold = True),
                                            '/'.join(sections)))
            return []

        if not self.pattern:
            # strip off the tarball extension
            pattern = pattern.split('.tar')[0]
            # and anchor regex at the end
            pattern = pattern + '$'

        regex = re.compile(pattern)

        if verbose:
            print('listing tags from %s (regex: %s)' % (url, regex))

        response = requests.get(url)
        if not response.ok:
            raise Exception('failed to get %s' % url)

        html = bs4.BeautifulSoup(response.content, 'html.parser')
        releases = html.find_all('div', attrs = {
                'data-test-selector':
                    lambda selector: selector and
                                     selector in [ 'tag-info-container',
                                                   'release-card' ]
            })

        for release in releases:
            links = release.find_all('a', attrs = {
                    'data-view-component': 'true',
                    'class': 'Link--primary',
                })
            for link in links:
                if verbose:
                    print('link:', link)
                    print('  regex:', regex)

                match = regex.search(link['href'])
                if not match:
                    continue

                if verbose:
                    print('  match:', match)
                    print('    lastindex:', match.lastindex)
                    print('    groups:', match.groups())

                if match.lastindex:
                    last = [ match.group(match.lastindex),
                             match.group(match.lastindex).replace('_', '.') ]
                else:
                    last = []

                # First, try the full match and if that doesn't yield a valid
                # version number (libexpat and some other packages use under-
                # scores as delimiter, rather than the regular period), try
                # to construct one by joining the individual version parts
                # (e.g. major, minor and patch). If that also fails, try one
                # more time using the release description.
                for version in last + [ '.'.join(match.groups()[1:]),
                                        link.string ]:
                    try:
                        version = Version(version)
                        break
                    except packaging.version.InvalidVersion as e:
                        #print('ERROR:', e)
                        pass
                else:
                    continue

                if not version in result:
                    result.append(version)

        return sorted(result, reverse = True)

class GitLabWatcher(PackageWatcher):
    REGEX = re.compile(r'https?://gitlab\.([^/]+)/([^/]+)/([^/]+)/(.*)')

    def __init__(self, url, *, keywords = None, pattern = None):
        super().__init__(url, keywords = keywords, pattern = pattern)

    @staticmethod
    def match(url):
        match = GitLabWatcher.REGEX.match(url)

        return match is not None

    def watch(self, verbose = False):
        result = []

        if verbose:
            print('watching GitLab URL: %s...' % self.url)

        match = GitLabWatcher.REGEX.match(self.url)
        if match:
            domain = match.group(1)
            project = '/'.join([ match.group(2), match.group(3) ])

            if verbose:
                print('  domain:', domain)
                print('  project:', project)

        parts = urllib.parse.urlparse(self.url)
        template = string.Template(parts.path)
        path = template.substitute(self.keywords)
        sections = path.split('/')[3:5]

        if verbose:
            print('  path: %s' % '/'.join(sections))

        if sections[0] == '-' and sections[1] in [ 'archive', 'releases' ]:
            if sections[1] == 'archive':
                regex = '/'.join(path.split('/')[:-1])

            if sections[1] == 'releases':
                regex = '/'.join(path.split('/')[:-2])
        else:
            print('%s: unknown path: %s' % (crayons.red('ERROR', bold = True),
                                            '/'.join(sections)))
            return []

        url = parts._replace(path = project + '/-/tags').geturl()

        if verbose:
            print('listing tags from %s (regex: %s)' % (url, regex))

        response = requests.get(url)
        if not response.ok:
            raise Exception('failed to get %s' % url)

        regex = re.compile(regex)

        html = bs4.BeautifulSoup(response.content, 'html.parser')
        links = html.find_all('a', href = regex)

        for link in links:
            href = link['href']

            # for archive links, strip the filename part before matching
            if sections[1] == 'archive':
                href = '/'.join(href.split('/')[:-1])

            match = regex.match(href)
            if match:
                match = match.group(match.lastindex)

            try:
                match = Version(match)

                if not match in result:
                    result.append(match)
            except:
                print('%s: failed to parse %s' % (crayons.red('ERROR', bold = True),
                                                  crayons.red(match, bold = True)))

        return sorted(result, reverse = True)

class PypiWatcher(PackageWatcher):
    REGEX = re.compile(r'https?://pypi.python.org/packages/source/([^/]*)/([^/]*)/(.*)')

    def __init__(self, url, *, keywords = None, pattern = None):
        super().__init__(url, keywords = keywords, pattern = pattern)

    @staticmethod
    def match(url):
        match = PypiWatcher.REGEX.match(url)

        return match is not None

    def watch(self, verbose = False):
        result = []

        match = PypiWatcher.REGEX.match(self.url)
        if match:
            project = match.group(2)

        template = string.Template(self.url)
        regex = template.substitute(self.keywords)

        url = 'https://pypi.org/project/%s' % project
        response = requests.get(url)
        if not response.ok:
            raise Exception('failed to get %s' % url)

        release = re.compile(r'release--latest')

        html = bs4.BeautifulSoup(response.content, 'html.parser')
        timeline = html.find('div', attrs = { 'class': 'release-timeline' })
        releases = timeline.find_all('div', attrs = { 'class': 'release' })

        for release in releases:
            version = release.find('p', attrs = { 'class': 'release__version' })

            # only look at the first string to avoid content from sub-tags
            # such as "pre-release"
            for content in version.stripped_strings:
                result.append(Version(content))
                break

        return sorted(result, reverse = True)

