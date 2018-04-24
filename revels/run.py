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


def predict(model_id):
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
    if model_id is not None:
        prediction, pred_name = training.predict_with(model_id, mass, density, height, width, depth)
    else:
        prediction, pred_name = training.predict(mass, density, height, width, depth)

    logging.info("Predicted type_id: {}".format(prediction[0]))
    logging.info("Predicted type: {}".format(pred_name))


if __name__ == '__main__':
    # If the database cannot be found, create it & load the data
    if not dbase.database_exists():
        dbase.create_database()

    if sys.argv[1] == 'train':
        logging.info("Training machine learning models")
        training.train_models(sys.argv[2], int(sys.argv[3]), True)

    elif sys.argv[1] == 'train-models':
        logging.info("Training machine learning models")
        for val_split in [.15, .18, .19, .2, .22, .24, .26, .265, .27, .275, .28, .285, .29, .3, .31, .32]:
            for rand_seed in [3, 5, 7, 9]:
                logging.info("Training models using validation split of {} and random seed {}"
                             .format(val_split, rand_seed))
                training.train_models(val_split, rand_seed, True)

    elif sys.argv[1] == 'x-val-score':
        logging.info("Doing cross validation on models")
        training.validate_models(sys.argv[2], sys.argv[3], sys.argv[4])

    elif sys.argv[1] == 'validate':
        logging.info("Performing full validation")
        training.train_models(sys.argv[2], int(sys.argv[3]), False)

    elif sys.argv[1] == 'summary':
        logging.info("Preparing data summary...")
        dbase.connection().log_summary().close()

    elif sys.argv[1] == 'results':
        logging.info("Getting best {} models from database.".format(sys.argv[2]))
        dbase.connection().log_results(sys.argv[2]).close()

    elif sys.argv[1] == 'best-model':
        logging.info("Getting best model and metadata from database")
        c = dbase.connection()
        result = c.get_best_model()
        meta = result[1]
        score = result[2]
        logging.info("Model Type: {}".format(type(result[0])))
        logging.info("Accuracy score: {}".format(score))
        for key in meta:
            logging.info("{}:\n{}".format(key, meta[key]))
        c.get_connection().close()

    elif sys.argv[1] == 'top-models':
        logging.info("Getting info on top {} trained models".format(sys.argv[2]))
        c = dbase.connection()
        counter = 1
        result = c.get_top_models(sys.argv[2])
        for model in result:
            logging.info("**** Rank {} ****".format(counter))
            logging.info("Model Id   : {}".format(model[4]))
            logging.info("Model Name : {}".format(model[3]))
            logging.info("Model Score: {}%".format(round(model[2]*100, 2)))
            counter = counter + 1
        c.get_connection().close()

    elif sys.argv[1] == 'get-model-by-id':
        logging.info("Getting info on model with id {}".format(sys.argv[2]))
        c = dbase.connection()
        result = c.get_model_by_id(sys.argv[2])
        score = result[2]
        name = result[3]
        meta = result[1]
        logging.info("Model Name: {}".format(name))
        logging.info("Accuracy score: {}".format(score))
        for key in meta:
            logging.info("{}:\n{}".format(key, meta[key]))
        c.get_connection().close()

    elif sys.argv[1] == 'predict-with':
        predict(sys.argv[2])
    elif sys.argv[1] == 'predict':
        predict(None)
    else:
        logging.error("Error parsing argument")
        sys.exit(1)
