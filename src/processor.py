from pydantic import BaseModel, Field
from prompt_template import mysql_template, pgsql_template, mongodb_template, cassandra_template
from llm_model import llm_model
from mysql_db import mysql_engine, mysql_schema
from postgres_db import pgsql_engine, pgsql_schema
from mongo_db import mongo_engine, mongo_schema
from dotenv import load_dotenv

load_dotenv()


# Pydantic Request Models
class DatabaseCredentials(BaseModel):
    """Base model for database credentials"""
    username: str = Field(..., description="Database username")
    password: str = Field(..., description="Database password")


class QueryRequest(BaseModel):
    """Base model for query requests"""
    query: str = Field(..., description="Natural language query to translate")


class MySQLRequest(BaseModel):
    """Request model for MySQL query translation"""
    username: str = Field(..., description="MySQL username")
    password: str = Field(..., description="MySQL password")
    query: str = Field(..., description="Natural language query to translate")


class PostgreSQLRequest(BaseModel):
    """Request model for PostgreSQL query translation"""
    username: str = Field(..., description="PostgreSQL username")
    password: str = Field(..., description="PostgreSQL password")
    query: str = Field(..., description="Natural language query to translate")


class MongoDBRequest(BaseModel):
    """Request model for MongoDB query translation"""
    username: str = Field(..., description="MongoDB username")
    password: str = Field(..., description="MongoDB password")
    query: str = Field(..., description="Natural language query to translate")


class CassandraRequest(BaseModel):
    """Request model for Cassandra query translation"""
    username: str = Field(..., description="Cassandra username")
    password: str = Field(..., description="Cassandra password")
    query: str = Field(..., description="Natural language query to translate")


# Response Models
class QueryResponse(BaseModel):
    """Response model for query translation"""
    message: dict = Field(..., description="Translated query result")


# Processor Methods
def process_mysql_query(request: MySQLRequest) -> dict:
    """
    Process MySQL query translation request.
    
    Args:
        request: MySQLRequest containing credentials and query
        
    Returns:
        dict: Response containing translated query
    """
    try:
        conn = mysql_engine(username=request.username, password=request.password)
        db_schema = mysql_schema(conn)
        output = llm_model(mysql_template, db_schema, request.query)
        return {"message": output}
    except Exception as e:
        raise Exception(f"Error processing MySQL query: {str(e)}")


def process_postgresql_query(request: PostgreSQLRequest) -> dict:
    """
    Process PostgreSQL query translation request.
    
    Args:
        request: PostgreSQLRequest containing credentials and query
        
    Returns:
        dict: Response containing translated query
    """
    try:
        conn = pgsql_engine(username=request.username, passwd=request.password)
        db_schema = pgsql_schema(conn)
        output = llm_model(pgsql_template, db_schema, request.query)
        return {"message": output}
    except Exception as e:
        raise Exception(f"Error processing PostgreSQL query: {str(e)}")


def process_mongodb_query(request: MongoDBRequest) -> dict:
    """
    Process MongoDB query translation request.
    
    Args:
        request: MongoDBRequest containing credentials and query
        
    Returns:
        dict: Response containing translated query
    """
    try:
        conn = mongo_engine(username=request.username, passwd=request.password)
        db_schema = mongo_schema(conn)
        output = llm_model(mongodb_template, db_schema, request.query)
        return {"message": output}
    except Exception as e:
        raise Exception(f"Error processing MongoDB query: {str(e)}")


def process_cassandra_query(request: CassandraRequest) -> dict:
    """
    Process Cassandra query translation request.
    
    Args:
        request: CassandraRequest containing credentials and query
        
    Returns:
        dict: Response containing translated query
    """
    try:
        # Note: Cassandra implementation may need to be added
        # For now, using placeholder
        output = llm_model(cassandra_template, "", request.query)
        return {"message": output}
    except Exception as e:
        raise Exception(f"Error processing Cassandra query: {str(e)}")

