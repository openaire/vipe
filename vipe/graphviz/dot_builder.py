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

class DotBuilder:
    """Tool for creating description of the graph using GraphViz's dot format.
    """
    
    __whitespace_pattern = re.compile(r'\s+')
    
    def __init__(self, vertical_orientation=True):
        """Args:
            vertical_orientation (bool): True if the graph should be drawn
                from top to bottom, False if it should be drawn from left to
                right.
        """
        self.__s = io.StringIO()
        self.__build_finished = False
        self.__print('digraph {')
        if not vertical_orientation:
            self.__print('rankdir=LR')

    def add_edge(self, start, start_output_port, end, end_input_port, 
                 label=None):
        """
        Args:
            start (string): label of the start node
            start_output_port (string): name of the start node's output port.
                If None, the node will be connected directly, not through
                its port (if any).
            end (string): label of the end node
            end_input_port (string): name of the end node's input port.
                If None, the node will be connected directly, not through
                its port (if any).
            label (string): label of the edge.
        """
        assert self.__build_finished == False
        connection_text = '{} -> {}'.format(
                self.__build_edge_point(start, start_output_port), 
                self.__build_edge_point(end, end_input_port))
        parameters = []
        if label is not None:
            parameters.append('label="{}"'.format(self.__normalize_label(label)))
        if len(parameters) == 0:
            self.__print(connection_text)
        else:
            self.__print('{}[{}]'.format(connection_text, ' '.join(parameters)))
    
    @staticmethod
    def __build_edge_point(node, port):
        text = ['"{}"'.format(node)]
        if port is not None:
            text.append(':')
            text.append('"{}"'.format(port))
        return ''.join(text)
    
    def add_node(self, name, labels=None, color=None, shape=None, 
                 width=None, height=None, use_raw_labels=False):
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
            use_raw_labels (bool): if True, the labels given as the input
                is not preprocessed.
        """
        assert self.__build_finished == False
        if (labels is None) and (color is None) and (shape is None) and \
                (width is None) and (height is None):
            return
        params = []
        if labels is not None:
            text = []
            for label in labels:
                processed_label = label
                if not use_raw_labels:
                    processed_label = self.__normalize_label(label)
                text.append(processed_label)
            final_label_text = r'\n'.join(text)
            if not use_raw_labels:
                final_label_text = '"{}"'.format(final_label_text)
            params.append('label={}'.format(final_label_text))
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
        self.__print('"{}" [{}]'.format(name, ' '.join(params)))
    
    def get_result(self):
        """
        Returns:
            string: graph description in dot format 
        """ 
        if self.__build_finished == False:
            self.__build_finished = True
            self.__print('}')
        return self.__s.getvalue()
    
    def __print(self, text):
        print(text, file=self.__s)

    @staticmethod
    def __normalize_label(label):
        text = label
        text = text.replace('"', '\'')
        text = re.sub(DotBuilder.__whitespace_pattern, ' ', text)
        return text