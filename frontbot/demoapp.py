#!/usr/bin/env python

from fastapi import FastAPI, Request
from pydantic import BaseModel 
from typing import List
from dotenv import load_dotenv
import argparse
import os
import json

app = FastAPI()
args = None

class Button(BaseModel):
    name: str

class FrontBotResponse(BaseModel):
    text: str | None = None
    error: str | None = None
    forms: list[Button] | None = None


def record_visit(userid: str) -> int:
    try:
        with open(args.database, 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}
    
    if userid in users:
        users[userid] += 1
    else:
        users[userid] = 1
    
    with open(args.database, 'w') as f:
        json.dump(users, f)
    
    return users[userid]


@app.get("/frontbot", response_model=FrontBotResponse)
def frontbot(request: Request):
    token = request.headers.get('authorization').split(' ')[1]
    username = request.headers.get('x-username')
    userid = request.headers.get('x-userid')

    if token != args.token:
        return FrontBotResponse(error=f'Bad token')

    vnum = record_visit(userid)

    data = FrontBotResponse(text=f'Hello **{username}**!\n\nYour userID is {userid}\n\nThis is your visit #{vnum}')
    return data

def get_args():
    parser = argparse.ArgumentParser(description='FrontBot-protected demo application')

    def_host = os.getenv('FRONTBOT_APP_HOST', 'localhost')
    def_port = int(os.getenv('FRONTBOT_APP_POST', '8899'))
    def_token = os.getenv('APP_TOKEN')
    def_db = os.getenv('APP_DB', "users.json")

    parser.add_argument('--host', type=str, default=def_host)
    parser.add_argument('--port', '-p', type=int, default=def_port)
    parser.add_argument('--token', '-t', type=str, default=def_token)
    parser.add_argument('--database', '-d', type=str, default=def_db)
    return parser.parse_args()

def main():
    global args
    import uvicorn
    load_dotenv()
    args = get_args()
    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()