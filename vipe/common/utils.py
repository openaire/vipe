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

def default_eq(self, other):
    """Default implementation of equality operator"""
    return (type(other) is type(self)) and (self.__dict__ == other.__dict__)

def read_as_string(_name_, relative_path):
    """Read file available at given `relative_path` to string.
    
    Args:
        _name_: `__name__` parameter of given module.
        relative_path: path to given file relative to given module position.
    
    Return:
        string: contents of the file as string
    """
    return resource_stream(_name_, relative_path).read().decode("utf-8")