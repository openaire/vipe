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

from vipe.common.utils import default_eq
from vipe.graphviz.simplified_dot_graph.line_parser import LineParser

class SimplifiedDotGraph:
    """Simplified representation of a graph defined in dot file.
    
    This corresponds to a subset of most important things defined in a
    dot file following certain conventions. 
    See docstring of `from_dot()` function for more details."""
    
    def __init__(self, nodes, connections):
        """Args:
            nodes (Set[string]): set of all nodes defined in the graph.
            connections (Set[Connection]): set of all connections in the graph.
        """
        self.nodes = nodes
        self.connections = connections

    @staticmethod
    def from_dot(dot_string):
        """Read graph from a string defining a graph in a simplified dot format.
    
        Args:
            dot_string (string): description of the graph in a simplified
                version of dot format. Among other things, the graph definition
                doesn't have to be surrounded by `digraph{ ... }` and available
                ports of a node don't have to be specified explicitly in the
                definition of the node.
    
        Return:
            SimplifiedDotGraph
        """
        nodes = set()
        connections = set()
        for line in dot_string.split('\n'):
            node = LineParser.parse_node(line)
            if node is not None:
                nodes = nodes.union({node})
                continue
            connection = LineParser.parse_connection(line)
            if connection is not None:
                connections = connections.union({connection})
                if connection.start_node not in nodes:
                    nodes = nodes.union({connection.start_node})
                if connection.end_node not in nodes:
                    nodes = nodes.union({connection.end_node})
                continue            
        return SimplifiedDotGraph(nodes, connections)

    def __eq__(self, other):
        return default_eq(self, other)
    
    def __str__(self):
        connections_str = '{'+', '.join([str(c) for c in self.connections])+'}'
        return 'Nodes: {}, Connections: {}'.format(
                                                self.nodes, connections_str)