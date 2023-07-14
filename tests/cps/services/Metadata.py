# -*- coding: utf-8 -*-

#  This file is part of the Calibre-Web (https://github.com/janeczku/calibre-web)
#    Copyright (C) 2021 OzzieIsaacs
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.

# 从calibre-web复制出来，方便测试使用
import abc
import dataclasses
import os
from typing import Dict, List, Optional, Union


@dataclasses.dataclass
class MetaSourceInfo:
    id: str
    description: str
    link: str


@dataclasses.dataclass
class MetaRecord:
    id: Union[str, int]
    title: str
    authors: List[str]
    url: str
    source: MetaSourceInfo
    cover: str = os.path.join("", 'generic_cover.jpg')
    description: Optional[str] = ""
    series: Optional[str] = None
    series_index: Optional[Union[int, float]] = 0
    identifiers: Dict[str, Union[str, int]] = dataclasses.field(default_factory=dict)
    publisher: Optional[str] = None
    publishedDate: Optional[str] = None
    rating: Optional[int] = 0
    languages: Optional[List[str]] = dataclasses.field(default_factory=list)
    tags: Optional[List[str]] = dataclasses.field(default_factory=list)


class Metadata:
    __name__ = "Generic"
    __id__ = "generic"

    def __init__(self):
        self.active = True

    def set_status(self, state):
        self.active = state

    @abc.abstractmethod
    def search(
            self, query: str, generic_cover: str = "", locale: str = "cn"
    ) -> Optional[List[MetaRecord]]:
        pass
