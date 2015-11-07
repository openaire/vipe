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

class PipelineData:
    """An alternative representation of Pipeline with focus on data.
    
    A subset of information from Pipeline structure is used here, the
    focus is on data passed between the nodes.
    """
    
    def __init__(self, data):
        """
        Args:
            data (Dict[string, DataInfo]): a mapping from data ID to 
                DataInfo object corresponding to this data
        """
        self.__data = data

    @staticmethod
    def from_pipeline(pipeline):
        """Create object by analyzing Pipeline
        
        Args:
            pipeline (Pipeline): Pipeline to be analyzed
        
        Returns:
            PipelineData
        """
        data = {}
        for (name, node) in pipeline.nodes.items():
            for (port, data_id) in node.output_ports.items():
                if data_id not in data:
                    data[data_id] = DataInfo(set(), set())
                data[data_id].producers.add(DataAddress(name, port))
            for (port, data_id) in node.input_ports.items():
                if data_id not in data:
                    data[data_id] = DataInfo(set(), set())
                data[data_id].consumers.add(DataAddress(name, port))
        return PipelineData(data)
    
    @staticmethod
    def from_basic_data_types(data_dict):
        """Create object from a basic Python data types.
        
        Create it from a nested structure consisting of basic Python data types.
        This is useful if you want to create the structure directly in the
        code (like in tests) - it saves you some typing.
        
        Args:
            data_dict (Dict[string: Dict[string, List[string]]): definition of
                the register. It's structure can be shown schematically as:
                data ID -> ('producers' or 'consumers' -> list of addresses in
                a form of '$NODE_NAME:$NODE_PORT')
        """
        data = {}
        for (data_id, data_info) in data_dict.items():
            result_producers = set()
            result_consumers = set()
            for (elem_name, addresses) in data_info.items():
                result_addresses = set()
                for address_str in addresses:
                    address_elems = address_str.split(':')
                    assert len(address_elems) == 2
                    result_address = \
                        DataAddress(address_elems[0], address_elems[1])
                    result_addresses.add(result_address)
                assert elem_name in ['producers', 'consumers']
                if elem_name == 'producers':
                    result_producers = result_producers.union(result_addresses)
                elif elem_name == 'consumers':
                    result_consumers = result_consumers.union(result_addresses)
            result_info = DataInfo(result_producers, result_consumers)
            data[data_id] = result_info
        return PipelineData(data)
   
    def get_ids(self):
        """
        Returns:
            Set[string]: IDs of all data
        """
        return self.__data.keys()
    
    def get_info(self, data_id):
        """Get information about given data
        
        Args:
            data_id (string): Data ID
                
        Returns:
            DataInfo
        """ 
        return self.__data[data_id]

    def __eq__(self, other):
        return default_eq(self, other)

    def __str__(self):
        return self.to_yaml_dump()

class DataInfo:
    """Information related to a data ID"""
    
    def __init__(self, producers, consumers):
        """
        Args:
            producers (Set[DataAddress]): producers of given data
            consumers (Set[DataAddress]): consumers of given data
        """
        self.producers = producers
        self.consumers = consumers

    def __eq__(self, other):
        return default_eq(self, other)

class DataAddress:    
    def __init__(self, node, port):
        """
        Args:
            node (string): node of the node
            port (string): node of the port
        """
        self.node = node
        self.port = port

    def __eq__(self, other):
        return default_eq(self, other)
    
    def __str__(self):
        return '{}:{}'.format(self.node, self.port)
    
    def __hash__(self):
        return hash(str(self))