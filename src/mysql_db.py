import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

def mysql_engine(username='',password=''):
    if username == '' and password == '':
        conn_string = f'mysql+mysqlconnector://localhost/'
    else:
        conn_string = f'mysql+mysqlconnector://{username}:{password}@localhost/'
    
    engine = create_engine(conn_string)

    with engine.connect() as conn:
        try:
            query = text("SELECT @@VERSION")
            result = conn.execute(query)
            print([row for row in result])
        except Exception as e:
            print(f"Connection could not be established: {e}")
            exit()

    conn = engine.connect()
    return conn

def mysql_schema(conn):
    db_list = conn.execute(text("SHOW DATABASES"))
    information_schema = conn.execute(text("SELECT * FROM INFORMATION_SCHEMA.TABLES"))

    user_db_list = []
    for db in db_list:
        if db[0] in ['mysql','sys','information_schema','performance_schema']:
            continue
        user_db_list.append(db[0])

    user_db_info ={}
    for db in user_db_list:
        user_db_info[db] = []  

    tables_info =[]
    for row in information_schema:
        db_name = row[1]
        if db_name not in user_db_list:
            continue
        tables_info.append(row)

    table_db_dict = {}
    for table in tables_info:
        table_db_dict[table[2]] = table[1]
        user_db_info[table[1]].append(table)

    def get_table_names(user_tables):
        table_names = []
        for table in user_tables:
            table_names.append(table[2]) 
        return table_names

    def get_random_rows(table, n=5):
        db = table_db_dict[table]
        conn.execute(text(f'use {db}'))
        query = f'SELECT * FROM {table} ORDER BY RAND() LIMIT {n}'
        return pd.read_sql(text(query), conn)
        
    def desc_table(table):
        db = table_db_dict[table]
        conn.execute(text(f'use {db}'))
        query = f'DESC {table}'
        return pd.read_sql(text(query), conn)
    
    markdown = []
    for table in get_table_names(tables_info):
        markdown.append(f'### {table}')
        random_rows = get_random_rows(table).to_markdown()
        table_description = desc_table(table).to_markdown()
        table_schema = table_description + '\n' + random_rows
        markdown.append(table_schema)
        markdown.append('\n')

    # Join the markdown list into a single string
    table_definitions = '\n'.join(markdown)
    table_definitions = table_definitions + '\n---\nReturn the TSQL Query for:'

    return table_definitions

