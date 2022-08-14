# typedload
# Copyright (C) 2021 Salvo "LtWorf" Tomaselli
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


import os
from time import monotonic as time
from typing import Generator, Tuple, Any
from tempfile import  mkstemp
import json
from contextlib import contextmanager

@contextmanager
def write_json_to_tmp_file(obj: Any) -> Generator[str, None, None]:
    """Returns a  a temporary (text) file after writing the argument to it as JSON"""
    _, file_name = mkstemp()
    with open(file_name, "w") as data_file:
        json.dump(obj, data_file)
    try:
        yield file_name
    finally:
        os.remove(file_name)



def timeit(f) -> Tuple[float, float]:
    '''
    f is a function taking no parameters.

    It gets called multiple times to try and reduce
    measure error.
    '''
    r = []
    for i in range(5):
        begin = time()
        f()
        end = time()
        r.append(end - begin)
    return min(r), max(r)
