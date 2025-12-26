from fastapi import FastAPI, HTTPException
import sys
from pathlib import Path

sys.path.insert(0, './src')

from processor import (
    MySQLRequest,
    PostgreSQLRequest,
    MongoDBRequest,
    CassandraRequest,
    QueryResponse,
    process_mysql_query,
    process_postgresql_query,
    process_mongodb_query,
    process_cassandra_query
)

app = FastAPI(
    title="Universal Query Translator",
    description="Translate natural language queries to database-specific queries using LLM",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Universal Query Translator API",
        "version": "1.0.0",
        "endpoints": {
            "mysql": "/api/mysql",
            "postgresql": "/api/psql",
            "mongodb": "/api/mongo",
            "cassandra": "/api/cassandra"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/mysql", response_model=QueryResponse)
async def mysql_endpoint(request: MySQLRequest):
    """
    Translate natural language query to MySQL query.
    
    Args:
        request: MySQLRequest containing database credentials and query
        
    Returns:
        QueryResponse: Translated MySQL query
    """
    try:
        result = process_mysql_query(request)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/psql", response_model=QueryResponse)
async def postgresql_endpoint(request: PostgreSQLRequest):
    """
    Translate natural language query to PostgreSQL query.
    
    Args:
        request: PostgreSQLRequest containing database credentials and query
        
    Returns:
        QueryResponse: Translated PostgreSQL query
    """
    try:
        result = process_postgresql_query(request)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/mongo", response_model=QueryResponse)
async def mongodb_endpoint(request: MongoDBRequest):
    """
    Translate natural language query to MongoDB query.
    
    Args:
        request: MongoDBRequest containing database credentials and query
        
    Returns:
        QueryResponse: Translated MongoDB query
    """
    try:
        result = process_mongodb_query(request)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/cassandra", response_model=QueryResponse)
async def cassandra_endpoint(request: CassandraRequest):
    """
    Translate natural language query to Cassandra CQL query.
    
    Args:
        request: CassandraRequest containing database credentials and query
        
    Returns:
        QueryResponse: Translated Cassandra CQL query
    """
    try:
        result = process_cassandra_query(request)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    # Run from src directory - use "main:app" when running python main.py from src/
    # Or run from parent directory with: uvicorn src.main:app --reload
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
