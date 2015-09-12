#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyplyr import Pyplyr
from pandas import (
    Series,
    DataFrame
)
from pandas.core.groupby import GroupBy
from pandas.util.testing import (
    assert_series_equal,
    assert_frame_equal
)

class TestPyplyr(object):
    def setup(self):
        self.columns = [
            "label1", "col0", "col1",
            "col2", "col3", "col4"
        ]
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

    def test_data(self):
        result = self.pyplyr.data()
        assert_frame_equal(result, self.df)

    def test_select(self):
        cols = ["col1", "label1"]
        result = self.pyplyr.select(*cols)
        assert isinstance(result, Pyplyr)
        result_df = result._Pyplyr__df
        expected = self.df.ix[:, cols]
        assert_frame_equal(result_df, expected)

    def test_filter_with_default(self):
        result = self.pyplyr.filter(
            label1=lambda x: x == "hoge",
            col1=lambda x: x > 10
        )
        assert isinstance(result, Pyplyr)
        result_df = result._Pyplyr__df
        expected = self.df.ix[[0,2,3,4], :]
        assert_frame_equal(result_df, expected)

    def test_filter_with_or_operator(self):
        result = self.pyplyr.filter(
            operator="or",
            label1=lambda x: x == "hoge",
            col1=lambda x: x > 10
        )
        assert isinstance(result, Pyplyr)
        result_df = result._Pyplyr__df
        expected = self.df.ix[[0,2,3,4], :]
        assert_frame_equal(result_df, expected)

    def test_filter_with_and_operator(self):
        result = self.pyplyr.filter(
            operator="and",
            label1=lambda x: x == "hoge",
            col1=lambda x: x > 10
        )
        assert isinstance(result, Pyplyr)
        result_df = result._Pyplyr__df
        expected = self.df.ix[[2,4], :]
        assert_frame_equal(result_df, expected)

    def test_summarize(self):
        result = self.pyplyr.summarize(
            col0=sum,
            col1=len,
            label1=lambda iter: len([i for i in iter if i == "hoge"])
        )
        assert isinstance(result, Pyplyr)
        result_df = result._Pyplyr__df
        assert len(result_df.columns) == 3
        assert result_df["col0"].equals(Series([50], name="col0"))
        assert result_df["col1"].equals(Series([5], name="col1"))
        assert result_df["label1"].equals(Series([3], name="label1"))

    def test_group_by(self):
        result = self.pyplyr.group_by("label1")
        df = result._Pyplyr__df
        assert isinstance(result, Pyplyr)
        assert isinstance(df, GroupBy)
        assert len(df) == 2

        for key, group_df in df:
            if key == "fuga":
                assert key == "fuga"
                expected = group_df.ix[[1, 3], group_df.columns]
            else:
                assert key == "hoge"
                expected = group_df.ix[[0, 2, 4], group_df.columns]
            assert_frame_equal(group_df, expected)
