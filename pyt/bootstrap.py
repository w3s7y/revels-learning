#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 14:48:11 2017

Provides single entry point to project for first time users.

@author: ben
"""
import sys
from dbase import connection as connection
from sqlalchemy.dialects import postgresql

# This is the main database user that will be created and
sci_user = 'scienceuser'
sci_pass = 'scienceuser'
create_user = "create user %s with login password '%s'" \
    % (sci_user, sci_pass)



def doDataLoad():
    dbc = connection('revelslearning_postgres_1', '5432',
                     'postgres', 'postgres', 'postgres')
    con = dbc.get_connection()
    con.execute(create_user)
    print('user %s created with password %s' % (sci_user, sci_pass))
    # Open the .sql file
    sql = open('psql/create_db.sql','r').readlines()
    sql_command = ''
    for line in sql:
        sql_command = sql_command + line
    con.execute(sql_command)
 
    con.close()
    dbc.close()
    print('Created database...')
    dbc = connection('revelslearning_postgres_1', '5432',
                     'postgres', 'postgres', 'sciencedbase')
    con = dbc.get_connection()
    sql = open('psql/dbdump.sql','r').readlines()
    sql_command = ''
    for line in sql:
        sql_command = sql_command + line
    con.execute(sql_command)
    con.close()
    dbc.close()
    return

def doTrainModel():
    pass

def doShowSummary():
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
    elif arg == 'do-show-summary':
        doShowSummary()
    elif arg == 'do-show-results':
        doResultsPrint()
    elif arg == 'do-predict-revel':
        doPrediction()
    else:
        print('Error parsing argument')
