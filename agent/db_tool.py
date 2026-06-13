from sqlalchemy import create_engine, text
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ecommerce.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)


def query_db(sql: str) -> list:
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            return [dict(row._mapping) for row in result]
    except Exception as e:
        return [{"error": str(e)}]