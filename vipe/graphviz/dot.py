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

import io.StringIO
import re

whitespace_pattern = re.compile(r'\s+')

# class LabelsRegister:
#     """
#     Register that assigns and stores mapping between user-readable labels and 
#     technical identifiers used in the *.dot file.
#     """
#     def __init__(self):
#         self.__d = {}
#         self.__largest = 0
# 
#     def get(self, label):
#         """@return node identifier assigned to given label"""
#         if label not in self.__d:
#             self.__largest = self.__largest+1
#             self.__d[label] = self.__largest
#         index = self.__d[label]
#         return 'n'+str(index)
    
class DotProcessor:
    """Takes GraphViz's graph in dot format and generates some derivative data.
    """
    
    def __init__(self, dot_graph):
        """
        Args:
            dot_graph (string): description of graph in GraphViz's dot format
        """
        self.__dot_graph = dot_graph
    
    def get_image_map(self):
        """
        Returns:
            string: client-size image map ready to be embedded in 
                HTML document. This is GraphViz's `cmapx` output 
                (see http://www.graphviz.org/doc/info/output.html#a:cmapx).
        """
        raise NotImplementedError
    
    def save_image(self, output_path):
        """Save the image to a file at given path
        
        Args:
            output_path (string): path to output png file
        """
        raise NotImplementedError
        
        
class DotBuilder:
    """Tool for creating description of the graph using GraphViz's dot format.
    """
    
    def __init__(self):
        self.__s = io.StringIO()

    def add_edges(self, start, ends, label=None):
        """
        Args:
            start (string): label of the start node
            ends (List[string]): labels of the end nodes
        """
        text = start+' -> {'+' '.join(ends)+'}'
        parameters = []
        if label is not None:
            parameters.append('label="{}"'.format(self.__normalize_label(label)))
        if len(parameters) == 0:
            print(text, file = self.__s)
        else:
            print('{}[{}]'.format(text, ' '.join(parameters)), file = self.__s)
    
    def add_node(self, name, labels=None, color=None, shape=None):
        """
        Args:
            labels (List[string]): list of labels to be printed in the node. 
            Each label is placed in a separate line.
            color (string): value taken from 
                http://graphviz.org/doc/info/colors.html
            shape (string): value taken from 
                http://graphviz.org/doc/info/shapes.html
        """
        if (labels is None) and (color is None) and (shape is None):
            return
        params = []
        if labels is not None:
            text = []
            for label in labels:
                text.append(self.__normalize_label(label))
            params.append('label="{}"'.format(r'\n'.join(text)))
        if color is not None:
            params.append('fillcolor={},style=filled'.format(color))
        if shape is not None:
            params.append('shape={}'.format(shape))
        print('{}[{}]'.format(name, ' '.join(params)), file = self.__s)
    
    def get_result(self, output_path):
        """
        Returns:
            string: graph description in dot format 
        """ 
        return self.__s.getvalue()

    @staticmethod
    def __normalize_label(label):
        text = label
        text = text.replace('"', '\'')
        text = re.sub(whitespace_pattern, ' ', text)
        return text
