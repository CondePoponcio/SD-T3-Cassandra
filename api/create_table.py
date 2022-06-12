#!/usr/local/bin/python3
import os

from cassandra.cluster import Cluster

KEYSPACE = os.environ["CASSANDRA_KEYSPACE"]
cluster = Cluster([os.environ["CASSANDRA_IP_ADDRESS"]], port=9042)
session = cluster.connect()
print("creating keyspace...")
#NetworkTopologyStrategy
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS %s
    WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
    """ % 'paciente_ks')

session.execute("""
    CREATE KEYSPACE IF NOT EXISTS %s
    WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '3' }
    """ % 'recetas_ks')

cluster = Cluster([os.environ["CASSANDRA_IP_ADDRESS"]], port=9042)
session = cluster.connect('paciente_ks', wait_for_all_pools=True)
print("creating table...")
session.execute("""
    CREATE TABLE IF NOT EXISTS paciente (
        id UUID,
        nombre text,
        apellido text,
        rut text,
        email text,
        fecha_nacimiento text,
        PRIMARY KEY ((nombre), id)
    )
""")

cluster = Cluster([os.environ["CASSANDRA_IP_ADDRESS"]], port=9042)
session = cluster.connect('recetas_ks', wait_for_all_pools=True)
print("creating table...")

session.execute("""
    CREATE TABLE IF NOT EXISTS recetas (
        id UUID,
        id_paciente UUID,
        comentario text,
        farmacos text,
        doctor text,
        PRIMARY KEY ((id))
    )
""")