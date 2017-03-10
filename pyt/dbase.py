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
        
    def getconnection(self):
        '''Returns the raw sqlalchemy datbase connection.'''
        return self.dbconn

    def writeshop(self, shop_name, address1, address2, address3, postcode):
        '''Write a shop to the DB.'''
        pass
    
    def writebag(self, shop_id, mass, price):
        pass
    
    def writesample(self, bag_id, type_id, mass, density, height, width, depth):
        pass
    
    def getshops(self):
        '''Returns a pandas DataFrame of the shops table.'''
        pass
    
    def getbags(self):
        '''Returns a pandas DataFrame of the bags table.'''
        pass
    
    def gettypes(self):
        '''Returns a pandas DataFrame of the types table.'''
        pass
    
    def getsamples(self):
        '''Returns a pandas DataFrame of the data table.'''
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
        shop_help = '''
        [shop name] [address 1] [address 2] [address 3] [county] [postcode]
        '''
        if options[0] == help:
            print(shop_help)
            return
            
        if len(options) == 6:
            self.dbc.writeshop(options[0], options[1], options[2], 
                               options[3], options[4], options[5])
    
    def doAddBag(self, options):
        bag_help = '''
        [shop id] [mass] [price]
        '''
        if len(options) == 1:
            if options[0] == 'help':
                print(bag_help)
                return
            
        if len(options) == 3:
            self.dbc.writebag(options[0], options[1], options[2])
    
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