# typedload
# Copyright (C) 2021-2022 Salvo "LtWorf" Tomaselli
#
# typedload is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>

import json
from typing import List, NamedTuple, Union
import sys

from common import timeit
from perftest.common import write_json_to_tmp_file


class Data(NamedTuple):
    data: List[Union[int, float]]


data = {'data': [i if i % 2 else float(i) for i in range(3000000)]}


with write_json_to_tmp_file(data) as data_file_path:
    if sys.argv[1] == '--typedload':
        from typedload import load
        def func():
            with open(data_file_path) as data_file:
                load(json.load(data_file), Data)
        print(timeit(func))

    elif sys.argv[1] == '--pydantic':
        import pydantic
        class DataPy(pydantic.BaseModel):
            data: List[Union[int, float]]
        print(timeit(lambda: pydantic.parse_file_as(DataPy, data_file_path)))
    elif sys.argv[1] == '--apischema':
        import apischema
        # apischema will return a pointer to the same list, which is a bug
        # that can lead to data corruption, but makes it very fast
        # so level the field by copying the list
        print(timeit(lambda: list(apischema.deserialize(Data, data))))
