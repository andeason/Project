import os
import mysql.connector
from flask import Flask, render_template,request,redirect, session,flash
import re



mydb = None
try:

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        db = "project"
        );

except mysql.connector.Error as err:
    print(mysql.connector.Error)
    print("An error occurred connecting to the database.")
    print("This is likely due to the username and password being incorrect")
    print("Please verify that the mydb's username and password are correct in ProjectTest and retry")
    quit()




cursor = mydb.cursor()
app = Flask(__name__)
app.secret_key = "SJKaslkjdj12kldsal21"

#Since the table might not have been created, this serves to automatically select the table for this situation.
try:
    cursor.execute("use project;")
    print("Project exists.  Going as planned")
except mysql.connector.Error as err:
    print("The project database has not been created yet!")
    print("Before running any commands, please run the button 'only click if initalizing'")



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
    
@app.route("/createDatabase")
def createDatabase():
    return render_template("createDatabase.html")

@app.route("/initializeDatabase")
def initializeDatabase():
    global cursor
    statement = ""
    for line in open('projectScript.sql'):
        #This is gonna take some time to implemenet.
        if not (re.search(r';$',line)):
            statement = statement + line
        else:
            statement = statement + line
            print("Running " + statement)
            try:
                cursor.execute(statement)
                if(statement[0:4] != "DROP" and statement[0:16] != "CREATE DATABASE"):
                    cursor.close()
                    mydb.reconnect()
                    cursor = mydb.cursor()
                print("Statement executed")
            except mysql.connector.Error as e:
                print(e)
                print("Error reading")
            statement = ""


    print("The project file should be created now.")
    return redirect("/")


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




