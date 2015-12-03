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

import pytest

from  vipe.oozie.converter.iis import PortsFromConfigurationRetriever

def test_simple():
    conf = {'input_document': '1', 'output_document': '2', 'input_person': '3'}
    check('input', conf, {'document': '1', 'person': '3'})
    check('output', conf, {'document': '2'})

def test_single_prefix():
    conf = {'input': '1', 'input_document': '2', 'output': '3'}
    check('output', conf, {'output': '3'})
    with pytest.raises(Exception):
        PortsFromConfigurationRetriever.run('input', conf)

def test_root_ports():
    conf = {'output_metadataimport_root': 'meta_root', 
            'metadataimport_output_name_document_meta': 'doc_meta',
            'metadataimport_output_name_document_content': 'doc_content',
            'output_unrelated_port': 'whatevs',
            'output_person_root': 'person_root',
            'person_output_name_name': 'name'}
    check('output', conf, {'metadataimport_document_meta': 'meta_root/doc_meta',
                           'metadataimport_document_content': 'meta_root/doc_content',
                           'unrelated_port': 'whatevs',
                           'person_name': 'person_root/name'})

def test_root_port_with_missing_port_names():
    conf = {'output_person_root': 'person_root',
            'output_unrelated_port': 'whatevs'}
    with pytest.raises(Exception):
        PortsFromConfigurationRetriever.run('output', conf)

def check(type_prefix, configuration, expected):
    actual = PortsFromConfigurationRetriever.run(type_prefix, configuration)
    assert expected == actual