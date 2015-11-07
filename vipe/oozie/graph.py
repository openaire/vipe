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

import yaml

import vipe.common.serialization
from vipe.common.utils import default_eq

class OozieGraph(yaml.YAMLObject):
    """A structure corresponding directly to Oozie XML file"""
    yaml_tag = '!OozieGraph'
    
    def __init__(self, parameters, nodes):
        """
        Args:
            parameters (Dict[string, string]): the key
                is the node of parameter and the value is it's value.
            nodes (Dict[string, Node]): a dictionary mapping node of a node 
                to a Node object. The node with node 'start' is the one that 
                the workflow starts from.
        """
        self.parameters = parameters
        self.nodes = nodes
    
    def get_start(self):
        """
        Returns:
            a Node that is the starting node of the workflow
        """
        return self.nodes['start']
    
    def __eq__(self, other):
        return default_eq(self, other)
    
    def __str__(self):
        return self.to_yaml_dump()

    def to_yaml_dump(self):
        """Dump the graph to YAML.
        
        Note that intially I named this method `to_yaml()`, but this
        interfered with the YAML serialization process and this exception
        was thrown: "TypeError: to_yaml() takes 1 positional argument but 2 were given"
        """
        return vipe.common.serialization.to_yaml(self)
    
    @staticmethod
    def from_yaml_dump(yaml_string):
        """Read the graph from YAML dump."""
        return vipe.common.serialization.from_yaml(yaml_string)
        
class Node(yaml.YAMLObject):
    pass

class Action(Node):
    def __init__(self, ok_node, error_node, configuration):
        """
        Args:
            ok_node: node of Node object that is executed after this Action 
                if no errors occurred during execution.
            error_node: node of Node object that is executed after this Action 
                if an error occurred during execution.
            configuration (Dict[string, string]): the key is
                the node of configuration property and the value is the
                value of the configuration property.
        """
        self.ok_node = ok_node
        self.error_node = error_node
        self.configuration = configuration

    def __eq__(self, other):
        return default_eq(self, other)

class OtherAction(Action):
    """Action that is not recognized by the program"""
    yaml_tag = '!OtherAction'
    
    def __init__(self, ok_node, error_node, configuration, type_):
        """
        Args:
            type_ (string): node of the XML tag corresponding to this action
        """
        super().__init__(ok_node, error_node, configuration)
        self.type = type_

    def __eq__(self, other):
        return default_eq(self, other)

class SubworkflowAction(Action):
    yaml_tag = '!SubworkflowAction'
    
    def __init__(self, ok_node, error_node, configuration, app_path, 
                 propagate_configuration):
        """
        Args:
            app_path (string): path to subworkflow.
            propagate_configuration (bool): True if the node has option of
                propagating its configuration to subworkflow set, False
                otherwise.
        """
        super().__init__(ok_node, error_node, configuration)
        self.app_path = app_path
        self.propagate_configuration = propagate_configuration

    def __eq__(self, other):
        return default_eq(self, other)

class JavaAction(Action):
    yaml_tag = '!JavaAction'
    
    def __init__(self, ok_node, error_node, configuration, main_class,
                 args, captures_output):
        """
        Args:
            main_class (string): node of Java class with the `main` method.
            args (List[string]): contains command line arguments passed to 
            the `main` method.
            captures_output (bool): True if the node has option of 
                capturing output set, False otherwise.
        """
        super().__init__(ok_node, error_node, configuration)
        self.main_class = main_class
        self.args = args
        self.captures_output = captures_output

    def __eq__(self, other):
        return default_eq(self, other)

class StreamingMapReduceAction(Action):
    yaml_tag = '!StreamingMapReduceAction'
    
    def __init__(self, ok_node, error_node, configuration, mapper, reducer):
        """
        Args:
            mapper (string): command line call of the mapper program.
            reducer (string): command line call of the reducer program
        """
        super().__init__(ok_node, error_node, configuration)
        self.mapper = mapper
        self.reducer = reducer

    def __eq__(self, other):
        return default_eq(self, other)

class JavaMapReduceAction(Action):
    yaml_tag = '!JavaMapReduceAction'
    
    def __init__(self, ok_node, error_node, configuration):
        super().__init__(ok_node, error_node, configuration)

    def __eq__(self, other):
        return default_eq(self, other)

class PigAction(Action):
    yaml_tag = '!PigAction'
    
    def __init__(self, ok_node, error_node, configuration, 
                 script, params, arguments):
        """
        Args:
            script (string): path to the Pig script
            params (List[string]): parameters passed to the Pig script
            arguments (List[string]): arguments passed to the Pig script
        """
        super().__init__(ok_node, error_node, configuration)
        self.script = script
        self.params = params
        self.arguments = arguments

    def __eq__(self, other):
        return default_eq(self, other)

class HiveAction(Action):
    yaml_tag = '!HiveAction'
    
    def __init__(self, ok_node, error_node, configuration, 
                 script, params):
        """
        Args:
            script (string): path to the Hive script
            params (List[string]): parameters passed to the Hive script
        """
        super().__init__(ok_node, error_node, configuration)
        self.script = script
        self.params = params

    def __eq__(self, other):
        return default_eq(self, other)

class FSAction(Action):
    yaml_tag = '!FSAction'
    
    def __init__(self, ok_node, error_node):
        super().__init__(ok_node, error_node, {})

    def __eq__(self, other):
        return default_eq(self, other)

class DistCPAction(Action):
    yaml_tag = '!DistCPAction'
    
    def __init__(self, ok_node, error_node, from_, to):
        super().__init__(ok_node, error_node, {})
        self.from_ = from_
        self.to = to

    def __eq__(self, other):
        return default_eq(self, other)

class Fork(Node):
    yaml_tag = '!Fork'
    
    def __init__(self, nodes):
        """
        Args:
            nodes (List[string]): A list of names of Nodes.
        """
        self.nodes = nodes

    def __eq__(self, other):
        return default_eq(self, other)

class Join(Node):
    yaml_tag = '!Join'
    
    def __init__(self, next_):
        """
        Args:
            next (string): A node of Node that should be executed after this one.
        """
        self.next = next_

    def __eq__(self, other):
        return default_eq(self, other)

class Decision(Node):
    yaml_tag = '!Decision'
    
    def __init__(self, cases, default_node):
        """
        Args:
            cases (List[DecisionCase]):
            default_node (string): node of the default case node.
        """
        self.cases = cases
        self.default_node = default_node

    def __eq__(self, other):
        return default_eq(self, other)

class DecisionCase(yaml.YAMLObject):
    yaml_tag = '!DecisionCase'
    
    def __init__(self, condition, target):
        """
        Args:
            condition (string): switch condition.
            target (string): A node of Node that will be executed after the 
                condition is met.
        """
        self.condition = condition
        self.target = target

    def __eq__(self, other):
        return default_eq(self, other)

class Start(Node):
    yaml_tag = '!Start'
    
    def __init__(self, next_):
        """
        Args:
            next (string): A node of Node that should be executed after 
                this one.
        """
        self.next = next_

    def __eq__(self, other):
        return default_eq(self, other)

class End(Node):
    yaml_tag = '!End'

    def __eq__(self, other):
        return default_eq(self, other)

class Kill(Node):
    yaml_tag = '!Kill'

    def __eq__(self, other):
        return default_eq(self, other)
