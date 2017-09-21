import socket
import requests


class BaseChecker(object):
    """Base interface for a checker."""
    def __init__(self, category, name):
        self.category = category
        self.name = name

    def check_availability(self, target):
        """Checks the availability of the given target. Returns
        True if the target is available, false otherwise. """
        raise NotImplementedError()


class HTTPChecker(BaseChecker):
    """Checker which tries to access a URL via HTTPS."""
    def __init__(self, category, name, url):
        super(HTTPChecker, self).__init__(category, name)
        self.url = url

    def check_availability(self, target):
        with requests.get(self.url % target) as r:
            if not r.ok:
                return True
            return False


class DNSChecker(BaseChecker):
    """Checker which tries to access a hsot via DNS."""
    def __init__(self, category, name, host):
        super(DNSChecker, self).__init__(category, name)
        self.host = host

    def check_availability(self, target):
        self.name = self.host % target
        try:
            socket.gethostbyname(self.host % target)
            return False
        except socket.gaierror:
            return True


GTLDS = ['ac', 'ad', 'ae', 'aero', 'af', 'ag', 'ai', 'al', 'am', 'an', 'ao',
         'aq', 'ar', 'arpa', 'as', 'asia', 'at', 'au', 'aw', 'ax', 'az', 'ba',
         'bb', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'biz', 'bj', 'bl', 'bm',
         'bn', 'bo', 'bq', 'br', 'bs', 'bt', 'bv', 'bw', 'by', 'bz', 'ca',
         'cat', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn',
         'co', 'com', 'coop', 'cr', 'cs', 'cu', 'cv', 'cw', 'cx', 'cy', 'cz',
         'dd', 'de', 'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'edu', 'ee', 'eg',
         'eh', 'er', 'es', 'et', 'eu', 'fi', 'fj', 'fk', 'fm', 'fo', 'fr',
         'ga', 'gb', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gn',
         'gov', 'gp', 'gq', 'gr', 'gs', 'gt', 'gu', 'gw', 'gy', 'hk', 'hm',
         'hn', 'hr', 'ht', 'hu', 'id', 'ie', 'il', 'im', 'in', 'info', 'int',
         'io', 'iq', 'ir', 'is', 'it', 'je', 'jm', 'jo', 'jobs', 'jp', 'ke',
         'kg', 'kh', 'ki', 'km', 'kn', 'kp', 'kr', 'kw', 'ky', 'kz', 'la',
         'lb', 'lc', 'li', 'lk', 'local', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly',
         'ma', 'mc', 'md', 'me', 'mf', 'mg', 'mh', 'mil', 'mk', 'ml', 'mm',
         'mn', 'mo', 'mobi', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'museum',
         'mv', 'mw', 'mx', 'my', 'mz', 'na', 'name', 'nato', 'nc', 'ne',
         'net', 'nf', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nu', 'nz', 'om',
         'onion', 'org', 'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl', 'pm',
         'pn', 'pr', 'pro', 'ps', 'pt', 'pw', 'py', 'qa', 're', 'ro', 'rs',
         'ru', 'rw', 'sa', 'sb', 'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sj',
         'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'ss', 'st', 'su', 'sv', 'sx',
         'sy', 'sz', 'tc', 'td', 'tel', 'tf', 'tg', 'th', 'tj', 'tk', 'tl',
         'tm', 'tn', 'to', 'tp', 'tr', 'travel', 'tt', 'tv', 'tw', 'tz', 'ua',
         'ug', 'uk', 'um', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi',
         'vn', 'vu', 'wf', 'ws', 'xxx', 'ye', 'yt', 'yu', 'za', 'zm', 'zr',
         'zw']


class ShorteningChecker(BaseChecker):
    """Checker which attempts to use the last few characters
    of the target to create a shortened URL."""
    def __init__(self, category, name):
        super(ShorteningChecker, self).__init__(category, name)

    def check_availability(self, target):
        for gtld in GTLDS:
            if target.endswith(gtld):
                break
        else:
            return False
        self.name = target[:-len(gtld)] + '.' + gtld
        try:
            socket.gethostbyname(self.name)
            return False
        except socket.gaierror:
            return True


ALL_CHECKERS = []


# Social Media Checkers
for _args in [('twitter', 'https://twitter.com/%s'),
              ('tumblr', 'https://%s.tumblr.com'),
              ('mastodon.social', 'https://mastodon.social/@%s'),
              ('dribble', 'https://dribbble.com/%s')]:
    ALL_CHECKERS.append(HTTPChecker('social', _args[0], _args[1]))

# Developer Checkers
for _args in [('github', 'https://github.com/%s'),
              ('gitlab', 'https://gitlab.com/%s'),
              ('bitbucket', 'https://bitbucket.com/%s'),
              ('dockerhub', 'https://hub.docker.com/u/%s')]:
    ALL_CHECKERS.append(HTTPChecker('dev', _args[0], _args[1]))

# Package Management Checkers
for _args in [('pypi', 'https://pypi.python.org/pypi/%s'),
              ('npm', 'https://www.npmjs.com/package/%s'),
              ('cargo', 'https://crates.io/crates/%s'),
              ('rubygems', 'https://rubygems.org/gems/%s')]:
    ALL_CHECKERS.append(HTTPChecker('package', _args[0], _args[1]))

# Websites
for ext in ['.com', '.net', '.org', '.io', '.me']:
    ALL_CHECKERS.append(DNSChecker('web', '*' + ext, '%s' + ext))

ALL_CHECKERS.append(ShorteningChecker('web', 'shorten'))
