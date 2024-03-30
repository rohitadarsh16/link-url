from bs4 import BeautifulSoup
import requests, json, lxml
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse  
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

origins = [
   "https://dashboardtool.vercel.app",
   "https://dashboardtool.vercel.app/",
    "http://localhost:3000",
    "http://localhost:3000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def getAllLinks(soup, query):
    data =[]
    div_data = soup.find_all('div',{'class': 'MjjYud'})
    for div in div_data:
        # urls = re.findall('https://vds.issgovernance.com/vds/#/\w+', div.text)
        urls = re.findall(rf'{query}\w+', div.text)
        for url in urls:
            data.append({'url': url})
    return data

async def getdatadiv(query):
    params = {
        "q": '"'+query+'"',         # query example
        "hl": "en",          # language
        "start": 0,          # number page by default up to 0
        "num": 9999999          # parameter defines the maximum number of results to return.
    }


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    
    url = "https://www.google.com/search"
    response = requests.get(url, headers=headers, params=params).text
    soup = BeautifulSoup(response, 'html.parser')
    data = await getAllLinks(soup, query)
    return data


@app.get("/geturl", response_class=JSONResponse)
async def read_item(query: str):
    data = await getdatadiv( query)
    return data
    
    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)