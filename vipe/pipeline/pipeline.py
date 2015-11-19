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
from enum import Enum, unique

import vipe.common.serialization
from vipe.common.utils import default_eq

@unique
class NodeImportance(Enum):
    """Importance of the node in the data processing workflow.
    
    The higher importance of the node, the more prominently it should be
    shown on the graph. With the default details level of showing nodes
    on the graph, the node with the `lowest` priority should be removed
    from the graph."""
    lowest = 1
    very_low = 2
    low = 3
    normal = 4

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
            nodes (Dict[string, Node]): a dictionary mapping node of a node 
                to a Node object.
        """
        self.nodes = nodes
    
    @staticmethod
    def get_input_node_name():
        """Name of a special node that defines data ingested by the pipeline.
        
        The node with this name might not be present in the pipeline."""
        return 'INPUT'
    
    @staticmethod
    def get_output_node_name():
        """Name of a special node that defines data produced by the pipeline.
        
        The node with this name might not be present in the pipeline."""
        return 'OUTPUT'

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
    
    def __init__(self, type_, input_ports, output_ports, 
                 importance=NodeImportance.normal):
        """
        Args:
            type_ (string): a description of the type of the node.
            input_ports (Dict[string, string]): ports from which the node takes 
                data to consume. 
                The key in the dictionary is the node of the port, the value 
                is a data identifier. This is an identifier of the data 
                consumed on this port. A producer port of one node is connected 
                to a consumer port of another node by specifying the same 
                data identifier.
            output_ports (Dict[string, string]): ports to which the node 
                produces data. The meaning of the elements of the dictionary
                is analogous to `input_ports`.
            importance (Importance): how important given node is. This 
                influences the presentation of the node on the graph.
        """ 
        self.type = type_
        self.input_ports = input_ports
        self.output_ports = output_ports
        self.importance = importance
        
    def __getstate__(self):
        """__getstate__() and __setstate__() methods are overriden.
        
        This is because enum field `self.importance` by default is not 
        serialized to YAML nicely, namely the field is serialized as, e.g.:
             importance: &id001 !!python/object/apply:vipe.pipeline.pipeline.Importance
             - 4
        Overriding these two methods gives us control over how this 
        enum field (and other fields as well) are serialized.
        """
        return {'type': self.type,
                'input_ports': self.input_ports,
                'output_ports': self.output_ports,
                'importance': self.importance.name}
    
    def __setstate__(self, state):
        """See the comment to __getstate__() method"""
        self.type = state['type']
        self.input_ports = state['input_ports']
        self.output_ports = state['output_ports']
        self.importance = NodeImportance[state['importance']]

    def __eq__(self, other):
        return default_eq(self, other)