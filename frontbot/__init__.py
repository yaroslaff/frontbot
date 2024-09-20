from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_simple_auth import SimpleAuth, logged_in_user
from pydantic_settings import BaseSettings
import requests
from requests.exceptions import RequestException
import markdown2
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import json


__version__ = '0.1.0'

app = FastAPI()

load_dotenv()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class Settings(BaseSettings):
    app_title: str = "FrontBot protected application"
    app_url: str = "http://localhost:8899/frontbot"
    app_userid_header: str = "X-UserID"
    app_token: str | None = None

settings = Settings()

simpleauth = SimpleAuth(app)

def get_remote_ip(rq: Request) -> str:
    return rq.headers.get('x-forwarded-for', rq.client.host).split(',')[0]


# @app.route("/", methods=["GET", "POST"])
@app.get("/")
@app.post("/") 
async def frontbot_view(rq: Request, user: logged_in_user) -> str:    

    debug = False

    headers = {
        "Authorization": f"Bearer {settings.app_token}",
        "X-UserID": user.uuid,
        "X-Username": user.username,
        "X-Remote-IP": get_remote_ip(rq)
    }
   
    try:
        if rq.method == "GET":
            r = requests.get(settings.app_url, headers=headers)
        else:
            form = await rq.form()
            r = requests.post(settings.app_url, headers=headers, data=form)
    
    except RequestException as e:
        return templates.TemplateResponse(
            request=rq, name="index.html", context={"content": "", "error": e }
        )

    if r.status_code != 200:
        return templates.TemplateResponse(
            request=rq, name="index.html", context={"content": "", "error": f"Bad status code {r.status_code} from app endpoint" }
        )

    rj = r.json()

    if debug:
        print(rj)

    if rj['text']:
        html_content = markdown2.markdown(rj['text'])
    else:
        html_content = None

    if rj['popup']:
        popup_content = markdown2.markdown(rj['popup'])
    else:
        popup_content = None

    return templates.TemplateResponse(
        request=rq, name="index.html", context={
            "title": settings.app_title,
            "content": html_content, 
            "error": rj['error'], 
            "forms": rj['forms'], 
            "popup": popup_content,
            "debug": debug,
            "response": json.dumps(rj, indent=4) 
            }
    )


def main():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
