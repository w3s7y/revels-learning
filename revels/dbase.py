#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 08:10:30 2017

Does database IO for the revels training project.
Also has a basic cli class for interactive data addition to dbase.

@author: ben
"""
import logging
import sqlalchemy
import pandas
import os
import pickle
import io

logging.basicConfig(level=logging.INFO)

db_host = os.environ.get('REVELS_DB_HOST', 'revels-db')
db_port = os.environ.get('REVELS_DB_PORT', '5432')
db_adm_usr = os.environ.get('REVELS_DB_ADMIN_USER', 'postgres')
db_adm_pass = os.environ.get('REVELS_DB_ADMIN_PASS', 'somepassword')
db_user = os.environ.get('REVELS_DB_USER', 'scienceuser')
db_pass = os.environ.get('REVELS_DB_PASS', 'sciencepass')
db_name = os.environ.get('REVELS_DB_NAME', 'revels')
db_schema = os.environ.get('REVELS_DB_SCHEMA', 'revels')


def database_exists():
    try:
        connect_str = 'postgresql+psycopg2://' + db_adm_usr + ':' + db_adm_pass + '@' + \
                      db_host + ':' + db_port + '/' + db_name
        engine = sqlalchemy.create_engine(connect_str)
        dbconn = engine.connect()
        logging.debug("database_exists returning True")
        dbconn.close()
        return True
    except Exception as e:
        logging.error(e)
        logging.debug("database_exists returning False")
        return False


def create_database():
    """
    Creates a DB and runs in sql/db.sql.
    :param drop: Drop any existing database (boolean)
    :return: None, were pretty verbose in the logger.
    """

    # Create connection to postgres DB as admin user to create top level objects.
    engine = sqlalchemy.create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(db_adm_usr, db_adm_pass, db_host,
                                                                                    db_port, 'postgres'))
    con = engine.connect()
    logging.info("Successfully connected to database 'postgres' as {}".format(db_adm_usr))

    # Drop existing database if requested.

    logging.info("Dropping database {}".format(db_name))
    con.execute("commit")
    con.execute("DROP SCHEMA IF EXISTS {} CASCADE".format(db_schema))
    con.execute("commit")
    con.execute("DROP DATABASE IF EXISTS {}".format(db_name))
    con.execute("commit")
    con.execute("DROP ROLE IF EXISTS {}".format(db_user))
    con.execute("commit")
    logging.info("Database {} successfully dropped.".format(db_name))

    # Create the application user
    con.execute(sqlalchemy.text("CREATE ROLE {} WITH LOGIN PASSWORD '{}'".format(db_user, db_pass)))
    logging.info("User {} created.".format(db_user))
    con.execute("commit")

    # Create the database
    con.execute(sqlalchemy.text("CREATE DATABASE {} WITH OWNER = {} TEMPLATE = template0 "
                                "ENCODING = 'UTF8' ".format(db_name, db_user)))
    con.execute("commit")
    logging.info("Database {} created.".format(db_name))

    # Disconnect from postgres and reconnect to revels database to create schema
    con.close()
    logging.info("Connection to database postgres closed.")
    engine = sqlalchemy.create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(db_adm_usr, db_adm_pass, db_host,
                                                                                    db_port, db_name))
    con = engine.connect()
    logging.info("Connection to {} as {} established, creating schema...".format(db_name, db_adm_usr))

    # Create the schema.
    logging.info("Creating tables, ACLs and performing data load.")
    con.execute(open('sql/db.sql', 'r').read())
    con.execute("commit")

    # Close off the connection.
    con.close()
    logging.info("Database creation complete.")


class connection:
    """Main database class, maintains the connection to the dbase."""

    def __init__(self):
        connect_str = 'postgresql+psycopg2://' + db_user + ':' + db_pass + '@' + \
                     db_host + ':' + db_port + '/' + db_name

        self.engine = sqlalchemy.create_engine(connect_str)
        self.dbconn = self.engine.connect()
        self.dbconn.execute("SET search_path = {}, pg_catalog".format(db_schema))
        self.dbconn.execute("commit")


    def get_connection(self):
        '''Returns the raw sqlalchemy datbase connection.'''
        return self.dbconn

    def write_shop(self, shop_name, address1, address2, address3, postcode):
        '''Write a shop to the DB.'''
        self.dbconn.execute('insert into revels.shops (shop_name,' +
                            'address_1, address_2, address_3, postcode) ' +
                            'values (%s, %s, %s, %s, %s)',
                            shop_name,
                            address1,
                            address2,
                            address3,
                            postcode)

    def write_bag(self, shop_id, mass, price):
        '''Write a bag to the DB.'''
        self.dbconn.execute("insert into revels.bags " +
                            "(shop_bought, total_mass, price) " +
                            "values (%s, %s, %s)",
                            shop_id,
                            mass,
                            price)

    def write_sample(self,
                     bag_id, type_id, mass, density, height, width, depth):
        '''Write a row of sample data to the DB.'''
        self.dbconn.execute("insert into revels.data " +
                            "(bag_id, type_id, mass, density, height, " +
                            "width, depth) values " +
                            "(%i, %i, %i, %i, %i, %i, %i)",
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
                                     schema=db_schema)

    def get_bags(self):
        '''Returns a pandas DataFrame of the bags table.'''
        return pandas.read_sql_table('bags', self.dbconn,
                                     schema=db_schema)

    def get_types(self):
        '''Returns a pandas DataFrame of the types table.'''
        return pandas.read_sql_table('types', self.dbconn,
                                     schema=db_schema)

    def get_samples(self):
        '''Returns a pandas DataFrame of the data table.'''
        return pandas.read_sql_table('data', self.dbconn,
                                     schema=db_schema)

    def get_revels(self):
        '''Returns the pandas object of the revels_detail view.'''
        return pandas.read_sql_table('revels_detail', self.dbconn,
                                     schema=db_schema)

    def log_summary(self):
        revels_data_frame = self.get_revels().drop(columns=['bag_id', 'type_id', 'shop_id', 'data_id']).groupby('type_name')
        for name, group in revels_data_frame:
            logging.info("{}\n{}".format(name, group.describe()))

    def log_results(self, num):
        results = self.dbconn.execute("SELECT model_name,accuracy_score FROM revels.models "
                                             "ORDER BY accuracy_score DESC LIMIT {}".format(num))
        model_count = self.dbconn.execute("SELECT count(*) FROM revels.models").next()['count']
        for row in results:
            logging.info("{}: {}%".format(row['model_name'], round(row['accuracy_score'] * 100, 2)))
        logging.info("{} trained models total".format(model_count))

    def write_model_to_db(self, model_name, model, score, metadata):

        model_bytes = io.BytesIO()
        meta_bytes = io.BytesIO()
        pickle.dump(model, model_bytes)
        pickle.dump(metadata, meta_bytes)
        model_bytes.seek(0)
        meta_bytes.seek(0)

        self.dbconn.execute("INSERT INTO revels.models (model_name, trained_model, accuracy_score, metadata) VALUES "
                            "(%s, %s, %s, %s)", model_name, model_bytes.read(), score, meta_bytes.read())
        self.dbconn.execute("COMMIT")

    def get_best_model(self):
        result = self.dbconn.execute("SELECT (model, accuracy_score, metadata) "
                                     "FROM revels.models ORDER BY accuracy_score DESC LIMIT 1")
        row = result.next()
        score = row['accuracy_score']
        model = pickle.loads(row['trained_model'])
        meta = pickle.loads(row['metadata'])
        return model, score, meta