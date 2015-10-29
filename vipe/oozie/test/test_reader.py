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

import vipe.oozie.reader
from vipe.oozie.graph_serialization import from_yaml

def test_simple_java_workflow():
    check('data/simple_java_workflow/workflow.xml', 
          'data/simple_java_workflow/expected.yaml')

def check(oozie_workflow_file_path, expected_yaml_file_path):
    oozie_workflow = __read_string(oozie_workflow_file_path)
    actual = vipe.oozie.reader.read(oozie_workflow)
    expected_yaml = __read_string(expected_yaml_file_path)
    expected = from_yaml(expected_yaml)
    assert expected == actual

def __read_string(relative_path):
    return resource_stream(__name__, relative_path).read().decode("utf-8")