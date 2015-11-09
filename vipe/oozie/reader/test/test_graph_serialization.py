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

from vipe.common.utils import read_as_string
from vipe.oozie.graph import OozieGraph

def test_simple_java_workflow():
    check('../../test/data/java/workflow.yaml')

def check(yaml_file_path):
    graph1 = OozieGraph.from_yaml_dump(read_as_string(__name__, yaml_file_path))
    yaml_str1 = graph1.to_yaml_dump()
    graph2 = OozieGraph.from_yaml_dump(yaml_str1)
    yaml_str2 = graph2.to_yaml_dump()
    assert yaml_str1 == yaml_str2
    assert graph1 == graph2
