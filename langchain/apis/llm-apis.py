import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialise model
model = ChatGroq(
    model="Gemma2-9b-It",
    groq_api_key=groq_api_key
)

# Prompt Templates
system_template = "Translate following into {language}:"
prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "{text}")
])

# Parser
parser = StrOutputParser()

# Create Chain
chain = prompt|model|parser

# Add Definitions
app = FastAPI(
    title="Lanchain Server",
    version="1.0",
    description="API Server"
)

add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="localhost", 
        port=8000
    )








