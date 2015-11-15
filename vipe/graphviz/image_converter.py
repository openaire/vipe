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

import subprocess
import os.path

class ImageConverter:
    """Takes GraphViz's graph in dot format and generates some derivative data.
    """
    
    def __init__(self, dot_graph, dot_program_path='/usr/bin/dot'):
        """
        Args:
            dot_graph (string): description of graph in GraphViz's dot format
            dot_program_path (string): path to the `dot` program installed
                in the system along with GraphViz library
        """
        if not os.path.isfile(dot_program_path):
            raise Exception('Given path to "dot" program ("{}") is incorrect. '
                'It does not exist or it does not correspond to a file. '
                'This might mean that GraphViz library is not installed '
                'in the system.')
        self.__dot_graph = dot_graph
        self.__dot_program_path = dot_program_path
    
    def to_image_map(self):
        """
        Returns:
            string: client-size image map ready to be embedded in 
                HTML document. This is GraphViz's `cmapx` output 
                (see http://www.graphviz.org/doc/info/output.html#a:cmapx).
        """
        raise NotImplementedError
    
    def to_image(self):
        """Convert the dot graph to a PNG image
        
        Return:
            byte string
        """
        p = subprocess.Popen([self.__dot_program_path, '-Tpng'], 
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        stdout, stderr = p.communicate(self.__dot_graph.encode('utf-8'))
        if len(stderr) > 0:
            raise Exception('Error output produced while running'
                            ' dot program: {} '.format(str(stderr)))
        return stdout