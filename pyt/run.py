#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 14:48:11 2017

Provides single entry point to project for first time users.

@author: ben
"""
import sys
import os
from pyt.dbase import connection


def test_for_revels_database():
    db_host = os.environ.get('REVELS_DB_HOST', 'postgres')
    db_port = os.environ.get('REVELS_DB_PORT', '5432')
    db_user = os.environ.get('REVELS_DB_USER', 'scienceuser')
    db_pass = os.environ.get('REVELS_DB_PASS', 'sciencepass')
    db_name = os.environ.get('REVELS_DB_NAME', 'revels')
    try:
        c = connection(db_host, db_port, db_user, db_pass, db_name)
        c.get_bags()
        return True
    except Exception:
        return False


def create_revels_database():
    pass


def do_data_load():
    return


def train_model():
    pass


def show_summary():
    pass


def print_results():
    pass


def predict():
    pass


if __name__ == '__main__':
    # If the database cannot be found, create it & load the data
    if not test_for_revels_database():
        create_revels_database()
        do_data_load()

    if sys.argv[1] == 'train-models':
        train_model()
    elif sys.argv[1] == 'summary':
        show_summary()
    elif sys.argv[1] == 'results':
        print_results()
    elif sys.argv[1] == 'predict':
        predict()
    else:
        print('Error parsing argument')
        sys.exit(1)
