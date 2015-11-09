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
from vipe.pipeline.pipeline import NodeImportance

__author__ = "Mateusz Kobos mkobos@icm.edu.pl"

from vipe.graphviz.dot import DotBuilder

class DotBuilderWrapper:
    """Wrapper for DotBuilder class.
    
    It is an intermediate layer between the dot format and business logic. 
    It translates business-level node objects to concepts of the dot format.
    """
    def __init__(self, importance_score_map):
        """Args:
            importance_score_map (ImportanceScoreMap):
        """
        self.__b = DotBuilder()
        self.__reg = _NamesRegister()
        self.__e_reg = _EdgesRegister()
        self.__importance_score_map = importance_score_map
    
    def __map(self, name):
        return self.__reg.get(name)
    
    def add_node(self, name, node):
        """Args:
            name (string): name of the node
            node (vipe.pipeline.pipeline.Node): data about the node
        """
        color = self.__get_color(node.importance)
        
        importance_score = \
            self.__importance_score_map.get_score(node.importance)
        if importance_score > -1:
            self.__b.add_node(self.__map(name), 
                            labels=[name, 'type={}'.format(node.type)], 
                            shape='box', color=color)
        elif importance_score == -1:
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
    
    def add_data_node(self, data_id):
        """Args:
            data_id (string): data ID
        """
        self.__b.add_node(self.__map(data_id), shape='point')
    
    def get_input_node_name(self):
        return 'INPUT'
    
    def add_input_node(self):
        self.__b.add_node(self.__map(self.get_input_node_name()), 
                          labels=[self.get_input_node_name()], 
                          shape='rarrow')
    
    def get_output_node_name(self):
        return 'OUTPUT'
    
    def add_output_node(self):
        self.__b.add_node(self.__map(self.get_output_node_name()), 
                          labels=[self.get_output_node_name()], 
                          shape='rarrow')
    
    def add_edge(self, start, end):
        """Add connection between two addresses. 
        
        The name field of the DataAddress might be a name of a node or a
        data ID - in the latter case the address corresponds to data. 
        The port field of the address might be set to `None`. It is
        always `None` if the address corresponds to data. 
        
        Args:
            start (DataAddress): start of the connection
            end (DataAddress): end of the connection
        """
        ## The code below prevents multiple edges connecting given two nodes 
        ## to be shown in the diagram. This makes sense when ports are not
        ## shown. In a mode of showing nodes, this should not be prevented
        ## any more.
        if self.__e_reg.contains(start.node, end.node):
            return
        else:
            self.__e_reg.add(start.node, end.node)
            self.__b.add_edge(self.__map(start.node), self.__map(end.node))
    
    def get_result(self):
        """Return:
            string: resulting graph in dot format
        """
        return self.__b.get_result()

class _NamesRegister:
    """
    Register that assigns and stores mapping between user-readable names of 
    nodes and technical identifiers used in the *.dot file.
    """
    def __init__(self):
        self.__d = {}
        self.__largest = 0

    def get(self, name):
        """@return node identifier assigned to given name"""
        if name not in self.__d:
            self.__largest = self.__largest+1
            self.__d[name] = self.__largest
        index = self.__d[name]
        return 'n'+str(index)

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