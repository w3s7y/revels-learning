#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 11:26:31 2017

pytest module for testing dbase module.

@author: ben
"""
import pyt.dbase as dbase
import secrets as thesecret

secrets = thesecret.secretprovider(2)

db = dbase.connection(secrets.hostname, secrets.port,
                      secrets.databaseUser, secrets.databasePassword,
                      secrets.dbname)


def test_database_connection():
    con = db.get_connection()
    assert str(type(con)) == '<class \'sqlalchemy.engine.base.Connection\'>'


def test_get_types_returns_correct_pandas_shape():
    results = db.get_types()
    assert results.shape == (6, 2)


def test_insert_into_shops():
    db.writeshop('Poundland', 'Pride Hill Shopping Centre', 'Shrewsbury',
                 'Shropshire', 'SY1 2SD')


def test_insert_into_bags():
    db.writebag(1, 112, 1)


def test_insert_into_data():
    db.writesample(1, 1, 1.12, 1.6, 2.5, 0.2, 0.65)
    db.writesample(1, 2, 2.42, 0.5, 1.25, 1.2, 0.35)
    db.writesample(1, 3, 0.62, 1.2, 1.15, 0.2, 0.47)
    db.writesample(1, 4, 2.12, 2, 0.25, 1.2, 0.25)
    db.writesample(1, 5, 1.74, 1.01, 0.85, 1.2, 2.165)
    db.writesample(1, 6, 1.37, 1.00, 0.55, 1.2, 1.35)


def test_get_shops_returns_pandas_dataframe():
    obj = db.get_shops()
    assert str(type(obj)) == '<class \'pandas.core.frame.DataFrame\'>'


def test_get_bags_returns_pandas_dataframe():
    obj = db.get_bags()
    assert str(type(obj)) == '<class \'pandas.core.frame.DataFrame\'>'


def test_get_types_returns_pandas_dataframe():
    obj = db.get_types()
    assert str(type(obj)) == '<class \'pandas.core.frame.DataFrame\'>'


def test_get_samples_returns_pandas_dataframe():
    obj = db.get_samples()
    assert str(type(obj)) == '<class \'pandas.core.frame.DataFrame\'>'


def test_get_revels_returns_pandas_dataframe():
    obj = db.get_revels()
    assert str(type(obj)) == '<class \'pandas.core.frame.DataFrame\'>'