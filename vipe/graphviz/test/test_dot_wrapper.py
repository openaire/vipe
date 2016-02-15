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

import pytest

from vipe.graphviz.dot_wrapper import DotBuilderWrapper
from vipe.graphviz.importance_score_map import ImportanceScoreMap, DetailLevel
from vipe.pipeline.pipeline import Node


class TestDotBuilderWrapper:

    def test_nodes_with_the_same_name_are_disallowed(self):
        importance_map = ImportanceScoreMap(DetailLevel.medium)
        builder = DotBuilderWrapper(importance_map, True, True)
        builder.add_node('n1', Node('Java', {}, {}))
        builder.add_node('n2', Node('Java', {}, {}))
        with pytest.raises(Exception):
            builder.add_node('n1', 'Java', Node({}, {}))
