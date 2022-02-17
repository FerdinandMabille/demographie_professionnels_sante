import os
import sqlite3
import pandas as pd

from .query_private_transform import *


def transform_export(filepath_activites, filepath_personnes, database="database", verbose = True) :
    """
    Création des fichiers activités.csv et personnes.csv à partir des fichiers .csv 
    présents dans data/input.
    """
    conn = sqlite3.connect(
        database=database
    )
    print(" - - - Suppression des fichiers output si existants...")
    if os.path.exists(filepath_activites):
        os.remove(filepath_activites)
    if os.path.exists(filepath_personnes):
        os.remove(filepath_personnes)

    # Transformation et export des données activités
    print(" ")
    print(" - - - Transformation et export des données activités...")
    select_activites_sql = query_select_activites_sql()

    for chunk in pd.read_sql_query(select_activites_sql, conn, chunksize=10000):
       chunk.to_csv(os.path.join(filepath_activites), index = True, index_label = "INDEX", mode='a',sep=';',encoding='utf-8')
    
    print(" --- select_activites_sql : OK")
    
    # transformation et export des données personnes
    print(" ")
    print(" - - - Transformation et export des données personnes...")
    
    select_personnes_sql = query_select_personnes_sql()

    for chunk in pd.read_sql_query(select_personnes_sql, conn, chunksize=10000):
       chunk.to_csv(os.path.join(filepath_personnes), index = True, index_label = "INDEX", mode='a',sep=';',encoding='utf-8')

    print(" --- select_personnes_sql : OK")
