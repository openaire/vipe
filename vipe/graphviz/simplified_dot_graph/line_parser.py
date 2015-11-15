# Copyright 2013-2015 University of Warsaw
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = "Mateusz Kobos mkobos@icm.edu.pl"

import re

from vipe.graphviz.simplified_dot_graph.connection import Connection

class LineParser:
    __node_pattern = re.compile(r'\s*"(?P<node>[\w-]+)"\s*\[.*')
    __connection_pattern = re.compile(\
            r'"(?P<start_node>[\w-]+)"(:"(?P<start_port>[\w-]+)")?\s*->\s*'\
            r'"(?P<end_node>[\w-]+)"(:"(?P<end_port>[\w-]+)")?.*')
    
    @staticmethod
    def parse_connection(line):
        match = LineParser.__connection_pattern.match(line)
        if match is None:
            return None
        return Connection(match.group('start_node'), match.group('start_port'),
                          match.group('end_node'), match.group('end_port'))
    
    @staticmethod
    def parse_node(line):
        match = LineParser.__node_pattern.match(line)
        if match is None:
            return None
        return match.group('node')