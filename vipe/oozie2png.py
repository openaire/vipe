# Copyright 2013-2016 University of Warsaw
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

from vipe.oozie.reader.reader import read as oozie_read
from vipe.oozie.converter.converter import convert as oozie_convert
from vipe.oozie.converter.iis import IISPipelineConverter
from vipe.graphviz.converter import Converter as PipelineConverter
from vipe.graphviz.image_converter import ImageConverter


def convert_oozie_to_dot(xml_oozie_string, detail_level,
                         show_input_ports, show_output_ports,
                         vertical_orientation):
    """Convert XML Oozie workflow definition to a graph described in DOT format.

    See docstring for `convert_oozie_to_png` function for description of
    parameters.

    Return:
        string
    """
    oozie_graph = oozie_read(xml_oozie_string)
    pipeline = oozie_convert(oozie_graph, IISPipelineConverter())
    dot_converter = PipelineConverter(detail_level,
                                      show_input_ports, show_output_ports,
                                      vertical_orientation)
    dot_string = dot_converter.run(pipeline)
    return dot_string


def convert_oozie_to_png(xml_oozie_string, detail_level,
                         show_input_ports, show_output_ports,
                         vertical_orientation,
                         dot_program_path='/usr/bin/dot'):
    """Convert XML Oozie workflow definition to a PNG image

    Args:
        xml_oozie_string (string): Oozie XML
        detail_level (DetailLevel): level of presentation details
        show_input_ports (bool):
        show_output_ports (bool):
        vertical_orientation (bool): True if the graph should be drawn
            from top to bottom, False if it should be drawn from left to
            right.
        dot_program_path (string): path to the 'dot' program

    Return:
        byte string
    """
    dot_string = convert_oozie_to_dot(xml_oozie_string, detail_level,
                                      show_input_ports, show_output_ports,
                                      vertical_orientation)
    dot_processor = ImageConverter(dot_string, dot_program_path)
    image = dot_processor.to_image()
    return image
