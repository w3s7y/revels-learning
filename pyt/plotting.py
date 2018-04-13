#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 13:16:05 2017

File which simply has nice convienience functions for creating various plots of
the dataset.

# Sample code to create a db connection and matrix_plot of all variables.
from pyt.dbase import connection
from pyt.plotting import plotter
dbc = connection('localhost','5432','scienceuser','scienceuser','sciencedbase')
p = plotter(dbc)
p.matrix_plot()


@author: ben
"""
from pandas.tools.plotting import scatter_matrix


class plotter:
    """Creates plots.  See main documentation."""

    def __init__(self, database_connection):
        self.data = database_connection.get_revels()
        self.cleaned_data = self.data.iloc[:, 4:]

    def matrix_plot(self):
        scatter_matrix(self.cleaned_data)

class model_evaluation:
    """Class which can evaluate which machine learning model is the best."""
    
    def __init__(self, database_connection):
        self.dbc = database_connection.get_connection()
