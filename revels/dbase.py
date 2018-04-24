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

db_host = os.environ.get('REVELS_DB_HOST', 'revelsdb')
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

    logging.debug("Dropping database {}".format(db_name))
    con.execute("commit")
    con.execute("DROP SCHEMA IF EXISTS {} CASCADE".format(db_schema))
    con.execute("commit")
    con.execute("DROP DATABASE IF EXISTS {}".format(db_name))
    con.execute("commit")
    con.execute("DROP ROLE IF EXISTS {}".format(db_user))
    con.execute("commit")
    logging.debug("Database {} successfully dropped.".format(db_name))

    # Create the application user
    con.execute(sqlalchemy.text("CREATE ROLE {} WITH LOGIN PASSWORD '{}'".format(db_user, db_pass)))
    logging.info("User {} created.".format(db_user))
    con.execute("commit")

    # Create the database
    con.execute(sqlalchemy.text("CREATE DATABASE {} WITH OWNER = {} TEMPLATE = template0 "
                                "ENCODING = 'UTF8' ".format(db_name, db_user)))
    con.execute("commit")
    logging.debug("Database {} created.".format(db_name))

    # Disconnect from postgres and reconnect to revels database to create schema
    con.close()
    logging.debug("Connection to database postgres closed, reconnect to {}.".format(db_name))
    engine = sqlalchemy.create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(db_adm_usr, db_adm_pass, db_host,
                                                                                    db_port, db_name))
    con = engine.connect()
    logging.debug("Connection to {} as {} established, creating schema...".format(db_name, db_adm_usr))

    # Create the schema.
    logging.info("Creating tables, ACLs and performing initial data load.")
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
        self.dbconn.execute("COMMIT")

    def get_connection(self):
        """
        :return: sqlalchemy.connection
        """
        return self.dbconn

    def write_shop(self, shop_name, address1, address2, address3, postcode):
        """

        :param shop_name:
        :param address1:
        :param address2:
        :param address3:
        :param postcode:
        :return: None
        """
        self.dbconn.execute('insert into shops (shop_name,' +
                            'address_1, address_2, address_3, postcode) ' +
                            'values (%s, %s, %s, %s, %s)',
                            shop_name,
                            address1,
                            address2,
                            address3,
                            postcode)
        self.dbconn.execute("COMMIT")

    def write_bag(self, shop_id, mass, price):
        """

        :param shop_id:
        :param mass:
        :param price:
        :return: None
        """
        self.dbconn.execute("insert into bags " +
                            "(shop_bought, total_mass, price) " +
                            "values (%s, %s, %s)",
                            shop_id,
                            mass,
                            price)
        self.dbconn.execute("COMMIT")

    def write_sample(self,
                     bag_id, type_id, mass, density, height, width, depth):
        """

        :param bag_id:
        :param type_id:
        :param mass:
        :param density:
        :param height:
        :param width:
        :param depth:
        :return:
        """
        self.dbconn.execute("insert into data " +
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
        self.dbconn.execute("COMMIT")

    def get_shops(self):
        """

        :return:
        """
        return pandas.read_sql_table('shops', self.dbconn,
                                     schema=db_schema)

    def get_bags(self):
        """

        :return:
        """
        return pandas.read_sql_table('bags', self.dbconn,
                                     schema=db_schema)

    def get_types(self):
        """

        :return:
        """
        return pandas.read_sql_table('types', self.dbconn,
                                     schema=db_schema)

    def get_samples(self):
        """

        :return:
        """
        return pandas.read_sql_table('data', self.dbconn,
                                     schema=db_schema)

    def get_revels(self):
        """

        :return:
        """
        return pandas.read_sql_table('revels_detail', self.dbconn,
                                     schema=db_schema)

    def log_summary(self):
        """

        :return:
        """
        revels_data_frame = self.get_revels().drop(columns=['bag_id', 'type_id', 'shop_id', 'data_id']).groupby('type_name')
        for name, group in revels_data_frame:
            logging.info("{}\n{}".format(name, group.describe()))
        return self.dbconn

    def log_results(self, num):
        """

        :param num:
        :return:
        """
        results = self.dbconn.execute("SELECT model_name,accuracy_score FROM models "
                                             "ORDER BY accuracy_score DESC LIMIT {}".format(num))
        model_count = self.dbconn.execute("SELECT count(*) FROM revels.models").next()['count']
        for row in results:
            logging.info("{}: {}%".format(row['model_name'], round(row['accuracy_score'] * 100, 2)))
        logging.info("{} trained models total".format(model_count))
        return self.dbconn

    def write_model_to_db(self, model_name, model, score, metadata):
        """
        Write a model and its associated metadata to the models table
        :param model_name: To store in the model_name column
        :param model: the trained machine learning model
        :param score: floating point number, generally the sklearn.metrics.accuracy_score() value
        :param metadata: Metadata (as dict). {"validataion_split": validation_split,
                                              "validation_seed": validation_seed,
                                              "confusion_matrix": sklearn.metrics.confusion_matrix(),
                                              "classification_rep": sklearn.metrics.classification_report()}
        :return: None
        """
        model_bytes = io.BytesIO()
        meta_bytes = io.BytesIO()
        pickle.dump(model, model_bytes)
        pickle.dump(metadata, meta_bytes)
        model_bytes.flush()
        meta_bytes.flush()
        model_bytes.seek(0)
        meta_bytes.seek(0)

        self.dbconn.execute("INSERT INTO models (model_name, trained_model, accuracy_score, metadata) VALUES "
                            "(%s, %s, %s, %s)", model_name, model_bytes.read(), score, meta_bytes.read())
        self.dbconn.execute("COMMIT")

    def get_best_model(self):
        """
        Get the most accurate model and it's metadata from the database.
        :return: Tuple(model, metadata, accuracy_score, model_name, id)
        """
        result = self.dbconn.execute("SELECT trained_model, metadata, accuracy_score, model_name, id "
                                     "FROM models ORDER BY accuracy_score DESC LIMIT 1").fetchone()

        model_b = io.BytesIO()
        meta_b = io.BytesIO()
        model_b.write(result[0])
        meta_b.write(result[1])
        model_b.flush()
        meta_b.flush()
        model_b.seek(0)
        meta_b.seek(0)
        model = pickle.loads(model_b.read())
        meta = pickle.loads(meta_b.read())

        return model, meta, result[2], result[3], result[4]

    def get_model_by_id(self, model_id):
        """
        Get a model by its database index number.
        :param model_id: the id of the model in the database
        :return:Tuple(model, metadata, accuracy_score, model_name)
        """
        result = self.dbconn.execute("SELECT trained_model, metadata, accuracy_score, model_name "
                                     "FROM models WHERE id = {}".format(model_id)).fetchone()
        model_b = io.BytesIO()
        model_b.write(result[0])
        model_b.flush()
        model_b.seek(0)

        meta_b = io.BytesIO()
        meta_b.write(result[1])
        meta_b.flush()
        meta_b.seek(0)
        return pickle.loads(model_b.read()), pickle.loads(meta_b.read()), result[2], result[3]

    def get_top_models(self, number):
        """
        Get a list of the top number of trained models
        :param number: Number of models to get
        :return: List of Tuple(model, metadata, accuracy_score, model_name, id)
        """
        result = self.dbconn.execute("SELECT trained_model, metadata, accuracy_score, model_name, id "
                                     "FROM models ORDER BY accuracy_score DESC LIMIT {}".format(number))
        results = []
        for row in result:
            model_b = io.BytesIO()
            meta_b = io.BytesIO()
            model_b.write(row[0])
            meta_b.write(row[1])
            model_b.flush()
            meta_b.flush()
            model_b.seek(0)
            meta_b.seek(0)
            model = pickle.loads(model_b.read())
            meta = pickle.loads(meta_b.read())
            results.append((model, meta, row[2], row[3], row[4]))
        return results
