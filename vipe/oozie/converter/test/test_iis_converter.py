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
from vipe.oozie.graph import OozieGraph
from vipe.pipeline.pipeline import Pipeline
from vipe.oozie.converter.iis import IISPipelineConverter
from vipe.oozie.converter.converter import convert

def test_bypass():
    check_from_data_dir('bypass')

def test_conditional():
    check_from_data_dir('conditional')

def test_distcp():
    check_from_data_dir('distcp')

def test_fork():
    check_from_data_dir('fork')

def test_fs():
    check_from_data_dir('fs')

def test_generatesschema():
    check_from_data_dir('generateschema')

def test_global_section():
    check_from_data_dir('global_section')

def test_hadoopstreaming():
    check_from_data_dir('hadoopstreaming')

def test_hive():
    check_from_data_dir('hive')

def test_i_o_paths_parameters():
    check_from_data_dir('i_o_paths_parameters')

def test_java():
    check_from_data_dir('java')

def test_javamapreduce():
    check_from_data_dir('javamapreduce')

def test_javamapreduce_multipleoutput():
    check_from_data_dir('javamapreduce_multipleoutput')

def test_pig():
    check_from_data_dir('pig')

def test_subworkflow():
    check_from_data_dir('subworkflow')

def test_java_with_reserved_node_name_lowercase():
    check_from_data_dir('java_with_reserved_node_name_lowercase')
     
def test_java_with_reserved_node_name_uppercase():
    with pytest.raises(Exception):
        convert_oozie_yaml_to_pipeline('../../test/data/{}/workflow.yaml'\
                              .format('java_with_reserved_node_name_uppercase'))

def check_from_data_dir(dir_name):
    check('../../test/data/{}/workflow.yaml'.format(dir_name), 
          '../../test/data/{}/pipeline.yaml'.format(dir_name))

def convert_oozie_yaml_to_pipeline(oozie_workflow_file_path):
    oozie_yaml = read_as_string(__name__, oozie_workflow_file_path)
    oozie_graph = OozieGraph.from_yaml_dump(oozie_yaml)
    pipeline = convert(oozie_graph, IISPipelineConverter())
    return pipeline

def check(oozie_workflow_file_path, expected_pipeline_file_path):
    actual_pipeline = convert_oozie_yaml_to_pipeline(oozie_workflow_file_path)
    expected_pipeline_yaml = read_as_string(__name__, expected_pipeline_file_path)
    expected = Pipeline.from_yaml_dump(expected_pipeline_yaml)
    assert expected == actual_pipeline, 'expected={},\nactual={}'\
                                            .format(expected, actual_pipeline)