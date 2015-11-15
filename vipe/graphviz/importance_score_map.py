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

from enum import Enum

class DetailLevel(Enum):
    """Detail level of the presentation of a node in the graph."""
    highest = 1
    very_high = 2
    high = 3
    medium = 4
    low = 5
    lowest = 6 

class ImportanceScoreMap:
    """Turn NodeImportance into a score based on DetailLevel.
    
    The score says how visible object with given importance should be on 
    given detail level. The larger the number, the more prominent the object.
    
    The detail and importance values are aligned like this:
    
    detail        importance
    ------        ----------
    highest       lowest
    very_high     very_low
    high          low
    medium        normal
    low           n/a
    lowest        n/a
    
    This means that when, e.g., detail is set to:
    
    - `lowest`, then the consecutive importance values receive the following 
       scores: `lowest`: -5, `very_low`: -4, `low`: -3, `normal`: -2
    - `medium`, then the consecutive importance values receive the following 
       scores: `lowest`: -3, `very_low`: -2, `low`: -1, `normal`: 0
    - `very_high`, then the consecutive importance values receive the following 
       scores: `lowest`: -1, `very_low`: 0, `low`: 1, `normal`: 2
    """
    
    def __init__(self, detail_level):
        """Args:
            detail_level (DetailLevel):
        """
        self.__detail = detail_level
        
    def get_score(self, importance):
        """Args:
            importance (NodeImportance):
        """
        return importance.value - self.__detail.value
        