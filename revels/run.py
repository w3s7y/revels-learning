#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 14:48:11 2017

Provides single entry point to project.

@author: ben
"""
import sys
import os
import logging
import dbase
import training

logging.basicConfig(level=logging.INFO)
db_host = os.environ.get('REVELS_DB_HOST', 'postgres')
db_port = os.environ.get('REVELS_DB_PORT', '5432')
db_user = os.environ.get('REVELS_DB_USER', 'scienceuser')
db_pass = os.environ.get('REVELS_DB_PASS', 'sciencepass')
db_name = os.environ.get('REVELS_DB_NAME', 'revels')
db_schema = os.environ.get('REVELS_DB_SCHEMA', 'revels')

def test_for_revels_database():
    try:
        c = dbase.connection(db_host, db_port, db_user, db_pass, db_name, db_schema)
        c.get_bags()
        return True
    except Exception as e:
        logging.error(e)
        return False


def train_models():
    training.train_and_validate_models(dbase.connection(db_host, db_port, db_user, db_pass, db_name, db_schema))

def validate_models():
    training.validate_models(dbase.connection(db_host, db_port, db_user, db_pass, db_name, db_schema))

def show_summary():
    logging.info("Preparing data summary...")
    c = dbase.connection(db_host, db_port, db_user, db_pass, db_name, db_schema)
    revels_dataframe = c.get_samples().drop(columns=['id', 'bag_id', 'type_id'])
    logging.info("\n{}".format(revels_dataframe.describe()))


def print_results():
    pass


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



if __name__ == '__main__':
    # If the database cannot be found, create it & load the data
    if not test_for_revels_database():
        dbase.create_database(False)

    if sys.argv[1] == 'train-models':
        train_models()
    elif sys.argv[1] == 'validate':
        validate_models()
    elif sys.argv[1] == 'summary':
        show_summary()
    elif sys.argv[1] == 'results':
        print_results()
    elif sys.argv[1] == 'predict':
        predict()
    else:
        print('Error parsing argument')
        sys.exit(1)
