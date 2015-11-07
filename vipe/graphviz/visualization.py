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
from vipe.pipeline.data_register import PipelineDataRegister 
from vipe.graphviz.dot import DotBuilder

def to_html(pipeline, output_dir):
    """
    Convert Pipeline to its visualization as an HTML document
    
    Args:
        pipeline (Pipeline): input Pipeline.
        output_dir (string): directory that will contain website with
            the visualization.
    """
    builder = DotBuilder()
    for (name, node) in pipeline.nodes.items():
        builder.add_node(name, labels=[name, 'type={}'.format(node.type)])
    
    data_register = PipelineDataRegister(pipeline)
    
    for data_id in data_register.get_data_ids():
        producers = data_register.get_producers(data_id)
        if len(producers) == 0:
            raise NotImplementedError
        elif len(producers) > 1:
            raise NotImplementedError
        else:
            raise NotImplementedError
        
        consumers = data_register.get_consumers(data_id)
        if len(consumers) == 0:
            raise NotImplementedError
        else:
            raise NotImplementedError
        
    
        for (port_name, data_id) in node.output_ports:
            ##TODO: implement
            destination_nodes = builder.get_destination_nodes()
            for (dst_node_name, dst_node_port) in destination_nodes:
                builder.add_edges(name, [dst_node_name])