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
import dbase

logging.basicConfig(level=logging.INFO)


def get_db_connection():
    return dbase.connection()


class ValidationSplitter:
    def __init__(self, db_connection, validation_split):
        """
        :param db_connection: dbase.connection object
        :param validation_split: The amount of data to keep back for validation of training (0.1 = 10% etc.)
        """
        self.data_set = db_connection.get_revels()

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


def validate_models():
    """
    Performs a K-Fold X-Validation (whatever that is?)
    :param data_connection: dbase.connection object
    :return: None, it prints to stdout.
    """
    data = ValidationSplitter(get_db_connection(), 0.1)
    k_fold = sklearn.model_selection.KFold(n_splits=3, random_state=7)
    for name, model in models:
        logging.info("Performing cross validation on {}".format(name))
        x_val_score = sklearn.model_selection.cross_val_score(model, data.X_train, data.Y_train,
                                                       cv=k_fold, scoring='accuracy')
        learn_curve = sklearn.model_selection.learning_curve(model, data.X_train, data.Y_train,
                                                             cv=k_fold, scoring='accuracy')
        logging.info(learn_curve)
        logging.info("{} accuracy: {} ({})".format(name, x_val_score.mean(), x_val_score.std()))


def train_models():
    pass


def predict():
    pass
