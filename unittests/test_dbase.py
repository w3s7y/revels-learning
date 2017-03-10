#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 11:26:31 2017

pytest module for testing dbase module.

@author: ben
"""
import pyt.dbase as dbase
import secrets

db = dbase.dbconnection(secrets.hostname, secrets.port, 
                        secrets.databaseUser, secrets.databasePassword, 
                        secrets.dbname)

def test_database_connection():
    con = db.getconnection()
    assert str(type(con)) == '<class \'sqlalchemy.engine.base.Connection\'>' 

def test_get_types_returns_correct_panas_object_shape():
    results = db.gettypes()
    assert results.shape == (6,2)
    
def test_get_shops_returns_correct_pandas_object_shape():
    results = db.getshops()
    assert results.shape == (2,6)
