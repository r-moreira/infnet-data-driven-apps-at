from fastapi import FastAPI 
from service import statsbomb_service
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.get("/")
def test():
    return statsbomb_service.get_competitions()