#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from pandas import Series, DataFrame

class Pyplyr(object):
    """Pyplyr"""
    def __init__(self, df):
        super(Pyplyr, self).__init__()
        self.__df = df

    def __str__(self):
        return self.__df.__str__()

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
        for new_col, assets in kwargs.items():
            target_col, func = assets
            val = func(self.__df[target_col])
            series = Series([val], name=new_col)
            series_list.append(series)
        return Pyplyr(pd.concat(series_list, axis=1))

    def data(self):
        """Called at end of method chains"""
        return self.__df
