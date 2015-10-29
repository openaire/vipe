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

from pkg_resources import resource_stream

from vipe.oozie.graph_serialization import from_yaml, to_yaml

def test_simple_java_workflow():
    check('data/simple_java_workflow/expected.yaml')

def check(yaml_file_path):
    graph1 = from_yaml(__read_string(yaml_file_path))
    yaml_str1 = to_yaml(graph1)
    graph2 = from_yaml(yaml_str1)
    yaml_str2 = to_yaml(graph2)
    assert yaml_str1 == yaml_str2
    assert graph1 == graph2

def __read_string(relative_path):
    return resource_stream(__name__, relative_path).read().decode("utf-8")
