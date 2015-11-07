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

class PipelineDataRegister:
    """A register of producers and consumers of data in the Pipeline."""
    
    def __init__(self, pipeline):
        """
        Args:
            pipeline (Pipeline): Pipeline to be analyzed
        """
        self.__producers = {}
        self.__consumers = {}
        self.__data_ids = set()
        for (name, node) in pipeline.nodes.iter():
            self.__add_to_dict(self.__consumers, self.__data_ids, name, 
                               node.input_ports)
            self.__add_to_dict(self.__producers, self.__data_ids, name, 
                               node.output_ports)
    
    @staticmethod
    def __add_to_dict(dict_, data_ids, node_name, node_ports_dict):
        for (port, data_id) in node_ports_dict.iter():
            if data_id not in data_ids:
                data_ids.add(data_id)
            if data_id not in dict_:
                dict_[data_id] = []
            self.__dict_[data_id].append(DataAddress(node_name, port))
    
    def get_data_ids(self):
        """
        Returns:
            Set[string]: data IDs
        """
        return self.__data_ids
    
    def get_producers(self, data_id):
        """Get information about producers of given data
                
        Returns:
            List[DataAddress]
        """ 
        return self.__producers[data_id]
    
    def get_consumers(self, data_id):
        """Get information about consumers of given data
                
        Returns:
            List[DataAddress]
        """ 
        return self.__consumers[data_id]
            
            
class DataAddress:
    def __init__(self, name, port):
        """
        Args:
            name (string): name of the node
            port (string): name of the port
        """
        self.name = name
        self.port = port