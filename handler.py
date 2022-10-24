#!/usr/bin/env python3

import sys
import config

from http.server import BaseHTTPRequestHandler
from http.client import HTTPConnection
from http import HTTPStatus

from datetime import datetime, timedelta


class HttpCachingRequestHandler(BaseHTTPRequestHandler):
    target_host = None
    target_port = None
    json_content_filter = None

    GET_request_dictionary = { '' : (), }

    def send_target_response(self, status, reason, headers, data):
        self.send_response(status, reason)
        for header, value in headers:
            self.send_header(header, value)
        self.end_headers()

        try:
            self.wfile.write(data)
        except BrokenPipeError as bp_error:
            print('Endpoint connection closed', file=sys.stderr)

    def cache_valid_data(self, request_type, status, reason, headers, data):
        if 'GET' == request_type and HTTPStatus.OK == status:
            self.GET_request_dictionary[self.path] = (datetime.now(), status, reason, headers, data)

    def is_content_json(self, headers):
        for key, value in headers:
            if ('Content-Type' == key) and ('json' in value):
                return True

        return False

    def update_headers(self, headers, data):
        new_headers = []

        for key, value in headers:
            if 'Content-Length' == key:
                new_headers.append((key, len(data)))
            else:
                new_headers.append((key, value))

        return new_headers

    def retrieve_and_sync_from_target(self, request_type, path):
        target_connection = HTTPConnection(self.target_host, self.target_port, 10)
        target_connection.request(request_type, path)
        target_response = target_connection.getresponse()

        status = target_response.status
        reason = target_response.reason
        headers = target_response.getheaders()
        data = target_response.read()

        if config.json_filter_enable and self.is_content_json(headers):
            for target_path, filter_data in config.json_filter_data:
                if target_path in path:
                    data = self.json_content_filter.filter_data(data, filter_data)
                    headers = self.update_headers(headers, data)
                    break

        print("Status: {} and reason: {}".format(status, reason), file=sys.stderr)

        self.send_target_response(status, reason, headers, data)
        target_connection.close()

        self.cache_valid_data(request_type, status, reason, headers, data)

    def do_GET(self):
        if self.path in self.GET_request_dictionary:
            timestamp, status, reason, headers, data = self.GET_request_dictionary[self.path]
            now = datetime.now()
            if timedelta(seconds=config.cache_duration) <= now - timestamp:
                print('Retrieving data from target, cached data timed out', file=sys.stderr)
                self.retrieve_and_sync_from_target('GET', self.path)
            else:
                print('Retrieving data from cache', file=sys.stderr)
                self.send_target_response(status, reason, headers, data)

        else:
            print('Retrieving data from target', file=sys.stderr)
            self.retrieve_and_sync_from_target('GET', self.path)

    def do_POST(self):
        self.retrieve_and_sync_from_target('POST', self.path)
