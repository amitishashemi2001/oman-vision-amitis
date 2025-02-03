import sys, os, shutil
from django.conf import settings
import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME', 'postgres'),
    user=os.getenv('DB_USER', 'postgres'),
    password=os.getenv('DB_PASSWORD', 'postgres'),
    host=os.getenv('DB_HOST', '127.0.0.1'),
    port=os.getenv('DB_PORT', '5432')
)

def move_file(file_field, new_path):
    try:
        if file_field and os.path.isfile(file_field.path):
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            shutil.move(file_field.path, new_path)
            file_field.name = new_path.replace(settings.MEDIA_ROOT + '/', '')
    except Exception as e:
        print(f'error in move_file helper : {e}', file=sys.stderr)

def check_soft_deleted_user_exists(email, company_email, username):
    try:
        cur = conn.cursor()
        query = sql.SQL("""
            SELECT EXISTS (
                SELECT 1
                FROM "accounts_user"
                WHERE (email = %s OR company_email = %s OR username = %s)
                AND is_deleted = TRUE
            );
        """)
        params = (email, company_email, username)
        cur.execute(query, params)
        exists = cur.fetchone()[0]
        cur.close()
        return exists
    except Exception as e:
        print(f'error in check_soft_deleted_user_exists helper : {e}', file=sys.stderr)
