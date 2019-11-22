# typedload
# Copyright (C) 2018-2019 Salvo "LtWorf" Tomaselli
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

from enum import Enum
from typing import Dict, FrozenSet, List, NamedTuple, Optional, Set, Tuple, Union
import unittest
import sys

if sys.version_info.minor >= 8 :
    from typing import Literal

from typedload import typechecks


class TestChecks(unittest.TestCase):

    def test_is_literal(self):
        if sys.version_info.minor >= 8 :
            l = Literal[1, 2, 3]
            assert typechecks.is_literal(l)

        assert not typechecks.is_literal(3)
        assert not typechecks.is_literal(int)
        assert not typechecks.is_literal(str)
        assert not typechecks.is_literal(None)
        assert not typechecks.is_literal(List[int])

    def test_is_typeddict(self):
        if sys.version_info.minor >= 8 :
            class A(TypedDict):
                val: str
            assert typechecks.is_typeddict(A)

        assert not typechecks.is_typeddict(int)
        assert not typechecks.is_typeddict(3)
        assert not typechecks.is_typeddict(str)
        assert not typechecks.is_typeddict({})
        assert not typechecks.is_typeddict(dict)
        assert not typechecks.is_typeddict(set)
        assert not typechecks.is_typeddict(None)
        assert not typechecks.is_typeddict(List[str])

    def test_is_list(self):
        assert typechecks.is_list(List)
        assert typechecks.is_list(List[int])
        assert typechecks.is_list(List[str])
        assert not typechecks.is_list(list)
        assert not typechecks.is_list(Tuple[int, str])
        assert not typechecks.is_list(Dict[int, str])
        assert not typechecks.is_list([])

    def test_is_dict(self):
        assert typechecks.is_dict(Dict[int, int])
        assert typechecks.is_dict(Dict)
        assert typechecks.is_dict(Dict[str, str])
        assert not typechecks.is_dict(Tuple[str, str])
        assert not typechecks.is_dict(Set[str])

    def test_is_set(self):
        assert typechecks.is_set(Set[int])
        assert typechecks.is_set(Set)

    def test_is_frozenset_(self):
        assert not typechecks.is_frozenset(Set[int])
        assert typechecks.is_frozenset(FrozenSet[int])
        assert typechecks.is_frozenset(FrozenSet)

    def test_is_tuple(self):
        assert typechecks.is_tuple(Tuple[str, int, int])
        assert typechecks.is_tuple(Tuple)
        assert not typechecks.is_tuple(tuple)
        assert not typechecks.is_tuple((1,2))

    def test_is_union(self):
        assert typechecks.is_union(Optional[int])
        assert typechecks.is_union(Optional[str])
        assert typechecks.is_union(Union[bytes, str])
        assert typechecks.is_union(Union[str, int, float])

    def test_is_nonetype(self):
        assert typechecks.is_nonetype(type(None))
        assert not typechecks.is_nonetype(List[int])

    def test_is_enum(self):
        class A(Enum):
            BB = 3
        assert typechecks.is_enum(A)
        assert not typechecks.is_enum(Set[int])

    def test_is_namedtuple(self):
        A = NamedTuple('A', [
            ('val', int),
        ])
        assert typechecks.is_namedtuple(A)
        assert not typechecks.is_namedtuple(Tuple)
        assert not typechecks.is_namedtuple(tuple)
        assert not typechecks.is_namedtuple(Tuple[int, int])

    def test_is_forwardref(self):
        try:
            # Since 3.7
            from typing import ForwardRef  # type: ignore
        except ImportError:
            from typing import _ForwardRef as ForwardRef  # type: ignore
        assert typechecks.is_forwardref(ForwardRef('SomeType'))

    def test_uniontypes(self):
        assert typechecks.uniontypes(Optional[bool]) == {typechecks.NONETYPE, bool}
        assert typechecks.uniontypes(Optional[int]) == {typechecks.NONETYPE, int}
        assert typechecks.uniontypes(Optional[Union[int, float]]) == {typechecks.NONETYPE, float, int}
        assert typechecks.uniontypes(Optional[Union[int, str, Optional[float]]]) == {typechecks.NONETYPE, str, int, float}

        with self.assertRaises(ValueError):
            typechecks.uniontypes(Union[int])
