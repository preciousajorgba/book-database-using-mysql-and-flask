from flask import Flask, request, render_template, redirect
from mysql_config import dbConfig
import mysql.connector as pyo

con = pyo.connect(**dbConfig)
#print(con)

cursor = con.cursor()

app = Flask(__name__)


def view():   #readnotes function
    cursor.execute("SELECT * FROM books")
    rows =cursor.fetchall()
    return rows
    
    
#create notes function
def insert(title, author, isbn):
    sql=("INSERT INTO books(title,author,isbn)VALUES (%s,%s,%s)")
    values =[title,author,isbn]
    cursor.execute(sql,values)
    con.commit()
       
#update notes
def update(id, title, author, isbn):# replace text input field with title and add two others for author and isbn
    tsql = 'UPDATE books SET  title = %s, author = %s, isbn = %s WHERE id=%s'
    cursor.execute(tsql, [title,author,isbn,id])
    con.commit()
        
    
#deletesnote
def delete( id):
    delquery ='DELETE FROM books WHERE id = %s'
    cursor.execute(delquery, [id])
    con.commit()
        


@app.route("/",methods=['GET','POST'])
def main():
    con = pyo.connect(**dbConfig)
    cursor = con.cursor()
    if request.method=="POST":
        title=request.form["title"]
        author=request.form["author"]
        isbn=request.form["isbn"]
        insert(title,author,isbn)
        
    return render_template('index.html', notes=view()) 

@app.route("/update/<note_id>", methods=['POST','GET'])
def Update(note_id):
    the_id=note_id
    title=request.form["title"]
    author=request.form["author"]
    isbn=request.form["isbn"]
    update(the_id,title,author,isbn)
    return redirect("/",code=302)

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def Delete(id):
    d_id=id
    delete(d_id)
    return redirect("/",code=302)


