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

from vipe.oozie2png import convert_oozie_to_dot, convert_oozie_to_png
from vipe.common.utils import read_as_string
from vipe.graphviz.importance_score_map import DetailLevel
from vipe.graphviz.simplified_dot_graph.graph import SimplifiedDotGraph


class TestEndToEndGenerateImages:
    """Integration-like end-to-end tests.

    The tests check if the whole processing path: from reading Oozie XML to
    generating image file works at all. It's not checked whether a reasonable
    output is generated.
    """

    def test_complex_workflow(self):
        self.__convert_to_images(
            '../../examples/complex_workflow/workflow.xml')

    def test_iis_preprocessing_main_workflow(self):
        self.__convert_to_images(
            '../../examples/iis_workflows/preprocessing-main.xml')

    def test_iis_primary_main_workflow(self):
        self.__convert_to_images(
            '../../examples/iis_workflows/primary-main.xml')

    def test_iis_primary_processing_workflow(self):
        self.__convert_to_images(
            '../../examples/iis_workflows/primary-processing.xml')

    @staticmethod
    def __convert_to_images(oozie_file_path):
        oozie_xml = read_as_string(__name__, oozie_file_path)
        vertical_orientation = False
        show_input_ports = True
        show_output_ports = True
        for detail_level in DetailLevel:
            TestEndToEndGenerateImages.__convert_to_image(oozie_file_path,
                                    oozie_xml, detail_level,
                                    show_input_ports, show_output_ports,
                                    vertical_orientation)
        detail_level = DetailLevel.highest
        show_input_ports = False
        show_output_ports = False
        TestEndToEndGenerateImages.__convert_to_image(oozie_file_path, 
                                    oozie_xml, detail_level,
                                    show_input_ports, show_output_ports,
                                    vertical_orientation)
        vertical_orientation = True
        TestEndToEndGenerateImages.__convert_to_image(oozie_file_path, 
                                    oozie_xml, detail_level,
                                    show_input_ports, show_output_ports,
                                    vertical_orientation)

    @staticmethod
    def __convert_to_image(oozie_file_path, oozie_xml, detail_level,
                           show_input_ports, show_output_ports,
                           vertical_orientation):
        try:
            convert_oozie_to_png(oozie_xml, detail_level,
                                 show_input_ports, show_output_ports,
                                 vertical_orientation)
        except:
            print('Error while processing file "{}" with '
                  'detail_level="{}", '
                  'show_input_ports="{}", show_output_ports="{}", '
                  'vertical_orientation="{}"'.
                  format(oozie_file_path, detail_level,
                         show_input_ports, show_output_ports,
                         vertical_orientation))
            raise


class TestEndToEndGenerateDot:
    """Integration-like end-to-end tests of creating dot files.

    The tests check if most of the processing path: from reading Oozie XML to
    generating dot file works as expected.
    """

    def test_complex_worfklow(self):
        oozie_xml_path = '../../examples/complex_workflow/workflow.xml'
        for (path, detail_level) in \
                [('data/complex-0_lowest_detail.dot', DetailLevel.lowest),
                 ('data/complex-1_low_detail.dot', DetailLevel.low),
                 ('data/complex-2_medium_detail.dot', DetailLevel.medium),
                 ('data/complex-3_high_detail.dot', DetailLevel.high),
                 ('data/complex-4_very_high_detail.dot', DetailLevel.very_high),
                 ('data/complex-5_highest_detail.dot', DetailLevel.highest)]:
            self.__check(path, oozie_xml_path, detail_level, True, True)

    @staticmethod
    def __check(expected_dot_path, oozie_xml_path, detail_level,
                show_input_ports=False, show_output_ports=False):
        actual_oozie_xml = read_as_string(__name__, oozie_xml_path)
        actual_dot = convert_oozie_to_dot(actual_oozie_xml, detail_level,
                                          show_input_ports, show_output_ports,
                                          True)
        actual = SimplifiedDotGraph.from_dot(actual_dot)
        expected_dot = read_as_string(__name__, expected_dot_path)
        expected = SimplifiedDotGraph.from_dot(expected_dot)
        assert expected == actual, 'Problem when analyzing file "{}", '\
            'namely: {} != {}'.format(expected_dot_path, expected, actual)
