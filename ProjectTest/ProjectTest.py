import os
import mysql.connector
from flask import Flask, render_template,request,redirect, session,flash



mydb = None
try:

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database="project"
        );

except mysql.connector.Error as err:
    print("An error occurred connecting to the database.  Please verify if it is correct.")
    quit()


cursor = mydb.cursor()
app = Flask(__name__)
app.secret_key = "SJKaslkjdj12kldsal21"

@app.route("/")
@app.route("/index")
def main_page(name=None):
    return render_template("main.html")


@app.route("/login")
def login():
    error = ""
    return render_template("login.html",error=error)


@app.route("/managerMain")
def managerMain():
     return render_template("managerMain.html")


@app.route("/stockerMain")
def stockerMain():
     return render_template("stockerMain.html")


@app.route("/logout")
def logout():

    session.pop('loginInfo', default=None)
    return redirect("/")


@app.route("/findItems")
def findItems():
    return render_template("findItems.html")


@app.route("/showItems")
def showItems():
    sql = "SELECT * FROM item;"

    cursor.execute(sql)
    results = cursor.fetchall()

    for info in results:
        flash(info)

    return render_template("showItems.html")
    


@app.route("/loginPost", methods=["POST"])
def loginPost():
    
    username = request.form["usName"]
    password = request.form["usPass"]
    error = None

    print("Preparing for query")
    sql = "SELECT FirstName, LastName,position FROM EMPLOYEE e JOIN loginInformation d ON d.EmployeeID = e.EmployeeID WHERE '" + username + "' = username AND '"+ password+"' = pssword;"
    cursor.execute(sql)

    results = cursor.fetchall()
    #Grab information deliniating between a manager and a stocker.
   

    print(results)
    if(len(results) == 0):
       error = "Invalid login info! Please re-enter login information"
       return render_template("login.html",error=error)

    session['loginInfo'] = results[0][2]

    if(results[0][2] == "manager"):
        return redirect("/managerMain")
    elif(results[0][2] == "stocker"):
        return redirect("/stockerMain")
    else:
        error = "Invalid login information"
        return render_template("login.html",error=error)





if __name__ == "__main__":
    app.run(debug=True)




