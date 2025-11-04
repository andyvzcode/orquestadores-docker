from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """<!doctype html>
    <html lang="es">
      <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width,initial-scale=1"/>
        <title>Hola Mundo - FastAPI</title>
      </head>
      <body>
        <h1>Hola mundo desde FastAPI!</h1>
        <p>Andres, esto es HTML servido por FastAPI.</p>
      </body>
    </html>"""


@app.get("/nodejs", response_class=HTMLResponse)
async def nodejs():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://nodejs:3000")
        return f"HTML desde Node.js con FastAPI: {response.text}"
