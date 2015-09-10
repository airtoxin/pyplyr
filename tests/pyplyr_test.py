#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from nose.tools import ok_, eq_

from pyplyr import Pyplyr
from pandas import DataFrame

class PyplyrPublicMethodsTestCase(TestCase):
    def setUp(self):
        self.df = DataFrame([
            [0,  1,  2,  3,  4],
            [5,  6,  7,  8,  9],
            [10, 11, 12, 13, 14],
            [15, 16, 17, 18, 19],
            [20, 21, 22, 23, 24]
        ], columns=["col0", "col1", "col2", "col3", "col4"])
        self.pyplyr = Pyplyr(self.df)
    def tearDown(self):
        self.df = None
        self.pyplyr = None

    def test_constructor(self):
        ok_(self.pyplyr._Pyplyr__df is self.df)

    def test_select_with_single_col(self):
        sel_list = "col1"
        selected = self.pyplyr.select(sel_list)._Pyplyr__df
        expected = self.df[[sel_list]]
        is_ok = (selected == expected).all().all()
        ok_(is_ok)

    def test_select_with_multi_col(self):
        sel_list = ["col1", "col4"]
        selected = self.pyplyr.select(sel_list)._Pyplyr__df
        expected = self.df[sel_list]
        is_ok = (selected == expected).all().all()
        ok_(is_ok)

    def test_data(self):
        ok_(self.pyplyr.data() is self.df)
