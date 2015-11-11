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

import io
import re

whitespace_pattern = re.compile(r'\s+')
        
class DotBuilder:
    """Tool for creating description of the graph using GraphViz's dot format.
    """
    
    def __init__(self):
        self.__s = io.StringIO()
        self.__build_finished = False
        print('digraph {', file=self.__s)

    def add_edge(self, start, end, label=None):
        """
        Args:
            start (string): label of the start node
            end (string): label of the end node
        """
        assert self.__build_finished == False
        text = '{} -> {}'.format(start, end)
        parameters = []
        if label is not None:
            parameters.append('label="{}"'.format(self.__normalize_label(label)))
        if len(parameters) == 0:
            print(text, file = self.__s)
        else:
            print('{}[{}]'.format(text, ' '.join(parameters)), file=self.__s)
    
    def add_node(self, name, labels=None, color=None, shape=None, 
                 width=None, height=None):
        """
        Args:
            labels (List[string]): list of labels to be printed in the node. 
            Each label is placed in a separate line.
            color (string): value taken from 
                http://graphviz.org/doc/info/colors.html
            shape (string): value taken from 
                http://graphviz.org/doc/info/shapes.html
            width (float): width of the node in inches. See
                http://graphviz.org/doc/info/attrs.html#d:width for details.
            height (float): height of the node in inches. See
                http://graphviz.org/doc/info/attrs.html#d:height for details.
        """
        assert self.__build_finished == False
        if (labels is None) and (color is None) and (shape is None) and \
                (width is None) and (height is None):
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
        if width is not None or height is not None:
            params.append('fixedsize=true')
            if width is not None:
                params.append('width={}'.format(width))
            if height is not None:
                params.append('height={}'.format(height))
        print('{}[{}]'.format(name, ' '.join(params)), file=self.__s)
    
    def get_result(self):
        """
        Returns:
            string: graph description in dot format 
        """ 
        if self.__build_finished == False:
            self.__build_finished = True
            print('}', file=self.__s)
        return self.__s.getvalue()

    @staticmethod
    def __normalize_label(label):
        text = label
        text = text.replace('"', '\'')
        text = re.sub(whitespace_pattern, ' ', text)
        return text
