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

import re
pattern_whitespace = re.compile(r'\s+')

def properties_to_dict(elem):
    """Take XML element containing properties and turn it into dictionary"""
    d = {}
    for child in elem:
        assert child.tag == 'property'
        name = get_text(child.find('name'))
        value = None
        value_elem = child.find('value')
        if value_elem is not None:
            value = value_elem.text.strip()
        d[name] = value
    return d

def get_text(elem):
    """Get the text content of the element and clean it up.
    
    Returns:
        string
    """
    stripped = elem.text.strip()
    return re.sub(pattern_whitespace, ' ', stripped)

def findall_to_text(elem, child_tag_name):
    """
    Returns:
        List[string]
    """
    return [get_text(e) for e in elem.findall(child_tag_name)]

def find_to_text(elem, child_tag_name):
    """
    Returns:
        string
    """
    return get_text(elem.find(child_tag_name))