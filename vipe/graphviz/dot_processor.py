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