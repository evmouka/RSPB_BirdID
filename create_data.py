import pandas as pd
import sqlite3
import psycopg2
from psycopg2 import sql

db = sqlite3.connect('bird_database.db')
cursor = db.cursor()

create_table_sql = """
CREATE TABLE birdInfo (
    species_number INTEGER PRIMARY KEY,
    name TEXT,
    latin_name TEXT,
    alt_names_mispellings TEXT,
    sex_age_variations TEXT,
    seasonal_variations TEXT,
    conservation_status TEXT,
    bird_group TEXT,
    time_of_year_active TEXT,
    summary TEXT,
    picture TEXT,
    picture_2 TEXT,
    picture_3 TEXT,
    picture_4 TEXT,
    illustration TEXT,
    audio TEXT,
    distribution_map TEXT,
    plumage_colour TEXT,
    beak_colour TEXT,
    feet_colour TEXT,
    leg_colour TEXT,
    beak_shape_1 TEXT,
    beak_shape_2 TEXT,
    tail_shape_1 TEXT,
    tail_shape_2 TEXT,
    pattern_markings TEXT,
    diet TEXT,
    population TEXT,
    min_length INTEGER,
    max_length INTEGER,
    mean_length REAL,
    size TEXT,
    wingspan TEXT,
    weight TEXT,
    habitat TEXT,
    appearance TEXT,
    call TEXT,
    behaviour TEXT,
    fact_1 TEXT,
    fact_2 TEXT,
    fact_3 TEXT,
    similar_species TEXT,
    where_to_see_them TEXT
);
"""

    # "Pattern/ Markings" TEXT,

# cursor.execute(create_table_sql)
birdlist = pd.read_json("./bird_data.json")
birdlist.to_sql('BirdInfo', db, index=False)