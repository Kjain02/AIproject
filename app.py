from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # type: ignore

from src.routers import analyse_company, extraction_rel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(analyse_company.router, tags=["analyse_company"], prefix="/api")
app.include_router(extraction_rel.router, tags=["extraction_related"], prefix="/api")

@app.get("/")
def read_root():
    print("Hello World")
    return {"Hello": "World from FastAPI"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=3006, log_level="debug", reload=True)
