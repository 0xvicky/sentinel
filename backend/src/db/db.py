import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv


@contextmanager
def get_db_conn():
    """Context manager to automatically open and close database connections."""
    connection = None
    try:
        connection = psycopg2.connect(
            dbname="admin",
            user="admin",
            password="admin123",
            host="localhost",
            port="5432",
        )

        yield connection
        connection.commit()

    except Exception as e:
        print(f"Database error: {e}")
        if connection:
            connection.rollback()
        raise e
    finally:
        if connection:
            connection.close()


@contextmanager
def db_init():
    try:
        with get_db_conn() as conn:
            with conn.cursor() as cursor:
                # create table if doesn't exist
                create_doc_table_qry = """
                CREATE TABLE IF NOT EXISTS documents (
                    doc_id VARCHAR PRIMARY KEY,
                    storage_path VARCHAR,
                    doc_size INT,
                    doc_name VARCHAR,
                    session_id VARCHAR
                )
                """

                cursor.execute(create_doc_table_qry)
                print("doc table created success")

    except Exception as e:
        print(f"Error: {e}")
