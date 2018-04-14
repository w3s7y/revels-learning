#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 11:52:41 2017

This module contains the main code to train a model.

@author: ben
"""
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import sklearn.model_selection
import logging

logging.basicConfig(level=logging.INFO)


class ValidationSplitter:
    def __init__(self, database_connection, validation_split):
        '''Accepts a revels.dbase.connection object and a validation split value
        (as a fraction, e.g. 0.2 = 20% validation data.)'''
        self.data_set = database_connection.get_revels()

        # Split by column into independant (X) and dependant (Y) vars.
        # These 2 statements carve the data_set into 2 DataFrames.
        # X = independant vars (mass, density, height, width, depth)
        # Y = dependant var (revels_type)
        self.X = self.data_set.iloc[:, 5:]  # From colindex 5 to end of table.
        self.Y = self.data_set.iloc[:, 4]  # Col 4 only.

        # Split data_set into training and validation data.
        self.X_train, self.X_test, self.Y_train, self.Y_test = sklearn.model_selection.train_test_split(
            self.X, self.Y,
            test_size=validation_split,
            random_state=7)


models = [('Logistic Regression', LogisticRegression()),
          ('Decision Tree', DecisionTreeClassifier()),
          ('K Nearest Neighbours', KNeighborsClassifier()),
          ('Linear Discriminant', LinearDiscriminantAnalysis()),
          ('Naive Bayes', GaussianNB()),
          ('Support Vector Machines', SVC())]


def validate_models(data_connection):
    """
    Performs a K-Fold X-Validation (whatever that is?)
    :param data_connection: dbase.connection object
    :return: None, it prints to stdout.
    """
    data = ValidationSplitter(data_connection, 0.1)
    k_fold = sklearn.model_selection.KFold(n_splits=3, random_state=7)
    results = []
    for name, model in models:
        logging.info("Performing cross validation on {}".format(name))
        meta = sklearn.model_selection.cross_val_score(model, data.X_train, data.Y_train,
                                                       cv=k_fold, scoring='accuracy')
        results.append((name, meta))


def persist_model_to_db(db, model, metadata):
    db.write_model_to_db(model, metadata)


def predict():
    pass
