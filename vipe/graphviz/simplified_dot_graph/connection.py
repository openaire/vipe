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

class Connection:
    def __init__(self, start_node, start_port, end_node, end_port):
        """Args:
            start_node (string): name of the start node
            start_port (string): name of the output port in the start node
            end_node (string): name of the end node
            end_port (string): name of the input port in the end node
        """
        self.start_node = start_node
        self.start_port = start_port
        self.end_node = end_node
        self.end_port = end_port
    
    def __str__(self):
        start_port_str = self.__get_port_string(self.start_port)
        end_port_str = self.__get_port_string(self.end_port)
        return '"{}"{} -> "{}"{}'.format(self.start_node, start_port_str,
                                       self.end_node, end_port_str)

    @staticmethod
    def __get_port_string(port_name):
        port_str = ''
        if port_name is not None:
            port_str = ':"{}"'.format(port_name)
        return port_str       
    
    def __eq__(self, other):
        return default_eq(self, other)

    def __hash__(self):
        return hash(str(self))