#!/usr/bin/env python3

from http.server import ThreadingHTTPServer

from handler import HttpCachingRequestHandler
from filter import JsonContentFilter

import os
import sys
import ssl
import config

def main():
    host = '0.0.0.0'
    port = 443

    target_host = os.environ['TARGET_HOST']
    target_port = os.environ['TARGET_PORT']

    cert_file = config.server_cert_file
    key_file = config.server_key_file

    HttpCachingRequestHandler.target_host = target_host
    HttpCachingRequestHandler.target_port = target_port
    HttpCachingRequestHandler.json_content_filter = JsonContentFilter()

    web_server = ThreadingHTTPServer((host, port), HttpCachingRequestHandler)
    web_server.socket = ssl.wrap_socket(web_server.socket, keyfile=key_file, certfile=cert_file, server_side=True)

    print("Server started http://%s:%s" % (host, port), file=sys.stderr)

    try:
        web_server.serve_forever()
    except:
        web_server.server_close()

if __name__ == '__main__':
    main()
