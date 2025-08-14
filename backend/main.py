from fastapi import FastAPI
from pydantic import BaseModel
from sql_generator import handle_sql_query
from rag_pipeline import handle_rag_query

app = FastAPI() 

class QueryRequest(BaseModel):
    query: str
    type: str # 'sql' or 'rag'

@app.post("/ask")
async def ask_data(request: QueryRequest):
    if request.type == 'sql':
        return handle_sql_query(request.query)
    elif request.type == 'rag':
        return handle_rag_query(request.query)
    else:
        return {"error": "Invalid query type. Use 'sql' or 'rag'."} 
    
@app.post("/ask-sql")
async def ask_sql(req: QueryRequest):
    sql = handle_sql_query(req.query)
    return {"sql": sql}