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

from io import StringIO

class PortName:
    def __init__(self, label, internal_name):
        """Args:
            label (string): name of the label to be displayed
            internal_name (string): name of the label used internally in the 
                definition of the dot format. It is unique for given node.
        """
        self.label = label
        self.internal_name = internal_name

class PortsLabelPrinter:
    """Creates a dot format label that shows node's ports."""
    
    def __init__(self):
        self.__s = None
    
    def __pr(self, text):
        print(text, file=self.__s)
    
    def run(self, labels, input_port_names, output_port_names, color):
        """Args:
            labels (List[string]): list of labels to be printed in the node. 
                Each label is placed in a separate line.
            input_port_names (List[PortName]): input port names
            output_port_names (List[PortName]): output port names
            color (string): value taken from
                http://graphviz.org/doc/info/colors.html
        """
        self.__s = StringIO()
        height = max(len(input_port_names), len(output_port_names), len(labels))
        self.__pr('<')
        self.__pr('<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">')
        self.__pr('  <TR>')
        self.__print_ports(input_port_names, height, True)
        self.__pr('    <TD ROWSPAN="{}" BGCOLOR="{}" BORDER="1">{}</TD>'\
                    .format(height, color, '<BR/>'.join(labels)))
        self.__print_ports(output_port_names, height, False)
        self.__pr('  </TR>')
        self.__pr('</TABLE>>')
        return self.__s.getvalue()
    
    def __print_ports(self, port_names, height, are_input_ports):
        if len(port_names) == 0:
            return
        self.__pr('    <TD ROWSPAN="{}">'.format(height))
        self.__pr('      <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">')
        for port in port_names:
            label = None
            align = None
            if are_input_ports:
                label = '&#9654; {}'.format(port.label)
                align = 'LEFT'
            else:
                label = '{} &#9654;'.format(port.label)
                align = 'RIGHT'
            self.__pr('        <TR><TD ALIGN="{}" PORT="{}">{}</TD></TR>'.\
                      format(align, port.internal_name, label))
        for _ in range(height-len(port_names)):
            self.__pr('        <TR><TD BORDER="0"> </TD></TR>')
        self.__pr('      </TABLE>')
        self.__pr('    </TD>')
