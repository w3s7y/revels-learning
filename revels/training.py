#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 11:52:41 2017

This module contains the main code to train models, predict etc.

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
    def __init__(self, db_connection, validation_split, random_state):
        """
        :param db_connection: dbase.connection object
        :param validation_split: The amount of data to keep back for validation of training (0.1 = 10% etc.)
        :param random_state: The random_state to use in sklearn.model_selection.train_test_split
        """
        self.data_set = db_connection.get_revels()

        # Split by column into independant (X) and dependant (Y) vars.
        # These 2 statements carve the data_set into 2 DataFrames.
        # X = independant vars (mass, density, height, width, depth)
        # Y = dependant var (revels_type)
        self.X = self.data_set.iloc[:, 5:]  # From colindex 5 to end of view.
        self.Y = self.data_set.iloc[:, 4]  # Col 4 only.

        # Split data_set into training and validation data.
        self.X_train, self.X_test, self.Y_train, self.Y_test = sklearn.model_selection.train_test_split(
            self.X, self.Y,
            test_size=validation_split,
            random_state=random_state)


def get_models():
    return [('Logistic_Regression', LogisticRegression()),
            ('Decision_Tree', DecisionTreeClassifier()),
            ('K_Nearest_Neighbours', KNeighborsClassifier()),
            ('Linear_Discriminant', LinearDiscriminantAnalysis()),
            ('Naive_Bayes', GaussianNB()),
            ('Support_Vector_Machines', SVC())]


def validate_models(validation_split, kfold_splits, random_seed):
    """
    Performs cross validation on the models
    :param validation_split:
    :param kfold_splits:
    :param random_seed:
    :return:
    """
    con = dbase.connection()
    data = ValidationSplitter(con, float(validation_split), random_seed)
    k_fold = sklearn.model_selection.KFold(n_splits=int(kfold_splits), random_state=int(random_seed))
    for name, model in get_models():
        logging.info("Performing cross validation on {}".format(name))
        x_val_score = sklearn.model_selection.cross_val_score(model, data.X_train, data.Y_train,
                                                              cv=k_fold, scoring='accuracy')
        logging.debug("{}\n{}".format(name, x_val_score))
        logging.info("{} x_val mean (std dev): {} ({})".format(name, x_val_score.mean(), x_val_score.std()))
    # Close connection
    con.get_connection().close()


def train_models(validation_split, random_seed, persist):
    """
    :param validation_split: amount of validation data to keep back from training (0.2 = 20%)
    :param random_seed: random to use on validation split
    :param persist: boolean value to store trained models in db.
    :return: None
    """
    con = dbase.connection()
    accuracy = []
    confusion = []
    classification = []
    for name, model in get_models():
        logging.debug("Training {}".format(name))
        data = ValidationSplitter(con, float(validation_split), int(random_seed))

        # Train the model on the training data set.
        model.fit(data.X_train, data.Y_train)
        logging.debug("Training complete, performing predictions on validation data")

        # Create predictions on the test (validation) data.
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
                                   "validation_seed": random_seed,
                                   "confusion_matrix": confu,
                                   "classification_rep": classi})

    for x in confusion:
        logging.debug("Confusion Matrix for {} using validation split {}:\n{}".format(x[0], validation_split, x[1]))
    for x in classification:
        logging.debug("Classification Report for {} validation split {}:\n{}".format(x[0], validation_split, x[1]))
    for x in accuracy:
        logging.info("Accuracy Score for {} validation split {}:\n{}".format(x[0], validation_split, x[1]))

    con.get_connection().close()


def predict(mass, density, height, width, depth):
    """
    Predict using best available model in database.
    :param mass: The sample mass (in g)
    :param density: Sample density (g/cm3)
    :param height: (mm)
    :param width: (mm)
    :param depth: (mm)
    :return: the prediction (type_id) of revel
    """
    con = dbase.connection()
    model = con.get_best_model()
    logging.info("Using best available model {} with accuracy score of {}%".format(model[3], round(model[2]*100, 2)))
    prediction = model[0].predict([[mass, density, height, width, depth]])
    logging.debug("Predicted type_id: {}".format(prediction[0]))
    revel_type = con.get_connection().execute("SELECT * FROM types WHERE id = {}".format(prediction[0])).fetchone()
    logging.debug(revel_type[1])
    con.get_connection().close()
    return prediction, revel_type[1]


def predict_with(model_id, mass, density, height, width, depth):
    """
    Predict using specific model in database.
    :param model_id: Specific model to use in predictions.
    :param mass: The sample mass (in g)
    :param density: Sample density (g/cm3)
    :param height: (mm)
    :param width: (mm)
    :param depth: (mm)
    :return: the prediction (type_id) of revel
    """
    con = dbase.connection()
    logging.debug("Getting model with id {}".format(model_id))
    model = con.get_model_by_id(model_id)
    logging.info("Using model of type: {} with accuracy score of {}%".format(model[3], round(model[2]*100, 2)))
    prediction = model[0].predict([[mass, density, height, width, depth]])
    for x in prediction:
        logging.debug(x)
    logging.debug("Predicted type_id: {}".format(prediction[0]))
    revel_type = con.get_connection().execute("SELECT * FROM types WHERE id = {}".format(prediction[0])).fetchone()
    logging.debug(revel_type[1])
    con.get_connection().close()
    return prediction, revel_type[1]
