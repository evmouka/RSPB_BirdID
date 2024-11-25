import sqlite3
import psycopg2
import random
from src.algo import BirdIdentifier
# from statistic import ProbabilisticBirdIdentifier
import os

def create_querry(dbName: str, dic: dict) -> str:
    query = f"SELECT * FROM {dbName} WHERE 1=1"
    params = []
    for key, value in dic.items():
        if not value or key == "new_attribute":
            continue
        conditions = []
        key = f"`{key}`"
        for item in value:
            conditions.append(f"{key} LIKE ?")
            params.append(f"%{item}%")      
        if conditions:
            query += f" AND ({' AND '.join(conditions)} OR {key} IS NULL)"
    return query, params 

def fetch_db(querry: str, params: list, isGame: bool=False) -> list:
    db = sqlite3.connect(os.getenv('POSTGRES_DB'))
    cursor = db.cursor()
    if isGame:
        cursor.execute("select * from birdInfo")
    else:
        cursor.execute(querry, params)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    
    result = [dict(zip(column_names, row)) for row in rows]
    
    db.close()
    if isGame:
        return random.choice(result)
    return result

def find_error(bird: dict, dic: dict) -> list:
    exclusions = []
    
    for key, value in dic.items():
        if bird.get(key) != value:
            exclusions.append({
                "category": key,
                "adjective": value,
                "bird_value": bird.get(key),
            })
    
    return exclusions

def find_bird(dic: dict, birds_left:int, features: list,  id: int, match_count: int) -> tuple:
    query, params = create_querry("birdInfo", dic)
    birds = fetch_db(query, params)
    all_birds = fetch_db("select * from birdInfo", [])
    error = None
    #if game
    if not id == -1:
        id_exists = any(d.get("id") == id for d in birds)
        if not id_exists:
            bird = fetch_db("select * from birdInfo where species_number=?", [id])
            error = find_error(bird, dic)

    birdId = BirdIdentifier(birds, all_birds, dic, features, match_count)
    question = birdId.find_best_question()
    if len(birds) < 2 or not question:
        matches = birdId.get_best_matches()
        return None, error, matches
    return question, error, None