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

from vipe.oozie.converter.converter import PipelineConverter
from vipe.oozie.graph import SubworkflowAction, JavaAction, \
    StreamingMapReduceAction, JavaMapReduceAction, PigAction, HiveAction, \
    Decision
from vipe.pipeline.pipeline import Node

class IISPipelineConverter(PipelineConverter):
    """Converter for Oozie workflows following conventions used in 
    OpenAIRE's IIS project (https://github.com/openaire/iis)"""
    
    def convert_node(self, oozie_node):
        if isinstance(oozie_node, SubworkflowAction):
            return self.__handle_subworkflow(oozie_node)
        elif isinstance(oozie_node, JavaAction):
            return self.__handle_java_action(oozie_node)
        elif isinstance(oozie_node, StreamingMapReduceAction):
            return self.__handle_mapreduce_action(
                                    oozie_node, 'StreamingMapReduceAction')
        elif isinstance(oozie_node, JavaMapReduceAction):
            return self.__handle_java_mapreduce_action(oozie_node)
        elif isinstance(oozie_node, PigAction):
            return self.__handle_pig_action(oozie_node)
        elif isinstance(oozie_node, HiveAction):
            return self.__handle_hive_action(oozie_node)
        elif isinstance(oozie_node, Decision):
            return None ##TODO
        else:
            return None
    
    @staticmethod
    def __handle_subworkflow(node):
        input_ports = IISPipelineConverter.__get_ports_from_configuration(
            'input', node.configuration)
        output_ports = IISPipelineConverter.__get_ports_from_configuration(
            'output', node.configuration)
        return Node('SubworkflowAction', input_ports, output_ports)
    
    @staticmethod
    def __get_ports_from_configuration(type_prefix, configuration):
        """
        Args:
            type_prefix (string): either 'input' or 'output'
            configuration (Dict[string, string]): configuration dictionary
        
        Return:
            Dict[string, string]: Key is the name of the port while the value
                is the path assigned to it.
        """
        keys = configuration.keys()
        prefixed_keys = [k for k in keys if k.startswith(type_prefix)]
        if type_prefix in prefixed_keys:
            if len(prefixed_keys) != 1:
                other_matching_keys = \
                    IISPipelineConverter.__remove_from_list_to_str(prefixed_keys, 
                                                                type_prefix)
                raise Exception('Among the configuration properties, there '
                    'was a property called "{}". Nevertheless, some other '
                    'properties prefixed with "{}" were found '
                    ' ({}). This is not allowed.'.format(
                        type_prefix, type_prefix, other_matching_keys))
            return {type_prefix: configuration[type_prefix]}
        else:
            ports = {}
            expected_prefix = '{}_'.format(type_prefix)
            for k in prefixed_keys:
                if not k.startswith(expected_prefix):
                    raise Exception('Expected prefix "{}", but "{}" '
                        'is not prefixed like that. This is not allowed.'.
                            format(expected_prefix, k))
                suffix = k[len(expected_prefix):]
                ports[suffix] = configuration[k]
        return ports
    
    @staticmethod
    def __remove_from_list_to_str(list_, elem):
        l_removed = list_.copy().remove(elem)
        return ', '.join('"{}"'.format(str(l_removed)))
  
    @staticmethod
    def __handle_prefixed_args(args, input_prefix, output_prefix, node_type):
        input_ports = IISPipelineConverter.__get_ports_from_args(
                                                    input_prefix, args)
        output_ports = IISPipelineConverter.__get_ports_from_args(
                                                     output_prefix, args)
        return Node(node_type, input_ports, output_ports)
    
    @staticmethod
    def __handle_java_action(node):
        return IISPipelineConverter.__handle_prefixed_args(
                node.args, '-I', '-O', 'JavaAction')
    
    @staticmethod
    def __handle_pig_action(node):
        return IISPipelineConverter.__handle_prefixed_args(
                node.params, 'input_', 'output_', 'PigAction')

    @staticmethod
    def __handle_hive_action(node):
        return IISPipelineConverter.__handle_prefixed_args(
                node.params, 'input_', 'output_', 'HiveAction')
    
    @staticmethod
    def __get_ports_from_args(type_prefix, args):
        """
        Args:
            type_prefix (string): e.g. '-I' or '-O'
            args (Array[string]): command line arguments of the Java node
        
        Return:
            Dict[string, string]: Key is the name of the port while the value
                is the path assigned to it.
        """
        port_args = [a for a in args if a.startswith(type_prefix)]
        ports = {}
        for port_arg in port_args:
            port_str = port_arg[len(type_prefix):]
            elems = port_str.split('=', 1)
            if len(elems) != 2:
                raise Exception('Two elements expected but more found in "{}"'
                                    .format(port_str))
            ports[elems[0]] = elems[1]
        return ports
    
    @staticmethod
    def __handle_java_mapreduce_action(node):
        if 'avro.mapreduce.multipleoutputs' in node.configuration:
            return IISPipelineConverter.__handle_java_mapreduce_multiple_outputs(node)
        else:
            return IISPipelineConverter.__handle_mapreduce_action(
                                                node, 'JavaMapReduceAction')
    
    @staticmethod
    def __handle_java_mapreduce_multiple_outputs(node):
        output_names = node.configuration['avro.mapreduce.multipleoutputs']
        o_names = output_names.strip().split()
        output_dir = node.configuration['mapred.output.dir']
        outputs = {name: '{}/{}'.format(output_dir, name.strip()) \
                   for name in o_names}
        input_port = node.configuration['mapred.input.dir']
        return Node('JavaMapReduceAction', 
                    {'input': input_port}, outputs)
    
    @staticmethod
    def __handle_mapreduce_action(node, node_type):
        input_port = node.configuration['mapred.input.dir']
        output_port = node.configuration['mapred.output.dir']
        return Node(node_type, 
                    {'input': input_port}, {'output': output_port})