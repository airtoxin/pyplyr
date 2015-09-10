#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyplyr import Pyplyr
from pandas import Series, DataFrame

class TestPyplyr(object):
    def setup(self):
        self.columns = ["label1", "col0", "col1", "col2", "col3", "col4"]
        self.df = DataFrame([
            ["hoge", 0,  1,  2,  3,  4],
            ["fuga", 5,  6,  7,  8,  9],
            ["hoge", 10, 11, 12, 13, 14],
            ["fuga", 15, 16, 17, 18, 19],
            ["hoge", 20, 21, 22, 23, 24]
        ], columns=self.columns)
        self.pyplyr = Pyplyr(self.df)

    def teardown(self):
        self.columns = None
        self.df = None
        self.pyplyr = None

    def test_constructor(self):
        assert self.pyplyr._Pyplyr__df is self.df

    def test_select(self):
        cols = ["col1", "label1"]
        result = self.pyplyr.select(*cols)
        df = result._Pyplyr__df
        assert isinstance(result, Pyplyr)
        assert list(df.columns) == cols
        assert (df == self.df[cols]).all().all()

    def test_data(self):
        assert (self.pyplyr.data() == self.df).all().all()
        assert (self.pyplyr.data() is self.df)

    def test_filter_with_default(self):
        result = self.pyplyr.filter(
            label1=lambda x: x == "hoge",
            col1=lambda x: x > 10
        )
        df = result._Pyplyr__df
        assert isinstance(result, Pyplyr)
        assert set(df.columns) == set(self.df.columns)
        assert (df == self.df[Series([True, False, True, True, True])]).all().all()

    def test_filter_with_or_operator(self):
        result = self.pyplyr.filter(
            operator="or",
            label1=lambda x: x == "hoge",
            col1=lambda x: x > 10
        )
        df = result._Pyplyr__df
        assert isinstance(result, Pyplyr)
        assert set(df.columns) == set(self.df.columns)
        assert (df == self.df[Series([True, False, True, True, True])]).all().all()

    def test_filter_with_and_operator(self):
        result = self.pyplyr.filter(
            operator="and",
            label1=lambda x: x == "hoge",
            col1=lambda x: x > 10
        )
        df = result._Pyplyr__df
        assert isinstance(result, Pyplyr)
        assert set(df.columns) == set(self.df.columns)
        assert (df == self.df[Series([False, False, True, False, True])]).all().all()

    def test_summarize(self):
        result = self.pyplyr.summarize(
            c0sum=("col0", sum),
            c1cnt=("col1", len),
            hogecnt=("label1", lambda iter: len([i for i in iter if i == "hoge"]))
        )
        df = result._Pyplyr__df
        expected = DataFrame([[50, 5, 3]], columns=["c0sum", "c1cnt", "hogecnt"])
        assert isinstance(result, Pyplyr)
        assert set(df.columns) == set(["c0sum", "c1cnt", "hogecnt"])
        assert len(df) == 1
        assert df.c0sum[0] == 50
        assert df.c1cnt[0] == 5
        assert df.hogecnt[0] == 3
