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

from vipe.pipeline.pipeline import NodeImportance, Pipeline
from vipe.graphviz.dot_builder import DotBuilder
from vipe.graphviz.ports_label_printer import PortsLabelPrinter, PortName

class DotBuilderWrapper:
    """Wrapper for DotBuilder class.
    
    It is an intermediate layer between the dot format and business logic. 
    It translates business-level node objects to concepts of the dot format.
    """
    def __init__(self, importance_score_map, 
                 show_input_ports, show_output_ports, 
                 vertical_orientation=True):
        """Args:
            importance_score_map (ImportanceScoreMap):
            show_input_ports (bool): 
            show_output_ports (bool):
            vertical_orientation (bool): True if the graph should be drawn
                from top to bottom, False if it should be drawn from left to
                right.
        """
        self.__b = DotBuilder(vertical_orientation)
        self.__e_reg = _EdgesRegister()
        self.__n_reg = _NodesRegister()
        self.__importance_score_map = importance_score_map
        self.__show_input_ports = show_input_ports
        self.__show_output_ports = show_output_ports
    
    def __map(self, name):
        return _NamesConverter.run(name)
    
    def add_node(self, name, node):
        """Args:
            name (string): name of the node
            node (vipe.pipeline.pipeline.Node): data about the node
        """
        if name in self.get_reserved_node_names():
            raise Exception('Node name "{}" not allowed since it is a '
                            'reserved word.'.format(name))
        
        color = self.__get_color(node.importance)
        if name in [Pipeline.get_input_node_name(),
                    Pipeline.get_output_node_name()]:
            self.__n_reg.add(name, _NodeInfo(True, True))
            self.__add_advanced_node(name, node, True, True, color, 'folder')
            return
        
        importance_score = \
            self.__importance_score_map.get_score(node.importance)
        if importance_score > -1:
            self.__n_reg.add(name, _NodeInfo(self.__show_input_ports,
                                             self.__show_output_ports))
            self.__add_advanced_node(name, node, 
                    self.__show_input_ports, self.__show_output_ports, color)
        else:
            self.__n_reg.add(name, _NodeInfo(False, False))
            if importance_score == -1:
                self.__b.add_node(self.__map(name), labels=[''], shape='box',
                                  width=0.2, height=0.2, color=color)
            elif importance_score < -1:
                self.__b.add_node(self.__map(name), labels=[''], shape='box',
                                  width=0.1, height=0.1, color=color)

    @staticmethod
    def __get_color(importance):
        color = 'white'
        if importance == NodeImportance.normal:
            color = 'cyan'
        elif importance == NodeImportance.low:
            color = 'lightcyan'
        return color
    
    def get_reserved_node_names(self):
        return [Pipeline.get_input_node_name(), Pipeline.get_output_node_name()]

    def __add_advanced_node(self, node_name, node, 
                         show_input_ports, show_output_ports, color, 
                         shape=None):
        """
        Args:
            shape(string): shape of the node. If None, the default
                approach of deciding which shape is appropriate is used.
        """
        labels=[node_name, 'type={}'.format(node.type)]
        if show_input_ports or show_output_ports:
            input_ports = []
            if show_input_ports:
                input_ports = self.__port_labels_to_PortNames(
                                            node.input_ports.keys(), True)            
            output_ports = []
            if show_output_ports:
                output_ports = self.__port_labels_to_PortNames(
                                            node.output_ports.keys(), False)
            labels = [PortsLabelPrinter().run(
                        labels, input_ports, output_ports, color)]
            if shape is None:
                shape = 'none'
            self.__b.add_node(self.__map(node_name), labels=labels, 
                              shape=shape, use_raw_labels=True)
        else:
            if shape is None:
                shape = 'box'
            self.__b.add_node(self.__map(node_name), labels=labels, 
                              shape=shape, color=color)

    
    @staticmethod
    def __port_labels_to_PortNames(port_labels, are_input_ports):
        names = []
        for n in sorted(port_labels):
            internal_name = DotBuilderWrapper.__port_name_to_internal_name(
                                                        n, are_input_ports)
            names.append(PortName(n, internal_name))
        return names   

    @staticmethod
    def __port_name_to_internal_name(name, is_input_port):
        if name is None:
            return None
        prefix = 'output_'
        if is_input_port:
            prefix = 'input_'
        return '{}{}'.format(prefix, name)
    
    def add_data_node(self, data_id):
        """Args:
            data_id (string): data ID
        """
        self.__b.add_node(self.__map(data_id), shape='point')
    
    def add_edge(self, start, end):
        """Add connection between two nodes. 
        
        The name field of the DataAddress might be a name of a node or a
        data ID - in the latter case the address corresponds to data. 
        The port field of the address might be set to `None`. It is
        always `None` if the address corresponds to data. 
        
        Args:
            start (DataAddress): start of the connection
            end (DataAddress): end of the connection
        """
        start_output_port = None
        if self.__n_reg.contains(start.node) and \
                self.__n_reg.get(start.node).has_visible_output_ports:
            start_output_port = start.port
        end_input_port = None
        if self.__n_reg.contains(end.node) and \
                self.__n_reg.get(end.node).has_visible_input_ports:
            end_input_port = end.port
        if start_output_port is not None or end_input_port is not None:
            self.__b.add_edge(
                    self.__map(start.node), 
                    self.__port_name_to_internal_name(start_output_port, False), 
                    self.__map(end.node), 
                    self.__port_name_to_internal_name(end_input_port, True))
        else:
            assert start_output_port is None
            assert end_input_port is None
            if not self.__e_reg.contains(start.node, end.node):
                self.__b.add_edge(self.__map(start.node), None, 
                                  self.__map(end.node), None)
        if not self.__e_reg.contains(start.node, end.node):
            self.__e_reg.add(start.node, end.node)
    
    def get_result(self):
        """Return:
            string: resulting graph in dot format
        """
        return self.__b.get_result()

class _NamesConverter:
    """Convert name of a node to representation accepted by dot format."""
    
    __pattern = re.compile(r'([\"])')

    @staticmethod
    def run(name):
        escaped_name = re.sub(_NamesConverter.__pattern, r'\\\1', name)
        return escaped_name

class _NodeInfo:
    """Information about the node stored by _NodesRegister"""
    
    def __init__(self, has_visible_input_ports, has_visible_output_ports):
        self.has_visible_input_ports = has_visible_input_ports
        self.has_visible_output_ports = has_visible_output_ports

class _NodesRegister:
    """Register of all nodes with information relevant to visualization."""
    
    def __init__(self):
        self.__nodes = {}
    
    def contains(self, node_name):
        """Args:
            node_name (string): name of the node
        """
        return node_name in self.__nodes
    
    def add(self, node_name, node_info):
        """Args:
            node_name (string): name of the node
            node_info (_NodeInfo): 
        """
        if node_name in self.__nodes:
            raise Exception('Node with name {} already exists in the register.'\
                                .format(node_name))
        self.__nodes[node_name] = node_info
    
    def get(self, node_name):
        """Args:
            node_name (string): name of the node
        """
        return self.__nodes[node_name]

class _EdgesRegister:
    """Register of all edges."""

    def __init__(self):
        self.__starts = {}
    
    def contains(self, start, end):
        """Args:
            start (string): start of the edge
            end (string): end of the edge
        """
        if start not in self.__starts:
            return False
        if end not in self.__starts[start]:
            return False
        return True
    
    def add(self, start, end):
        """Args:
            start (string): start of the edge
            end (string): end of the edge
        """
        if start not in self.__starts:
            self.__starts[start] = set()
        if end in self.__starts[start]:
            raise Exception('End "{}" already registered.'.format(end))
        self.__starts[start].add(end)