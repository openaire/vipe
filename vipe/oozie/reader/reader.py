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

import xml.etree.ElementTree as ET
import sys
import re
from vipe.oozie.graph import OozieGraph
from vipe.oozie.reader.handlers import handle_fork, handle_decision, \
    handle_action, handle_join, handle_start, handle_end, handle_kill
from vipe.oozie.reader.utils import properties_to_dict

def read(xml_string):
    """ Read Oozie XML workflow definition

    Args:
        xml_string (string): Oozie XML

    Returns:
        OozieGraph
    """
    root = ET.fromstring(__remove_namespaces(xml_string))
    ignore_tags = ['global']
    independently_handled_tags = ['parameters']
    handlers_register = {'fork': handle_fork, 
                         'decision': handle_decision,
                         'action': handle_action,
                         'join': handle_join,
                         'start': handle_start,
                         'end': handle_end,
                         'kill': handle_kill}
    
    nodes_register = {}
    parameters = {}
    for child in root:
        tag_name = child.tag
        if tag_name not in (list(handlers_register.keys()) + \
                            independently_handled_tags + ignore_tags):
            raise Exception('tag "{}" encountered which is neither '\
                'ignored nor handled'.format(tag_name))
        if tag_name in ignore_tags:
            pass
        elif tag_name in independently_handled_tags:
            if tag_name == 'parameters':
                parameters = properties_to_dict(child)
        else:
            try:
                (name, node) = handlers_register[tag_name](child)
                nodes_register[name] = node
            except Exception:
                tag_string = ET.tostring(child, encoding='utf8', method='xml')
                print('Error occurred while analyzing tag "{}"'.\
                    format(tag_string), file=sys.stderr)
                raise
    return OozieGraph(parameters, nodes_register)

def __remove_namespaces(xml_string):
    ## We don't care about namespaces, so we remove them. Analyzing the XML with
    ## the namespace information is more difficult than without it.
    xml_string_no_namespaces1= re.sub('xmlns="[^"]+"', '', xml_string)
    xml_string_no_namespaces2= re.sub("xmlns='[^']+'", "", 
                                     xml_string_no_namespaces1)
    return xml_string_no_namespaces2
