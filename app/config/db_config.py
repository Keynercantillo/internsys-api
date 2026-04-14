import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="ep-weathered-credit-amp6j2mh-pooler.c-5.us-east-1.aws.neon.tech",
        port="5432",
        user="neondb_owner",
        password="npg_dY7fiSqmQU9n",
        dbname="neondb",
        sslmode="require"
    )