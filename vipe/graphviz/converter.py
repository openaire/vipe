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

from vipe.pipeline.pipeline_data import PipelineData, DataAddress
from vipe.graphviz.dot_wrapper import DotBuilderWrapper
from vipe.graphviz.importance_score_map import ImportanceScoreMap
from vipe.graphviz.low_score_nodes_remover import LowScoreNodesRemover

class Converter:
    """Convert Pipeline to its visualization in GraphViz dot format."""
    
    def __init__(self, detail_level, show_input_ports, show_output_ports, 
                 vertical_orientation=True):
        """Args:
            detail_level (DetailLevel): level of presentation details
            show_input_ports (bool): 
            show_output_ports (bool):
            vertical_orientation (bool): True if the graph should be drawn
                from top to bottom, False if it should be drawn from left to
                right.
        """
        score_map = ImportanceScoreMap(detail_level)
        self.__b = DotBuilderWrapper(
                            score_map, show_input_ports, show_output_ports,
                            vertical_orientation)
        self.__low_score_nodes_remover = LowScoreNodesRemover(score_map)
        self.__input_created = False
        self.__output_created = False
        self.__already_run = False
    
    def run(self, pipeline):
        """
        Convert Pipeline to its visualization in GraphViz dot format
        
        Args:
            pipeline (Pipeline): input Pipeline.
        
        Return:
            string: dot format
        """
        assert self.__already_run == False
        self.__already_run = True
        
        clean_pipeline = self.__low_score_nodes_remover.run(pipeline)
        
        ## We sort the collection to obtain the same order of output elements
        ## every time. That is, we remove non-determinism of the output.
        for (name, node) in \
                sorted(clean_pipeline.nodes.items(), key=lambda x: x[0]):
            self.__b.add_node(name, node)
        pipeline_data = PipelineData.from_pipeline(clean_pipeline)
        
        ## We sort the collection to obtain the same order of output elements
        ## every time. That is, we remove non-determinism of the output.
        for data_id in sorted(pipeline_data.get_ids()):
            info = pipeline_data.get_info(data_id)
            start = self.__get_data_start(data_id, info.producers)
            ends = self.__get_data_ends(data_id, info.consumers)
            if start is not None and ends is not None:
                for end in ends:
                    self.__b.add_edge(start, end)
        return self.__b.get_result()
    
    def __get_data_start(self, data_id, data_producers):
        if len(data_producers) == 0:
            return None
        elif len(data_producers) > 1:
            self.__b.add_data_node(data_id)
            for address in data_producers:
                self.__b.add_edge(address, DataAddress(data_id, None))
            return DataAddress(data_id, None)
        else:
            assert len(data_producers) == 1
            ## Take an element from the set
            for e in data_producers:
                break
            return e
    
    def __get_data_ends(self, data_id, data_consumers):
        if len(data_consumers) == 0:
            return None
        else:
            return [address for address in data_consumers]