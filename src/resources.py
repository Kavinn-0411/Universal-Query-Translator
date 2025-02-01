from flask import jsonify
from flask_restful import Resource,Api, marshal,reqparse,fields,marshal_with,inputs
from prompt_template import mysql_template,pgsql_template,mongodb_template,cassandra_template
from llm_model import llm_model
from mysql_db import mysql_engine,mysql_schema
from postgres_db import pgsql_engine,pgsql_schema
from mongo_db import mongo_engine,mongo_schema
from dotenv import load_dotenv

load_dotenv()
api=Api(prefix='/api')

mysql_parser=reqparse.RequestParser()
psql_parser=reqparse.RequestParser()
mongo_parser=reqparse.RequestParser()
cassandra_parser=reqparse.RequestParser()
query=reqparse.RequestParser()

mysql_parser.add_argument('username',type=str,required=True)
mysql_parser.add_argument('password',type=str,required=True)

psql_parser.add_argument('username',type=str,required=True)
psql_parser.add_argument('password',type=str,required=True)

mongo_parser.add_argument('username',type=str,required=True)
mongo_parser.add_argument('password',type=str,required=True)

cassandra_parser.add_argument('username',type=str,required=True)
cassandra_parser.add_argument('password',type=str,required=True)

query.add_argument('query',type=str,required=True)

class Mysql(Resource):
    def post(self):
        args=mysql_parser.parse_args()
        args1=query.parse_args()
        conn=mysql_engine(username=args.get("username"),passwd=args.get("password"))
        input=mysql_schema(conn)
        output=llm_model(mysql_template,input,args1.get("query"))
        return {"message":output},200
api.add_resource(Mysql,'/mysql')

class Psql(Resource):
    def post(self):
        args=psql_parser.parse_args()
        args1=query.parse_args()
        conn=pgsql_engine(username=args.get("username"),passwd=args.get("password"))
        input=pgsql_schema(conn)
        output=llm_model(mysql_template,input,args1.get("query"))
        return {"message":output},200
api.add_resource(Psql,'/psql')

class Mongo(Resource):
    def post(self):
        args=mongo_parser.parse_args()
        args1=query.parse_args()
        conn=mongo_engine(username=args.get("username"),passwd=args.get("password"))
        input=mongo_schema(conn)
        output=llm_model(mysql_template,input,args1.get("query"))
        return {"message":output},200
api.add_resource(Mongo,'/mongo')






