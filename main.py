from fastapi import FastAPI,Request,Form
import mysql.connector
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from starlette.responses import RedirectResponse

templates=Jinja2Templates(directory='templates')
app=FastAPI()


mydb= mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='login'
    )
mycursor=mydb.cursor()
@app.get('/')
def hello(request:Request):
    mycursor.execute('select * from contact')
    contact=mycursor.fetchall()
    return templates.TemplateResponse("contact.html", {"request": request,'contact':contact})


@app.get('/SHOW1')
def create1(request:Request):
    return templates.TemplateResponse("index.html",{'request':request})



@app.post('/crt')
def create(request:Request,name:str=Form(...),pn:int=Form(...),mail:str=Form(...),rltn:str=Form(...)):
    sql='INSERT into contact(name,phone_no,email_id,relation) values (%s,%s,%s,%s)'
    val=(name,pn,mail,rltn)
    mycursor.execute(sql,val)
    mydb.commit()
    return RedirectResponse("/", status_code=302)
import uvicorn

uvicorn.run(app)