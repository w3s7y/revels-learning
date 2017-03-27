-- postgresql (9.6) psql file for creation of revels schema.
-- Run as the postgres admin user.
create role scienceuser with login password '*********'; -- create some password
create database sciencedb with owner scienceuser;
