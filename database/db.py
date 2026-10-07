from sqlalchemy import create_engine
from dotenv import load_dotenv

import os 
import logging

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

logging.basicConfig(filename='erros.log', level=logging.ERROR)

def consult_db(script, params=None):

    print("SCRIPT SQL:", script.text)
    print("PARAMS:", params)

    if params:
        print("PARAM TYPE:", type(params.get("embedding")))
        print("PARAM SAMPLE:", str(params.get("embedding"))[:50])

    try:
        with engine.connect() as conn:
            if params is not None:
                result = conn.execute(script, params)
            else:
                result = conn.execute(script)

            rows = result.fetchall()
            print("RESULT TYPE:", type(rows))
            print(rows)

            print("ROWS LEN:", len(rows))
            print("ROWS SAMPLE:", rows[:2])

            return rows

    except Exception as e:
        logging.error(f'Erro ao consultar o banco de dados: {e}')
        return None


def exe_db(script, params=None):
    try:
        with engine.begin() as conn:

            conn.execute(script, params or {})
            
    except Exception as e:

        logging.error(f'Erro ao executar o script no banco de dados: {e}, params: {params}')
        return None
