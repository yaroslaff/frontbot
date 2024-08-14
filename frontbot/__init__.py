from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_simple_auth import SimpleAuth, logged_in_user
from pydantic_settings import BaseSettings
import requests
from requests.exceptions import RequestException
import markdown2
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv


__version__ = '0.1.0'

app = FastAPI()

load_dotenv()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class Settings(BaseSettings):
    auth_secret_key: str = "secret_key"
    app_url: str = "http://localhost:8899/frontbot"
    app_userid_header: str = "X-UserID"
    app_token: str | None = None

settings = Settings()

simpleauth = SimpleAuth(app)

@app.get("/")
async def frontbot_view(rq: Request, user: logged_in_user) -> str:    

    headers = {
        "Authorization": f"Bearer {settings.app_token}",
        "X-UserID": user.uuid,
        "X-Username": user.username
    }

    try:
        r = requests.get(settings.app_url, headers=headers)
    except RequestException as e:
        return templates.TemplateResponse(
            request=rq, name="index.html", context={"content": "", "error": e }
        )

    if r.status_code:
        return templates.TemplateResponse(
            request=rq, name="index.html", context={"content": "", "error": f"Bad status code {r.status_code} from app endpoint" }
        )


    rj = r.json()

    print(rj)

    if rj['text']:
        html_content = markdown2.markdown(rj['text'])
    else:
        html_content = None

    return templates.TemplateResponse(
        request=rq, name="index.html", context={"content": html_content, "error": rj['error'] }
    )


def main():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
