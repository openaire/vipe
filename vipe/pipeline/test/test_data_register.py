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
from vipe.pipeline.pipeline import Pipeline
from vipe.pipeline.pipeline_data import PipelineData

def test_simple():
    check('data/pipeline_simple.yaml', 
          {'${workingDir}/producer/person': {
                'producers': ['producer:person'],
                'consumers': ['mr_cloner:input']},
           '${workingDir}/producer/document': { 
                'producers': ['producer:document'],
                'consumers': []},
           '${workingDir}/mr_cloner/age': {
                'producers': ['mr_cloner:age'],
                'consumers': []},
           '${workingDir}/mr_cloner/person': {
                'producers': ['mr_cloner:person'],
                'consumers': ['cloner:person']},
           '${workingDir}/cloner/person':{
                'producers': ['cloner:person'],
                'consumers': ['consumer:person']}})

def test_multiple_consumers_and_producers():
    check('data/pipeline_multiple_consumers_and_producers.yaml', 
          {'${workingDir}/producer/person': {
                'producers': ['producer:person'],
                'consumers': ['mr_cloner:input', 'java_cloner:person']},
           '${workingDir}/cloner/person': {
                'producers': ['mr_cloner:person', 'java_cloner:person'],
                'consumers': ['consumer:person']}})

def check(pipeline_file_path, data_dict):
    pipeline_yaml = read_as_string(__name__, pipeline_file_path)
    pipeline = Pipeline.from_yaml_dump(pipeline_yaml)
    actual_data = PipelineData.from_pipeline(pipeline)
    expected_data = PipelineData.from_basic_data_types(data_dict)
    assert expected_data == actual_data