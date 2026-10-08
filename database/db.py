import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("A variável DATABASE_URL não foi configurada no ambiente.")

engine = create_engine(DATABASE_URL, echo=False)
logging.basicConfig(filename="erros.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")


def consult_db(script, params=None):
    try:
        with engine.connect() as conn:
            if params is not None:
                result = conn.execute(script, params)
            else:
                result = conn.execute(script)
            return result.fetchall()
    except Exception as exc:
        logging.error("Erro ao consultar o banco de dados: %s", exc)
        return None


def exe_db(script, params=None):
    try:
        with engine.begin() as conn:
            conn.execute(script, params or {})
    except Exception as exc:
        logging.error("Erro ao executar o script no banco de dados: %s | params: %s", exc, params)
        return None
