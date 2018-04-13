#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 09:11:29 2017

Secret provider which... provides secrets.

@author: ben
"""


class secretprovider:
    def __init__(self, switch):
        if switch == 1:
            self.databaseUser = 'xxxx'
            self.databasePassword = 'xxxx'
            self.hostname = 'xxxx'
            self.port = 'xxx'
            self.dbname = 'xxxx'
        elif switch == 2:
            self.databaseUser = 'xxxx'
            self.databasePassword = 'xxxx'
            self.hostname = 'xxxx'
            self.port = 'xxx'
            self.dbname = 'xxxx'

    def dump(self):
        print('Database User = ' + self.databaseUser)
        print('Database Pass = ' + self.databasePassword)
        print('Database Host = ' + self.hostname)
        print('Database Post = ' + self.port)
        print('Database Name = ' + self.dbname)
