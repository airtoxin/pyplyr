#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Pyplyr(object):
    """Pyplyr"""
    def __init__(self, df):
        super(Pyplyr, self).__init__()
        self.__df = df

    def select(self, names):
        """SQL: SELECT clause"""
        if isinstance(names, str): names = [names]
        return Pyplyr(self.__df[names])

    def data(self):
        """Called at end of method chains"""
        return self.__df
