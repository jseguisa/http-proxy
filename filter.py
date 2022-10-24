#!/usr/bin/env python3

import json
import sys
import config

class JsonContentFilter:
    def filter_data(self, data_bytes, filter_data):
        try:
            json_data_dictionary = json.loads(data_bytes)

            if [] != filter_data:
                for filter_string in filter_data:
                    self.remove_entry(json_data_dictionary, filter_string)

            modified_json_data_dictionary = json.dumps(json_data_dictionary, indent=2)
            return bytes(modified_json_data_dictionary, 'utf-8')

        except json.JSONDecodeError as err:
            print('invalid JSON data', file=sys.stderr)
            return data_bytes

    def remove_entry(self, json_data_dict, filter_string):
        filter_tree = filter_string[1:].split('/')

        try:
            if 1 == len(filter_tree):
                del json_data_dict[filter_tree[0]]
                return

            filter_tree_head = filter_tree[0 : len(filter_tree) - 1]
            filter_tree_last = filter_tree[len(filter_tree) - 1]

            subtree = None
            multi_subtree = False

            for key in filter_tree_head:
                if '*' == key:
                    multi_subtree = True
                else:
                    if None == subtree:
                        subtree = json_data_dict[key]

                    else:
                        if not multi_subtree:
                            subtree = subtree[key]
                        else:
                            for subtree_ in subtree:
                                subtree_ = subtree_[key]

            if not multi_subtree:
                del subtree[filter_tree_last]
            else:
                for subtree_ in subtree:
                    del subtree_[filter_tree_last]

        except KeyError:
            print('Invalid filter string: ' + filter_string, file=sys.stderr)
            return

        except TypeError:
            print('Filter string not applicable: ' + filter_string, file=sys.stderr)
            return
