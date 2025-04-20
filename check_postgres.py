import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError


def get_env() -> dict[str]:
    """Get ENVs from .env file."""
    load_dotenv()

    postgres_user = os.getenv("POSTGRES_USER")
    postgres_pwd = os.getenv("POSTGRES_PASSWORD")
    envs = {
        "user": postgres_user,
        "pwd": postgres_pwd,
    }
    return envs


def check_connection(host: str, user: str, password) -> bool:
    """Check connection to Postgres in remote host."""
    cursor, connection = None, None
    success = False
    try:
        connection = psycopg2.connect(
            host=host, user=user, password=password, dbname="postgres"
        )
        print("Connection successful!")

        cursor = connection.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        print(f"Result of query 'SELECT 1': {result[0]}")

        success = True
        return success

    except OperationalError as e:
        print(f"Connection error: {e}")
        return success

    except Exception as e:
        print(f"Error: {e}")
        return success

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def main():
    """Main function for step-by-step complete all tasks."""
    if len(sys.argv) != 2:
        print("Incorrect usage!")
        print("Usage: python deploy_postgres.py server_ip")
        sys.exit(1)
    server = sys.argv[1]

    envs = get_env()
    status = check_connection(host=server, user=envs["user"], password=envs["pwd"])
    if status:
        print("[INFO] ===== Successful test connection to Postgres =====")
    else:
        print("[ERRROR] ===== Error when test connection to Postgres! =====")


if __name__ == "__main__":
    main()
