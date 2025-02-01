import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

def pgsql_engine(username='',password=''):
    if username == '' and password == '':
        conn_string = f'postgresql+psycopg2://localhost/'
    else:
        conn_string = f'postgresql+psycopg2://{username}:{password}@localhost/'
    
    engine = create_engine(conn_string)

    with engine.connect() as conn:
        try:
            query = text("select setting from pg_settings where name like '%version%'")
            result = conn.execute(query)
            print([row for row in result][0][0])
            print()
        except Exception as e:
            print(f"Connection could not be established: {e}")
            exit()

    conn = engine.connect()
    return conn

# username, password = 'postgres','postgres123'
# conn = pgsql_engine(username,password)

def pgsql_schema(conn):
    db_list = conn.execute(text("SELECT datname FROM pg_database"))

    user_db_list = []
    for db in db_list:
        if 'template' in db[0]:
            continue
        user_db_list.append(db[0])

    # print(user_db_list)

    table_db_dict = {}
    master_table_list = []
    for db in user_db_list:
        tables = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        for table in tables:
            table_db_dict[table[0]] = db
            master_table_list.append(table[0])
            
    # print(table_db_dict)
    # print(master_table_list)

    def get_random_rows(table, n=5):
        db = table_db_dict[table]
        engine = create_engine(f'postgresql+psycopg2://postgres:postgres123@localhost/{db}')
        
        with engine.connect() as cnxn:
            query = f'SELECT * FROM {table} ORDER BY RANDOM() LIMIT {n}'
            return pd.read_sql(text(query), cnxn)

    def desc_table(table):
        db = table_db_dict[table]
        engine = create_engine(f'postgresql+psycopg2://postgres:postgres123@localhost/{db}')

        with engine.connect() as cnxn:
            query = f"select column_name, data_type, udt_name, is_nullable from information_schema.columns where table_name = '{table}'"
            return pd.read_sql(text(query), cnxn)

    markdown = []

    for table in master_table_list:
        markdown.append(f'### {table}')
        random_rows = get_random_rows(table).to_markdown()
        table_description = desc_table(table).to_markdown()
        table_schema = table_description + '\n' + random_rows
        markdown.append(table_schema)
        markdown.append('\n')

    # Join the markdown list into a single string
    table_definitions = '\n'.join(markdown)
    table_definitions = table_definitions + '\n---\nReturn the TSQL Query for:'

    # print(table_definitions)
    return table_definitions

