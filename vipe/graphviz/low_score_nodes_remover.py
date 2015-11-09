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

import copy

class LowScoreNodesRemover:
    __lowest_acceptable_score = -2
    
    def __init__(self, importance_score_map):
        """Args:
            importance_score_map (ImportanceScoreMap):
        """
        self.__score_map = importance_score_map
        
    def run(self, pipeline):
        """Remove nodes with importance score value below a threshold.
        
        Apart from low score, some other criteria have to be met in order
        to proceed with removing given node.
        
        Args:
            pipeline (Pipeline): input pipeline.
        
        Return:
            Pipeline: a copy of the input pipeline with some nodes removed.
        """
        result = copy.deepcopy(pipeline)
        names = list(result.nodes.keys())
        for name in names:
            node = result.nodes[name]
            if self.__score_map.get_score(node.importance) < \
                    self.__lowest_acceptable_score:
                ## Removing nodes with either no incoming or no outcoming 
                ## connections is easy. That's why we do it here. 
                ## As a substitute of checking for incoming and outcoming 
                ## connections, we check here the presence of
                ## input or output ports. We could later implement a more 
                ## precise solution where in fact existing connections are 
                ## checked (because there might be a situation that there 
                ## is a port, but it is not connected to anything).
                if (len(node.output_ports) == 0) or \
                    (len(node.input_ports) == 0):
                    del result.nodes[name]
        return result