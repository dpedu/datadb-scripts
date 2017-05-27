#!/usr/bin/env python3

import os
import sys
import traceback
from urllib.parse import parse_qs as _parse_qs
from base64 import b64decode


def start_response(content_type="text/html", status_code=("200", "OK",), extra_headers=[]):
    print('Status: %s %s' % (status_code))
    print("Content-Type: %s" % content_type)
    for line in extra_headers:
        print(line)
    print()
    sys.stdout.flush()


def parse_qs():
    # Parse query string to GET dict
    GET = {}
    if "QUERY_STRING" in os.environ:
        GET = _parse_qs(os.environ["QUERY_STRING"])
        GET = {k: v[0] for k, v in GET.items()}
    return GET


class HTTPBasicAuth:
    username = None
    password = None

    def __str__(self):
        return "<HTTPBasicAuth object username='%s' password='%s'>" % (self.username, self.password)


def parse_auth():
    if "HTTP_AUTHORIZATION" in os.environ:
        authtype, value = os.environ["HTTP_AUTHORIZATION"].split(' ')
        if authtype == "Basic":
            auth = HTTPBasicAuth()
            auth.username, auth.password = b64decode(value).decode().split(":")
            return auth

# cgi.print_environ()
