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
from vipe.graphviz.simplified_dot_graph.graph import SimplifiedDotGraph
from vipe.graphviz.image_converter import ImageConverter


class TestConversionToImage:
    def test_convert_various_cases_to_image(self):
        convert_to_images('data/converter/pipeline_with_various_cases.yaml')
    
    def test_convert_incorrect_dot_format_to_image(self):
        dot_with_port_not_defined_earlier = """
        digraph{
        "node1":"port1" -> "node2"
        }
        """
        with pytest.raises(Exception):
            ImageConverter(dot_with_port_not_defined_earlier).to_image()
            
        dot_without_wrapping = """
        node1 -> node2
        """
        with pytest.raises(Exception):
            ImageConverter(dot_without_wrapping).to_image()

class TestProducedDotGraphsWithVariusDetailLevels:
    def test_various_cases_highest_detail_with_input_and_output(self):
        check('data/converter/pipeline_with_various_cases_dot_versions/highest_detail_level_with_input_and_output.dot',
              'data/converter/pipeline_with_various_cases.yaml',
              DetailLevel.highest, True, True)
    
    def test_various_cases_highest_detail_with_output(self):
        check('data/converter/pipeline_with_various_cases_dot_versions/highest_detail_level_with_output.dot',
              'data/converter/pipeline_with_various_cases.yaml',
              DetailLevel.highest, False, True)
    
    def test_various_cases_highest_detail(self):
        check('data/converter/pipeline_with_various_cases_dot_versions/highest_detail_level.dot',
              'data/converter/pipeline_with_various_cases.yaml',
              DetailLevel.highest, False, False)
    
    def test_various_cases_medium_detail_with_input_and_output(self):
        check('data/converter/pipeline_with_various_cases_dot_versions/medium_detail_level_with_input_and_output.dot',
              'data/converter/pipeline_with_various_cases.yaml',
              DetailLevel.medium, True, True)
    
    def test_various_cases_lowest_detail_with_input_and_output(self):
        check('data/converter/pipeline_with_various_cases_dot_versions/lowest_detail_level_with_input_and_output.dot',
              'data/converter/pipeline_with_various_cases.yaml',
              DetailLevel.lowest, True, True)

def convert_to_images(pipeline_path):
    dot = {}
    dot['low'] = convert_to_dot(pipeline_path, 
                   detail_level=DetailLevel.lowest, 
                   show_input_ports=False, show_output_ports=False)
    dot['medium'] = convert_to_dot(pipeline_path, 
                   detail_level=DetailLevel.medium, 
                   show_input_ports=False, show_output_ports=False)
    dot['medium_io'] = convert_to_dot(pipeline_path, 
                   detail_level=DetailLevel.medium, 
                   show_input_ports=True, show_output_ports=True)
    dot['high'] = convert_to_dot(pipeline_path, 
                   detail_level=DetailLevel.highest, 
                   show_input_ports=True, show_output_ports=True)
    for name, dot_str in dot.items():
        try:
            converter = ImageConverter(dot_str)
            converter.to_image()
        except:
            print('Error while processing "{}" version.'.format(name))
            raise

def check(expected_dot_path, pipeline_path, detail_level, 
                   show_input_ports=False, show_output_ports=False):
    actual_dot = convert_to_dot(pipeline_path, detail_level, 
                   show_input_ports, show_output_ports)
    actual = SimplifiedDotGraph.from_dot(actual_dot)
    expected_dot = read_as_string(__name__, expected_dot_path)
    expected = SimplifiedDotGraph.from_dot(expected_dot)
    assert expected == actual, '{} != {}'.format(expected, actual)  

def convert_to_dot(pipeline_file_relative_path, detail_level=DetailLevel.medium, 
                   show_input_ports=False, show_output_ports=False):
    pipeline_yaml = read_as_string(__name__, pipeline_file_relative_path)
    pipeline = Pipeline.from_yaml_dump(pipeline_yaml)
    dot_converter = Converter(detail_level, show_input_ports, show_output_ports)
    return dot_converter.run(pipeline)