#!/bin/bash

export PGPASSWORD='password'

#psql -d test -U test -h localhost -c 'CREATE TABLE IF NOT EXISTS ITEMS (name varchar(255) PRIMARY KEY,count int);'
psql -d test -U test -h localhost -c 'DROP TABLE ITEMS;'
#docker exec -it postgresql psql -U test -c 'select * from pg_create_physical_replication_slot('node1');'
