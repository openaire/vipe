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

from vipe.pipeline.pipeline import Pipeline

class PipelineConverter:
    """Interface to be implemented by all classes that implement conversion of 
        OozieGraph to Pipeline.
    """
    
    def convert_node(self, oozie_node):
        """Convert OozieGraph's Node
        
        Args:
            oozie_node (vipe.oozie.graph.Node): OozieGraph's Node
        
        Returns:
            vipe.pipeline.pipeline.Node: Pipeline's Node. If `None` is returned,
                it is assumed that given node should be ignored.
        """
        raise NotImplementedError

def convert(oozie_graph, pipeline_converter):
    """Convert OozieGraph to Pipeline using given Converter
    
    Args:
        oozie_graph (OozieGraph):
        pipeline_converter (PipelineConverter):
    
    Returns:
        Pipeline
    """
    pipeline_nodes = {}
    for (name, oozie_node) in oozie_graph.nodes.items():
        pipeline_node = pipeline_converter.convert_node(oozie_node)
        if pipeline_node is not None:
            pipeline_nodes[name] = pipeline_node
    return Pipeline(pipeline_nodes)