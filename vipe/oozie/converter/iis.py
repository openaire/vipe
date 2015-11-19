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
from vipe.pipeline.pipeline import Node, NodeImportance

class IISPipelineConverter(PipelineConverter):
    """PipelineConverter for Oozie workflows following conventions used in 
    OpenAIRE's IIS project (https://github.com/openaire/iis)"""
    
    __IO_nodes_type = 'I/O'
    
    def convert_parameters(self, parameters):
        input_ = self.__get_ports_from_parameters('input', parameters, False)
        output = self.__get_ports_from_parameters('output', parameters, True)
        return (input_, output)
    
    @staticmethod
    def __get_ports_from_parameters(prefix, parameters, 
                                    put_ports_into_input_ports_container):
        ports = IISPipelineConverter.__get_ports_from_configuration(
            prefix, parameters)
        for p in ports.keys():
            if p == prefix:
                ports[p] = '${'+prefix+'}'
            else:
                ports[p] = '${'+prefix+'_'+p+'}'
        node = None
        if len(ports) > 0:
            if put_ports_into_input_ports_container:
                node = Node(IISPipelineConverter.__IO_nodes_type, ports, {})
            else:
                node = Node(IISPipelineConverter.__IO_nodes_type, {}, ports)
        return node
    
    def convert_node(self, name, oozie_node):
        result = None
        if isinstance(oozie_node, SubworkflowAction):
            result = self.__handle_subworkflow(oozie_node)
        elif isinstance(oozie_node, JavaAction):
            result = self.__handle_java_action(oozie_node)
        elif isinstance(oozie_node, StreamingMapReduceAction):
            result = self.__handle_mapreduce_action(
                                    oozie_node, 'StreamingMapReduceAction')
        elif isinstance(oozie_node, JavaMapReduceAction):
            result = self.__handle_java_mapreduce_action(oozie_node)
        elif isinstance(oozie_node, PigAction):
            result = self.__handle_pig_action(oozie_node)
        elif isinstance(oozie_node, HiveAction):
            result = self.__handle_hive_action(oozie_node)
        elif isinstance(oozie_node, Decision):
            result =  None ##TODO
        else:
            result =  None
        if result is not None:
            importance = self.__get_importance(name)
            result.importance = importance
        return result
    
    @staticmethod
    def __get_importance(node_name):
        if node_name.startswith('skip-') or (node_name == 'generate-schema'):
            return NodeImportance.lowest
        elif node_name.startswith('transformers_'):
            return NodeImportance.low
        else:
            return NodeImportance.normal
    
    @staticmethod
    def __handle_subworkflow(node):
        input_ports = IISPipelineConverter.__get_ports_from_configuration(
            'input', node.configuration)
        output_ports = IISPipelineConverter.__get_ports_from_configuration(
            'output', node.configuration)
        return Node('SubworkflowAction', input_ports, output_ports)
    
    @staticmethod
    def __get_ports_from_configuration(type_prefix, configuration):
        """Retrieve ports definitions from configuration of the node.
        
        Name of the property has to be given explicitly by following the
        `$type_prefix_$some_name` pattern or be implicit by being defined as 
        `$type_prefix`. In the latter case it means that the port name is
        simply `$type_prefix`. `type_prefix` might be, e.g. "input".
        
        For illustration purposes, let's focus our further attention on 
        type_prefix equal "input". 
        
        If there is a property "input" defined among all properties, 
        definitions of other ports starting from 
        "input_" are not allowed since it is assumed that there is only
        one input port called "input".
        
        Args:
            type_prefix (string): either 'input' or 'output'
            configuration (Dict[string, string]): configuration dictionary
        
        Return:
            Dict[string, string]: Key is the name of the port while the value
                is the path assigned to it.
        """
        keys = configuration.keys()
        expected_prefix = '{}_'.format(type_prefix)
        prefixed_keys = [k for k in keys if k.startswith(expected_prefix)]
        if (type_prefix in keys):
            if len(prefixed_keys) > 0:
                raise Exception('Among the configuration properties, there '
                    'was a property called "{}". Nevertheless, some other '
                    'properties prefixed with "{}" were found '
                    ' ({}). This is not allowed.'.format(
                        type_prefix, expected_prefix, ', '.join(prefixed_keys)))
            return {type_prefix: configuration[type_prefix]}
        else:
            ports = {}
            for k in prefixed_keys:
                suffix = k[len(expected_prefix):]
                ports[suffix] = configuration[k]
        return ports
    
    @staticmethod
    def __handle_prefixed_args(args, input_prefix, output_prefix, node_type):
        input_ports = IISPipelineConverter.__get_ports_from_args(
                                                    args, input_prefix)
        output_ports = IISPipelineConverter.__get_ports_from_args(
                                                    args, output_prefix)
        return Node(node_type, input_ports, output_ports)
    
    @staticmethod
    def __handle_prefixed_args_with_implicit_port(
            args, input_type_prefix, output_type_prefix, type_prefix_separator, 
            node_type):
        input_ports = IISPipelineConverter.\
            __get_ports_from_args_with_implicit_port(
                                args, input_type_prefix, type_prefix_separator)
        output_ports = IISPipelineConverter.\
            __get_ports_from_args_with_implicit_port(
                                args, output_type_prefix, type_prefix_separator)
        return Node(node_type, input_ports, output_ports)
    
    @staticmethod
    def __handle_java_action(node):
        return IISPipelineConverter.__handle_prefixed_args(
                node.args, '-I', '-O', 'JavaAction')
    
    @staticmethod
    def __handle_pig_action(node):
        return IISPipelineConverter.\
            __handle_prefixed_args_with_implicit_port(
                node.params, 'input', 'output', '_', 'PigAction')

    @staticmethod
    def __handle_hive_action(node):
        return IISPipelineConverter.\
            __handle_prefixed_args_with_implicit_port(
                node.params, 'input', 'output', '_', 'HiveAction')
    
    @staticmethod
    def __get_ports_from_args(args, type_prefix):
        """Retrieve ports definitions from command line arguments of the node.
        
        Args:
            args (Array[string]): command line arguments of the Java node
            type_prefix (string): e.g. '-I' or '-O'
        
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
    def __get_ports_from_args_with_implicit_port( 
                args, type_prefix, type_prefix_separator):
        """Retrieve ports definitions from command line arguments of the node.
        
        When compared with method `__get_ports_from_args`, it handles
        implicit ports given in as command line arguments, e.g., "input".
        
        What is done here is analogous to what `__get_ports_from_configuration` 
        method does (see its Python doc).
        
        Args:
            args (Array[string]): command line arguments of the node
            type_prefix (string): e.g. 'input' or 'output'
            type_prefix_separator (string): separates type_prefix from the
                name of the port e.g. '_'
        
        Return:
            Dict[string, string]: Key is the name of the port while the value
                is the path assigned to it.
        """
        normal_ports = IISPipelineConverter.__get_ports_from_args(
                     args, '{}{}'.format(type_prefix, type_prefix_separator))
        single_port_prefix = '{}='.format(type_prefix)
        single_port_args = [a for a in args if a.startswith(single_port_prefix)]
        if len(single_port_args) > 1:
            raise Exception('More than one argument starting with "{}" '
                            'not allowed'.format(single_port_prefix))
        if len(single_port_args) == 1:
            elems = single_port_args[0].split('=')
            if len(elems) != 2:
                raise Exception('Argument "{}" found consisting of {} '
                                'elements separated by "=" and not 2'.format(
                                        a, len(elems)))
            if len(normal_ports) > 0:
                raise Exception('When argument prefixed with "{}" is defined '
                    'no other port definitions are allowed.'.format(
                                                        single_port_prefix))
            return {elems[0]: elems[1]}
        else:
            assert len(single_port_args) == 0
            return normal_ports
    
    @staticmethod
    def __handle_java_mapreduce_action(node):
        if 'avro.mapreduce.multipleoutputs' in node.configuration:
            return IISPipelineConverter.\
                __handle_java_mapreduce_multiple_outputs(node)
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