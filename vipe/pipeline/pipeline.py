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

import yaml

import vipe.common.serialization
from vipe.common.utils import default_eq

class Pipeline(yaml.YAMLObject):
    """A graph structure corresponding to workflow pipeline.
    
    Producer-consumer dependencies are presented explicitly here. However,
    the information about sequence of execution of consecutive workflow nodes is
    gone.
    """
    yaml_tag = '!Pipeline'
    
    def __init__(self, nodes):
        """
        Args:
            nodes (Dict[string, Node]): a dictionary mapping name of a node 
                to a Node object.
        """
        self.nodes = nodes

    def __eq__(self, other):
        return default_eq(self, other)
    
    def __str__(self):
        return self.to_yaml_dump()

    def to_yaml_dump(self):
        """Dump the graph to YAML.
        """
        return vipe.common.serialization.to_yaml(self)
    
    @staticmethod
    def from_yaml_dump(yaml_string):
        """Read the graph from YAML dump."""
        return vipe.common.serialization.from_yaml(yaml_string)

class Node(yaml.YAMLObject):
    yaml_tag = '!Node'
    
    def __init__(self, type_, input_ports, output_ports):
        """
        Args:
            type_ (string): a description of the type of the node.
            input_ports (Dict[string, string]): ports from which the node takes 
                data to consume. 
                The key in the dictionary is the name of the port, the value 
                is a data identifier. This is an identifier of the data 
                consumed on this port. A producer port of one node is connected 
                to a consumer port of another node by specifying the same 
                data identifier.
            output_ports (Dict[string, string]): ports to which the node 
                produces data. The meaning of the elements of the dictionary
                is analogous to `input_ports`.
        """ 
        self.type = type_
        self.input_ports = input_ports
        self.output_ports = output_ports

    def __eq__(self, other):
        return default_eq(self, other)