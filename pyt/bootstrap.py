#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 14:48:11 2017

Provides single entry point to project for first time users.

@author: ben
"""
import sys
from pyt.dbase import connection


def doDataLoad():
    dbc = connection('localhost', '5432', 'postgres', 'postgres', 'postgres')
    sqlfile = open('psql/dbdump.sql', 'r')
    sql = sqlfile.readlines()
    print(sql)
    return

def doTrainModel():
    pass


def doResultsPrint():
    pass


def doPrediction():
    pass

if __name__ == '__main__':
    arg = sys.argv[1]
    if arg == 'do-initial-dataload':
        doDataLoad()
    elif arg == 'do-train-model':
        doTrainModel()
    elif arg == 'do-show-results':
        doResultsPrint()
    elif arg == 'do-predict-revel':
        doPrediction()
    else:
        print('Error parsing argument')
