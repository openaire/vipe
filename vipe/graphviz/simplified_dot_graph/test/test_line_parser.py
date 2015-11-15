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

from vipe.graphviz.simplified_dot_graph.line_parser import LineParser
from vipe.graphviz.simplified_dot_graph.connection import Connection

def test_node_simple():
    check_node('"citation_matching" [label="cit"]', 'citation_matching')

def test_node_with_hyphen():
    check_node('"citation-matching-node" [label=""]', 'citation-matching-node')

def test_node_extended():
    check_node('"citationmatching_chain" [label="" fillcolor=cyan,style=filled shape=box fixedsize=true width=0.1 height=0.1]',
               'citationmatching_chain')
    check_node('"citationmatching_chain"[label="" fillcolor=cyan,style=filled shape=box fixedsize=true width=0.1 height=0.1]',
               'citationmatching_chain')

def test_node_wrong_line():
    check_node('"node1" -> "node2"', None)
    check_node('"node1":"port1" -> "node2":"port2"', None)
    check_node('"node1" -> "node2" [label="something"]', None)
    check_node('      <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">', None)
    check_node('digraph {', None)
    check_node('rankdir=LR', None)

def test_connection_simple():
    check_connection('"node1" -> "node2"', 
               Connection('node1', None, 'node2', None))
    check_connection('"node1":"port1" -> "node2":"port2"', 
               Connection('node1', 'port1', 'node2', 'port2'))
    check_connection('"node1" -> "node2" [label="something"]', 
               Connection('node1', None, 'node2', None))
    check_connection('"node1"  ->\t"node2" [label="something"]', 
               Connection('node1', None, 'node2', None))

def test_connection_mixed_ports():
    check_connection('"node1":"document" -> "node2"', 
               Connection('node1', 'document', 'node2', None))
    check_connection('"node1" -> "node2":"document"', 
               Connection('node1', None, 'node2', 'document'))

def test_connection_with_hyphen():
    check_connection('"node-1" -> "my-node_here":"port-1"', 
                     Connection('node-1', None, 'my-node_here', 'port-1'))

def test_connection_wrong_line():
    check_connection('"citation_matching" [label="cit"]', None)
    check_connection('"citationmatching_chain" [label="" fillcolor=cyan,style=filled shape=box fixedsize=true width=0.1 height=0.1]', None)
    check_connection('"citationmatching_chain"[label="" fillcolor=cyan]', None)
    check_connection('digraph {', None)
    check_connection('rankdir=LR', None)

def check_node(line, expected_node):
    actual_node = LineParser.parse_node(line)
    if expected_node is None:
        assert actual_node is None
    else:
        assert expected_node == actual_node

def check_connection(line, expected_connection):
    actual_connection = LineParser.parse_connection(line)
    if expected_connection is None:
        assert actual_connection is None
    else:
        assert expected_connection == actual_connection, \
            '{} != {}'.format(expected_connection, actual_connection)