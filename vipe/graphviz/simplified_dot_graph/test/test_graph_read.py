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

from vipe.common.utils import read_as_string
from vipe.graphviz.simplified_dot_graph.graph import SimplifiedDotGraph
from vipe.graphviz.simplified_dot_graph.connection import Connection

def test_simple():
    check('data/simple.dot', create_simple_graph())

def test_no_digraph_wrapping():
    check('data/no_digraph_wrapping.dot', create_simple_graph())

def test_nodes_not_defined_explicitly():
    check('data/nodes_not_defined_explicitly.dot', create_simple_graph())

def test_html_node():
    check('data/html_node.dot', SimplifiedDotGraph(
            {'node1', 'node2'},
            {Connection('node1', None, 'node2', None)}))

def create_simple_graph():
    return SimplifiedDotGraph(
            {'node1', 'node2', 'node3'},
            {Connection('node1', 'p1', 'node2', 'p21'),
             Connection('node3', 'p3', 'node2', 'p23'),
             Connection('node2', None, 'node3', None),
             Connection('node2', 'p2', 'node1', None)})
    

def check(relative_input_path, expected_graph):
    input_dot = read_as_string(__name__, relative_input_path)
    actual_graph = SimplifiedDotGraph.from_dot(input_dot)
    assert expected_graph == actual_graph, \
        '{} != {}'.format(expected_graph, actual_graph)