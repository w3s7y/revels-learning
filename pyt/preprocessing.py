#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 11:52:34 2017

Data pre-processing module.  Creates the vectors and splits
into training and validation datasets etc..

@author: ben
"""
from sklearn.model_selection import train_test_split


class parser:
    """Data parser object."""
    def __init__(self, database_connection, validation_split):
        '''Accepts a pyt.dbase.connection object and a validation split value
        (as a fraction, e.g. 0.2 = 20% validation data.)'''
        self.dbc = database_connection
        self.dataset = self.dbc.get_revels()

        # Split by column into independant (X) and dependant (Y) vars.
        # These 2 statements carve the dataset into 2 DataFrames.
        # X = independant vars (mass, density, height, width, depth)
        # Y = dependant var (revels_type)
        self.X = self.dataset.iloc[:, 5:]  # From colindex 5 to end of table.
        self.Y = self.dataset.iloc[:, 4]   # Col 4 only.

        # Split dataset into training and validation data.
        self.X_train, self.X_test,\
            self.Y_train, self.Y_test = train_test_split(
                self.X, self.Y,
                test_size=validation_split,
                random_state=0)
