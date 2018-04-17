#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 14:48:11 2017

Provides single entry point to project.

@author: ben
"""
import sys
import logging
import dbase
import training

logging.basicConfig(level=logging.INFO)


def predict():
    logging.info("Enter the mass (g) of the sample:")
    mass = sys.stdin.readline()
    logging.info("Enter the density (g/cm3) of the sample:")
    density = sys.stdin.readline()
    logging.info("Enter the height (mm) of the sample:")
    height = sys.stdin.readline()
    logging.info("Enter the width (mm) of the sample:")
    width = sys.stdin.readline()
    logging.info("Enter the depth (mm) of the sample:")
    depth = sys.stdin.readline()
    logging.info("Predicting sample with following variables:\n"
                 "mass = {}"
                 "density = {}"
                 "height = {}"
                 "width = {}"
                 "depth = {}".format(mass, density, height, width, depth))
    logging.info(training.predict(mass, density, height, width, depth))


if __name__ == '__main__':
    # If the database cannot be found, create it & load the data
    if not dbase.database_exists():
        dbase.create_database()

    if sys.argv[1] == 'train':
        logging.info("Training machine learning models")
        training.train_models(sys.argv[2], True)

    elif sys.argv[1] == 'x-val-score':
        logging.info("Doing cross validation on models")
        training.validate_models(sys.argv[2])

    elif sys.argv[1] == 'validate':
        logging.info("Performing full validation")
        training.train_models(sys.argv[2], False)

    elif sys.argv[1] == 'summary':
        logging.info("Preparing data summary...")
        dbase.connection().log_summary()

    elif sys.argv[1] == 'results':
        logging.info("Getting best {} models from database.".format(sys.argv[2]))
        dbase.connection().log_results(sys.argv[2])

    elif sys.argv[1] == 'predict':
        predict()
    else:
        logging.error("Error parsing argument")
        sys.exit(1)
