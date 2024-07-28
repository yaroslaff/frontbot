#!/usr/bin/env python

from fastapi import FastAPI
from pydantic import BaseModel 
from typing import List
from dotenv import load_dotenv
import argparse
import os

app = FastAPI()

class Button(BaseModel):
    name: str

class FrontBotResponse(BaseModel):
    text: str
    forms: list[Button] | None = None

@app.get("/frontbot", response_model=FrontBotResponse)
def frontbot():
    # Создаем экземпляр собственного класса
    data = FrontBotResponse(text='Hello **World**!')
    return data

def get_args():
    parser = argparse.ArgumentParser(description='FrontBot-protected demo application')

    def_host = os.getenv('FRONTBOT_APP_HOST', 'localhost')
    def_port = int(os.getenv('FRONTBOT_APP_POST', '8899'))

    parser.add_argument('--host', type=str, default=def_host)
    parser.add_argument('--port', '-p', type=int, default=def_port)
    return parser.parse_args()

def main():
    import uvicorn
    load_dotenv()
    args = get_args()
    uvicorn.run(app, host=args.host, port=args.port)

# Запуск приложения
if __name__ == "__main__":
    main()