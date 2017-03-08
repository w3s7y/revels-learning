#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 08:10:30 2017

Does database IO for the revels training project.
Also has a basic cli class for interactive data addition to dbase.

@author: ben
"""
import sys
import sqlalchemy
import psycopg2
import pandas

USE = """dbase.py [db host] [db port] [username] [password] [db name]"""

class dbconnection:
    """Main database class, maintains the connection to the dbase."""
    def __init__(self, host, port, user, password, dbname):
        self.engine = sqlalchemy.create_engine(
        'postgresql+psycopg2://' + user + ':' + password + 
        '@' + host + ':' + port + '/' + dbname)
        self.dbconn = self.engine.connect()
        
    def getConnection(self):
        return self.dbconn

    def writeShop(self, shop_name, address1, address2, address3, postcode):
        pass
    
    def writeBag(self, shop_id, mass, price):
        pass
    
    def writeSample(self, bag_id, type_id, mass, density, height, width, depth):
        pass
    
class cli:
    """Command line interface for entering data"""
    help = """Available commands: 
        help      = this help text.
        addshop   = add a shop to the db.
        addbag    = add a bag to the db.
        addsample = add a individual sample to the db.
        quit      = Not sure what this does, undocumented...
For additional help on each function, use help <function name>."""

    def __init__(self, dbc):
        self.dbc = dbc
        
    def doHelp(self, *args):
        print(self.help)
    
    def doAddShop(self, options):
        shop_help = '''Adds a shop to the database.
        '''
        if options[0] == help:
            print(shop_help)
    
    def doAddBag(self, options):
        pass
    
    def doAddSample(self, options):
        pass
        
    def runCli(self):
        cmd = ''
        while cmd != 'quit':
            cmd = input('$$$ ')
            cmd = cmd.split(' ')
        
            if cmd[0] == 'addshop':
                self.doAddShop(cmd[1:])
            elif cmd[0] == 'addbag':
                self.doAddBag(cmd[1:])
            elif cmd[0] == 'addsample':
                self.doAddSample(cmd[1:])
            elif cmd[0] == 'help':
                self.doHelp(cmd[1:])                
            elif cmd[0] == 'quit':
                break
            else:
                print('Invalid input')
    
if __name__ == '__main__':
    
    if len(sys.argv) != 6:
        print(USE)
        quit
    
    dbc = dbconnection(sys.argv[1], sys.argv[2], sys.argv[3],
                       sys.argv[4], sys.argv[5])
    cli = cli(dbc)
    cli.runCli()