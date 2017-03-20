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
import pandas

USE = """dbase.py [db host] [db port] [username] [password] [db name]"""


class connection:
    """Main database class, maintains the connection to the dbase."""
    def __init__(self, host, port, user, password, dbname):
        connectStr = 'postgresql+psycopg2://' + user + ':' + password + '@' + \
            host + ':' + port + '/' + dbname

        self.engine = sqlalchemy.create_engine(connectStr)
        self.dbconn = self.engine.connect()

    def get_connection(self):
        '''Returns the raw sqlalchemy datbase connection.'''
        return self.dbconn

    def writeshop(self, shop_name, address1, address2, address3, postcode):
        '''Write a shop to the DB.'''
        self.dbconn.execute('insert into revels.shops (shop_name,' +
                            'address_1, address_2, address_3, postcode) ' +
                            'values (%s, %s, %s, %s, %s)',
                            shop_name,
                            address1,
                            address2,
                            address3,
                            postcode)

    def writebag(self, shop_id, mass, price):
        '''Write a bag to the DB.'''
        self.dbconn.execute("insert into revels.bags " +
                            "(shop_bought, total_mass, price) " +
                            "values (%s, %s, %s)",
                            shop_id,
                            mass,
                            price)

    def writesample(self,
                    bag_id, type_id, mass, density, height, width, depth):
        '''Write a row of sample data to the DB.'''
        self.dbconn.execute("insert into revels.data " +
                            "(bag_id, type_id, mass, density, height, " +
                            "width, depth) values " +
                            "(%s, %s, %s, %s, %s, %s, %s)",
                            bag_id,
                            type_id,
                            mass,
                            density,
                            height,
                            width,
                            depth)

    def get_shops(self):
        '''Returns a pandas DataFrame of the shops table.'''
        return pandas.read_sql_table('shops', self.dbconn,
                                     schema='revels')

    def get_bags(self):
        '''Returns a pandas DataFrame of the bags table.'''
        return pandas.read_sql_table('bags', self.dbconn,
                                     schema='revels')

    def get_types(self):
        '''Returns a pandas DataFrame of the types table.'''
        return pandas.read_sql_table('types', self.dbconn,
                                     schema='revels')

    def get_samples(self):
        '''Returns a pandas DataFrame of the data table.'''
        return pandas.read_sql_table('data', self.dbconn,
                                     schema='revels')

    def get_revels(self):
        '''Returns the pandas object of the revels_detail view.'''
        return pandas.read_sql_table('revels_detail', self.dbconn,
                                     schema='revels')


class cli:
    """Command line interface for entering data"""
    main_help = """Available functions:
        help      = this help text.
        addshop   = add a shop to the db.
        addbag    = add a bag to the db.
        addsample = add a individual sample to the db.
        listtypes = lists revels typs and their database IDs.
        listshops = lists shops and their database IDs.
        listbags  = lists bags and their database IDs.
        quit      = Not sure what this does, undocumented...
For additional help on each function, use help <function name>."""

    sample_help = '''
        addsample [bag id] [type id] [mass] [density] [height] [width] [depth]
        '''

    shop_help = '''
        addshop [shop_name] [address 1] [address 2] [address 3] [postcode]
        '''

    bag_help = '''
        addbag [shop id] [mass] [price]
        '''

    sample_help = '''
        addsample [bag id] [type id] [mass] [density] [height] [width] [depth]
        '''

    def __init__(self, dbc):
        self.dbc = dbc

    def doHelp(self, *args):
        try:
            argument = args[0][0]
        except IndexError:
            print(self.main_help)
            return

        if argument == 'addshop':
            print(self.shop_help)
        elif argument == 'addbag':
            print(self.bag_help)
        elif argument == 'addsample':
            print(self.sample_help)
        else:
            print(self.main_help)

    def doAddShop(self, options):
        if len(options) == 5:
            self.dbc.writeshop(options[0], options[1], options[2],
                               options[3], options[4])
            print('Like a boss!')
        else:
            print('Unknown length of options, please try \'help addshop\'')

    def doAddBag(self, options):
        if len(options) == 3:
            self.dbc.writebag(options[0], options[1], options[2])
            print('Like a boss!')
        else:
            print('Unknown length of options, please try \'help addbag\'')

    def doAddSample(self, options):
        if len(options) == 7:
            self.dbc.writesample(options[0], options[1], options[2],
                                 options[3], options[4], options[5],
                                 options[6])
            print('Like a boss!')
        else:
            print('Unknown length of options, please try \'help addsample\'')

    def listtypes(self):
        print(self.dbc.gettypes())

    def listbags(self):
        print(self.dbc.getbags())

    def listshops(self):
        print(self.dbc.getshops())

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
            elif cmd[0] == 'listtypes':
                self.listtypes()
            elif cmd[0] == 'listbags':
                self.listbags()
            elif cmd[0] == 'listshops':
                self.listshops()
            elif cmd[0] == 'quit':
                break
            else:
                print('Invalid input')

if __name__ == '__main__':

    if len(sys.argv) != 6:
        print(USE)
        exit()

    dbc = connection(sys.argv[1], sys.argv[2], sys.argv[3],
                     sys.argv[4], sys.argv[5])
    cli = cli(dbc)
    cli.runCli()
