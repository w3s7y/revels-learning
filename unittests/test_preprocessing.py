#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 12:56:02 2017

@author: ben
"""
import pyt.preprocessing as pre
import pyt.dbase as dbase
import secrets as thesecret

secrets = thesecret.secretprovider(2)

db = dbase.connection(secrets.hostname, secrets.port,
                      secrets.databaseUser, secrets.databasePassword,
                      secrets.dbname)

parser = pre.parser(db, 0.2)


def test_dataset_type_is_DataFrame():
    assert str(type(parser.dataset)) == \
              '<class \'pandas.core.frame.DataFrame\'>'


def test_X_type_is_DataFrame():
    assert str(type(parser.X)) == \
              '<class \'pandas.core.frame.DataFrame\'>'


def test_Y_type_is_Series():
    assert str(type(parser.Y)) == \
              '<class \'pandas.core.series.Series\'>'


def test_X_train_type_is_DataFrame():
    assert str(type(parser.X_train)) == \
              '<class \'pandas.core.frame.DataFrame\'>'


def test_X_test_type_is_DataFrame():
    assert str(type(parser.X_test)) == \
              '<class \'pandas.core.frame.DataFrame\'>'


def test_Y_train_type_is_Series():
    assert str(type(parser.Y_train)) == \
              '<class \'pandas.core.series.Series\'>'


def test_Y_test_type_is_Series():
    assert str(type(parser.Y_test)) == \
              '<class \'pandas.core.series.Series\'>'


def test_dataset_shape():
    assert parser.dataset.shape[1] == 10


def test_training_indeps_shape():
    assert parser.X_train.shape[1] == 5


def test_validation_indeps_shape():
    assert parser.X_test.shape[1] == 5


def test_indeps_size():
    assert len(parser.X_train) + len(parser.X_test) == len(parser.X)


def test_deps_size():
    assert len(parser.Y_train) + len(parser.Y_test) == len(parser.Y)


def test_all_training_indep_vars_in_original_dataset():
    pass


def test_all_validation_indep_vars_in_original_dataset():
    pass


def test_all_training_dep_vars_in_original_dataset():
    pass


def test_all_validation_dep_vars_in_original_dataset():
    pass
