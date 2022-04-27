from django.shortcuts import render
import mysql.connector
from flask import Flask, render_template,request,redirect, session,flash,jsonify
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
        raise err



#modes and filepath are usually set to None if the form is basically a select without any change.
#If there is more, they can be set to allow different SQL commands.
def renderFormResults(sql,modes = None,filepath = None):
    
    error = ""
    try:
        results = runSQLCommand(sql)
    except Exception as err:
        render_template("failure.html")

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



    
    return render_template("formResults.html",error=error, modes=modes, filepath=filepath)



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

@app.route("/showHazardousItems")
def hazardousItems():
    return renderFormResults("SELECT e.itemName, h.HazardType, h.HazardInfo FROM item e JOIN hazard h ON e.itemID = h.itemID;")

@app.route("/employeeList")
def employeeList():

    return renderFormResults("Select * FROM EMPLOYEE");

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
    
    #We need employeeID to be something or else the SQL is an error.
    #employeeID is always inputed as positive, so we can give -1.
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
    
@app.route("/addOrder")
def addOrder():

    return render_template("addOrder.html",numItems=1)

 
@app.route("/enlargeAddOrder",methods=["POST"])
def enlargeAddOrder():

    numItems = int(request.form.get("addItem"))
    return render_template("addOrder.html",numItems=numItems)


@app.route("/addOrderPost",methods=["POST"])
def addOrderPost():

    hr = request.form["hrTransacted"]
    day = request.form["dayTransacted"]
    month = request.form["monthTransacted"]

    try:
        runSQLCommand("INSERT INTO orders(hrTransacted,dayTransacted,monthTransacted,managerID) VALUES('" + hr + "','" + day + "','" + month + "'," + str(session['employeeID']) + ");")
    except Exception as err:
        return render_template("failure.html")

    numItems = int(request.form.get("numItems"))


    try:
        for i in range(1,numItems+1):
            itemID = request.form["itemID-" + str(i)]
            orderAmount = request.form["orderAmount-" + str(i)]
            result = runSQLCommand("INSERT INTO itemOrder(orderID,itemID,orderAmount) SELECT LAST_INSERT_ID() , " + itemID + " , " + orderAmount + ";")
    except Exception as err:
        print("Failure to load")
        mydb.rollback()
        return render_template("failure.html")


    
    print("Committing")
    mydb.commit()
    return render_template("success.html")

@app.route("/loginPost", methods=["POST"])
def loginPost():
    
    username = request.form["usName"]
    password = request.form["usPass"]
    error = None

    try:
        results = runSQLCommand("SELECT e.FirstName, e.LastName, e.position, e.EmployeeID FROM EMPLOYEE e JOIN loginInformation d ON d.EmployeeID = e.EmployeeID WHERE '" + username + "' = username AND '"+ password+"' = pssword;")
    except Exception as err:
        error = "Invalid login attempt! Please re-enter login information"
        return render_template("login.html",error=error)

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




@app.route("/showOrders/<string:mode>")
def showOrders(mode="ORDERID",filepath="showOrders"):

    sql = "SELECT b.OrderID as ORDERID, SUM(b.orderAmount * d.price) as TOTALCOST, e.managerID as MANAGERID, p.firstName, p.lastName, e.hrTransacted, e.dayTransacted, e.monthTransacted FROM itemorder b"
    sql += " JOIN item d on d.itemID = b.itemID JOIN orders e ON e.OrderID = b.OrderID JOIN employee p on e.managerID = p.employeeID GROUP BY ORDERID ORDER BY " + mode + " DESC;"

    return renderFormResults(sql,modes = ["ORDERID","TOTALCOST","MANAGERID"],filepath=filepath)


@app.route("/totalSales/<string:mode>")
def totalSales(mode="month",filepath="totalSales"):

    #to ensure it is easy to loop for the html, we will order the results by the month.
    sql = "SELECT SUM(e.boughtAmount) * p.price  AS MONTHINCOME, d." + mode + "Transacted FROM receiptBought e"
    sql += " JOIN RECEIPT d ON e.ReceiptID = d.RECEIPTID JOIN item p ON p.itemID = e.itemID GROUP BY d." + mode + "Transacted ORDER BY " + mode + "Transacted ASC;"
    
    return renderFormResults(sql,modes = ["hr","day","month"],filepath=filepath)

@app.route("/showReceipts/<string:mode>")
def showReceipts(mode="receiptID",filepath="showReceipts"):


    sql = "SELECT b.receiptID as RECEIPTID, SUM(b.boughtAmount * d.price) as TOTALSALES, e.hrTransacted, e.dayTransacted, e.monthTransacted FROM receiptBought b"
    sql += " JOIN item d on d.itemID = b.itemID JOIN receipt e ON e.receiptID = b.receiptID GROUP BY RECEIPTID ORDER BY " + mode + " DESC;"

    return renderFormResults(sql,modes = ["RECEIPTID","TOTALSALES"],filepath=filepath)

@app.route("/netInventory/<string:mode>")
def netInventory(mode="ITEM", filepath="netInventory"):

    sql = "select p.itemName as ITEM, SUM(b.orderAmount) - SUM(r.boughtAmount) as  NETITEMSGAINED, SUM(r.boughtAmount) * p.price - SUM(b.orderAmount) * p.price as NETGAIN FROM item p LEFT JOIN itemorder b ON b.itemID = p.itemID LEFT JOIN receiptBought r ON p.itemID = r.itemID GROUP BY ITEM ORDER BY " + mode + " DESC;"
    
    return renderFormResults(sql,modes = ["ITEM","NETITEMSGAINED","NETGAIN"],filepath=filepath)

@app.route("/managerItemsOrdered/<string:mode>")
def managerTotalOrders(mode="TOTALITEMORDERS", filepath="managerItemsOrdered"):
    sql = "SELECT o.managerID, e.firstName as FIRSTNAME, e.lastName, SUM(i.orderAmount) as TOTALITEMORDERS, SUM(i.orderAmount * p.price) as TOTALCOST FROM orders o JOIN employee e ON o.managerID = e.employeeID JOIN itemOrder i ON o.orderID = i.orderID JOIN item p ON p.itemID = i.itemID GROUP BY o.managerID ORDER BY " + mode + " DESC;"

    return renderFormResults(sql, modes=["TOTALITEMORDERS","TOTALCOST","FIRSTNAME"],filepath=filepath)








if __name__ == "__main__":
    app.run(debug=True)




