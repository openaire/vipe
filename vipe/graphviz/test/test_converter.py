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

from vipe.common.utils import read_as_string
from vipe.graphviz.converter import Converter
from vipe.pipeline.pipeline import Pipeline
from vipe.graphviz.importance_score_map import DetailLevel

def test_reserved_word_as_node_name_lowercase():
    convert_to_dot('data/converter/pipeline_with_incorrect_node_name_lowercase.yaml')

def test_reserved_word_as_node_name_uppercase():
    with pytest.raises(Exception):
        convert_to_dot('data/converter/pipeline_with_incorrect_node_name_uppercase.yaml')

def convert_to_dot(pipeline_file_relative_path):
    pipeline_yaml = read_as_string(__name__, pipeline_file_relative_path)
    pipeline = Pipeline.from_yaml_dump(pipeline_yaml)
    dot_converter = Converter(DetailLevel.medium)
    return dot_converter.run(pipeline)