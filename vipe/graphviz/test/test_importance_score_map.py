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

from vipe.graphviz.importance_score_map import ImportanceScoreMap, DetailLevel
from vipe.pipeline.pipeline import NodeImportance

def test_medium():
    check(DetailLevel.medium, {NodeImportance.lowest: -3, 
                               NodeImportance.very_low: -2,
                               NodeImportance.low: -1,
                               NodeImportance.normal: 0})

def test_highest():
    check(DetailLevel.highest, {NodeImportance.lowest: 0, 
                               NodeImportance.very_low: 1,
                               NodeImportance.low: 2,
                               NodeImportance.normal: 3})

def test_lowest():
    check(DetailLevel.lowest, {NodeImportance.lowest: -5, 
                               NodeImportance.very_low: -4,
                               NodeImportance.low: -3,
                               NodeImportance.normal: -2})

def check(detail_level, expected_importance_scores):
    map_ = ImportanceScoreMap(detail_level)
    for (importance, expected_score) in expected_importance_scores.items():
        actual_score = map_.get_score(importance)
        assert expected_score == actual_score

