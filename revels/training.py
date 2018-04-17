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
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import sklearn.model_selection
import logging
import dbase

logging.basicConfig(level=logging.DEBUG)

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


def get_models():
    return [('Logistic_Regression', LogisticRegression()),
          ('Decision_Tree', DecisionTreeClassifier()),
          ('K_Nearest_Neighbours', KNeighborsClassifier()),
          ('Linear_Discriminant', LinearDiscriminantAnalysis()),
          ('Naive_Bayes', GaussianNB()),
          ('Support_Vector_Machines', SVC())]


def validate_models(validation_split):
    """
    Performs cross validation on the models
    :param data_connection: dbase.connection object
    :return: None, it prints to stdout.
    """
    con = dbase.connection()
    data = ValidationSplitter(con, float(validation_split))
    k_fold = sklearn.model_selection.KFold(n_splits=10, random_state=7)
    for name, model in get_models():
        logging.info("Performing cross validation on {}".format(name))
        x_val_score = sklearn.model_selection.cross_val_score(model, data.X_train, data.Y_train,
                                                              cv=k_fold, scoring='accuracy')
        logging.debug("{}\n{}".format(name, x_val_score))
        logging.info("{} x_val mean (std dev): {} ({})".format(name, x_val_score.mean(), x_val_score.std()))
    # Close connection
    con.get_connection().close()


def train_models(validation_split, persist):
    con = dbase.connection()
    data = ValidationSplitter(con, float(validation_split))
    accuracy = []
    confusion = []
    classification = []
    for name, model in get_models():
        logging.info("Training {}".format(name))
        model.fit(data.X_train, data.Y_train)
        logging.info("Training complete, performing predictions on validation data")
        predictions = model.predict(data.X_test)
        score = accuracy_score(predictions, data.Y_test)
        confu = confusion_matrix(predictions, data.Y_test)
        classi = classification_report(predictions, data.Y_test)
        accuracy.append((name, score))
        confusion.append((name, confu))
        classification.append((name, classi))
        if persist:
            con.write_model_to_db(name, model, score,
                                  {"validataion_split": validation_split,
                                   "confusion_matrix": confu,
                                   "classification_rep": classi})

    for x in confusion:
        logging.info("Confusion Matrix for {} using validation split {}:\n{}".format(x[0], validation_split, x[1]))
    for x in classification:
        logging.info("Classification Report for {} validation split {}:\n{}".format(x[0], validation_split, x[1]))
    for x in accuracy:
        logging.info("Accuracy Score for {} validation split {}:\n{}".format(x[0], validation_split, x[1]))

    con.get_connection().close()


def predict(mass, density, height, width, depth):
    con = dbase.connection()
    model = con.get_best_model()
    con.get_connection().close()
    return model.predict([mass, density, height, width, depth])
