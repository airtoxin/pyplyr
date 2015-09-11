#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import pandas as pd
from pandas import Series, DataFrame
from pandas.core.groupby import GroupBy

class Pyplyr(object):
    """Pyplyr"""
    def __init__(self, df):
        super(Pyplyr, self).__init__()
        self.__df = df

    def __repr__(self):
        strings = [str(self.__df)]
        if isinstance(self.__df, GroupBy):
            for key, df in self.__df:
                strings.append("GroupedDataFrame: " + key)
                strings.append(str(df))
        return "\n".join(strings)

    def select(self, *cols):
        return Pyplyr(self.__df[list(cols)])

    def filter(self, operator="or", **kwargs):
        if operator not in ("or", "and"): raise ValueError()

        total_mask = None
        for col, func in kwargs.items():
            mask = self.__df[col].map(func)
            if total_mask is None:
                total_mask = mask
                continue
            if operator is "or":
                total_mask = mask | total_mask
            elif operator is "and":
                total_mask = mask & total_mask

        return Pyplyr(self.__df[total_mask])

    def summarize(self, **kwargs):
        series_list = []
        if isinstance(self.__df, GroupBy):
            for group_key, df in self.__df:
                _series_list = []
                for target_col, func in kwargs.items():
                    val = func(df[target_col])
                    series = Series([val], index=[group_key], name=target_col)
                    _series_list.append(series)
                series_list.append(pd.concat(_series_list, axis=1))
            return Pyplyr(pd.concat(series_list, axis=0))
        else:
            for target_col, func in kwargs.items():
                val = func(self.__df[target_col])
                series = Series([val], name=target_col)
                series_list.append(series)
            return Pyplyr(pd.concat(series_list, axis=1))

    def group_by(self, *cols):
        return Pyplyr(self.__df.groupby(by=cols))

    def data(self):
        """Called at end of method chains"""
        return self.__df
