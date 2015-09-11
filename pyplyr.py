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
        if isinstance(self.__df, GroupBy):
            self.__pp_group(self.__df)
        self.__df.__str__()

    def __pp_group(self, group):
        for key, df in group:
            print(key)
            print(df)

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
        for target_col, func in kwargs.items():
            val = func(self.__df[target_col])
            series = Series([val], name=target_col)
            series_list.append(series)
        return Pyplyr(pd.concat(series_list, axis=1))

    def data(self):
        """Called at end of method chains"""
        return self.__df
