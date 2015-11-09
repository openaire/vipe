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

import os.path

from vipe.common.utils import read_as_string
from vipe.pipeline.pipeline import Pipeline
from vipe.graphviz.low_score_nodes_remover import LowScoreNodesRemover
from vipe.graphviz.importance_score_map import ImportanceScoreMap, DetailLevel

def test_separated():
    check_changed('separated')

def test_no_input():
    check_changed('no_input')

def test_no_input_not_lowest():
    check_no_changes('no_input_not_lowest')

def test_no_output():
    check_changed('no_output')

def test_no_output_not_lowest():
    check_no_changes('no_output_not_lowest')

def test_lowest_with_input_and_output():
    check_no_changes('lowest_with_input_and_output')

def test_output_going_nowhere():
    """ The case when the output of a node is not connected to anything.
    
    The node should probably be removed, but is not in the current 
    implementation.
    """
    check_no_changes('output_going_nowhere')

def check_changed(dir_name):
    path = ['data', 'low_score_nodes_remover', dir_name]
    src_dir = os.path.join(*(path + ['pipeline.yaml']))
    pipeline_yaml = read_as_string(__name__, src_dir)
    pipeline = Pipeline.from_yaml_dump(pipeline_yaml)
    remover = LowScoreNodesRemover(ImportanceScoreMap(DetailLevel.medium))
    actual = remover.run(pipeline)
    expected_yaml = read_as_string(__name__, 
                                   os.path.join(*(path + ['expected.yaml'])))
    expected = Pipeline.from_yaml_dump(expected_yaml)
    assert expected == actual

def check_no_changes(dir_name):
    src_dir = os.path.join('data', 'low_score_nodes_remover', 
                           dir_name, 'pipeline.yaml')
    pipeline_yaml = read_as_string(__name__, src_dir)
    pipeline = Pipeline.from_yaml_dump(pipeline_yaml)
    remover = LowScoreNodesRemover(ImportanceScoreMap(DetailLevel.medium))
    actual = remover.run(pipeline)
    assert pipeline == actual