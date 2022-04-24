import mysql.connector
from flask import Flask, render_template,request,redirect, session,flash
import re


mydb = None

try:
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        db="project"
    );
except mysql.connector.Error as err:
    print(err)
    print("Please verify that the user, password, and host is correct and fix.")
    quit()


cursor = mydb.cursor()
app = Flask(__name__)
app.secret_key = "SJKaslkjdj12kldsal21"



def runSQLCommand(sql):
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(err)



def renderFormResults(sql):
    
    error = ""
    results = runSQLCommand(sql)


    #TODO:  Change executeMYSQL to have two other functions.  
    #These can better be able to handle errors and not require catching problems twice
    try:
        cursorFields = [i[0] for i in cursor.description]
        if(results != None):
            
            flash(cursorFields)
            for info in results:
                flash(info)
        else:
            error="No output obtained from the search"
    except Exception as e:
        print(e)

    
    return render_template("formResults.html",error=error)



@app.route("/")
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

@app.route("/employeeList")
def employeeList():

    return renderFormResults("Select * FROM EMPLOYEE");

@app.route("/showOrders")
def showOrders():
    return renderFormResults("Select * FROM ORDERS")

@app.route("/myEmployees")
def myEmployees():

    return renderFormResults("SELECT * FROM EMPLOYEE WHERE ManagerID = " + str(session["employeeID"]) + ";")

@app.route("/logout")
def logout():

    session.pop('loginInfo', default=None)
    session.pop('employeeID',default=None)
    return redirect("/")

@app.route("/findItems")
def findItems():
    return render_template("findItems.html")

@app.route("/findEmployees")
def findEmployees():
    return render_template("findEmployees.html")

@app.route("/findEmployeePost",methods=["POST"])
def findEmployeePost():
    employeeName = request.form["eName"]
    employeeID = request.form["eID"]
    
    #We need itemID to be something or else the SQL is an error.
    #itemID is always inputed as positive, so we can give -1.
    if(employeeID == "" or isinstance(employeeID,str)):
        employeeID = '-1'
    
    return renderFormResults("SELECT * FROM EMPLOYEE WHERE firstName = '" + employeeName + "' OR employeeID = " + employeeID + ";")


@app.route("/showItems")
def showItems():

    return renderFormResults("SELECT * FROM item;")

@app.route("/findItemPost",methods=["POST"])
def findItemPost():

    itemName = request.form["iName"]
    itemID = request.form["iID"]
    
    #We need itemID to be something or else the SQL is an error.
    #itemID is always inputed as positive, so we can give -1.
    if(itemID == "" or isinstance(itemID,str)):
        itemID = '-1'
    
    return renderFormResults("SELECT * FROM ITEM WHERE itemName = '" + itemName + "' OR itemID = " + itemID + ";")
    

@app.route("/orderItems")

 
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

    results = runSQLCommand("SELECT e.FirstName, e.LastName, e.position, e.EmployeeID FROM EMPLOYEE e JOIN loginInformation d ON d.EmployeeID = e.EmployeeID WHERE '" + username + "' = username AND '"+ password+"' = pssword;")
   
    if(len(results) == 0):
       error = "Invalid login info! Please re-enter login information"
       return render_template("login.html",error=error)

    
    session['loginInfo'] = results[0][2]
    session['employeeID'] = results[0][3]

    if(results[0][2] == "manager"):
        return redirect("/managerMain")
    elif(results[0][2] == "stocker"):
        return redirect("/stockerMain")
    else:
        return render_template("login.html",error=error)




@app.route("/totalSales/<string:mode>")
def totalSales(mode="month"):

    #to ensure it is easy to loop for the html, we will order the results by the month.
    sql = "SELECT SUM(e.boughtAmount) * p.price  AS MONTHINCOME, d." + mode + "Transacted FROM receiptBought e"
    sql += " JOIN RECEIPT d ON e.ReceiptID = d.RECEIPTID JOIN item p ON p.itemID = e.itemID GROUP BY d." + mode + "Transacted ORDER BY " + mode + "Transacted ASC;"
    
    results = runSQLCommand(sql)
    if(results != None):
        for info in results:
            flash(info)
    else:
        error="No output obtained from the search"
    
    return render_template("totalsales.html",mode=mode)

@app.route("/showReceipts/<string:mode>")
def showReceipts(mode="receiptID"):


    sql = "SELECT b.receiptID as RECEIPTID, SUM(b.boughtAmount * d.price) as TOTALSALES, e.hrTransacted, e.dayTransacted, e.monthTransacted FROM receiptBought b"
    sql += " JOIN item d on d.itemID = b.itemID JOIN receipt e ON e.receiptID = b.receiptID GROUP BY RECEIPTID ORDER BY " + mode + " DESC;"

    results = runSQLCommand(sql)
    cursorFields = [i[0] for i in cursor.description]
    try:
        if(results != None):
            flash(cursorFields)
            for info in results:
                flash(info)
        else:
            error="No output obtained from the search"
    except Exception as err:
        print(err)


    return render_template("showReceipts.html",mode=mode)








if __name__ == "__main__":
    app.run(debug=True)




