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
        
        Apart from the low score, another condition must hold for a given node
        to be removed. Namely, given node has to lack either input or output 
        ports. This condition is a substitute of removing nodes with either 
        no incoming or no outcoming connections. We could later implement a 
        more precise solution where existing connections are checked 
        (this makes sense because there might be a situation that we have a
        port, but it is not connected to anything) 
        
        Note that we focus here on removing nodes with either incoming or 
        outcoming connections missing and this is because removing such nodes
        from a graph is easy. However, if required, we might
        implement a solution that removes also nodes with both 
        incoming and outcoming connections present.
        
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
                if (len(node.output_ports) == 0) or \
                    (len(node.input_ports) == 0):
                    del result.nodes[name]
        return result