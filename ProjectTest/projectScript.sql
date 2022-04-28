DROP DATABASE IF EXISTS project;
CREATE DATABASE project;
USE project; 


CREATE TABLE EMPLOYEE(
	EmployeeID INT NOT NULL AUTO_INCREMENT,
    FirstName varchar(50) NOT NULL,
    LastName varchar(50) NOT NULL,
    position varchar(50) NOT NULL,
    workLocation varChar(20) DEFAULT NULL,
    ManagerID INT,
    
    PRIMARY KEY(EmployeeID),
    FOREIGN KEY(ManagerID) REFERENCES EMPLOYEE(EmployeeID)
);


CREATE TABLE ITEM(
	itemID int(9) NOT NULL AUTO_INCREMENT,
    buyPrice int(10) DEFAULT 0,
    sellPrice int(10) DEFAULT 0,
    itemName varchar(100) NOT NULL,
    itemDescription varChar(250) DEFAULT NULL,
    Location varChar(100) NOT NULL,
	PRIMARY KEY(itemID)
    
);

CREATE TABLE HAZARD(
	itemID INT NOT NULL,
    HazardType varChar(40) NOT NULL,
    HazardInfo varChar(100) NOT NULL,
    
    PRIMARY KEY(HazardType),
    FOREIGN KEY(itemID) REFERENCES ITEM(itemID)
	ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE RECEIPT(
	ReceiptID INT NOT NULL AUTO_INCREMENT,
    hrTransacted INT NOT NULL,
    dayTransacted INT NOT NULL,
    monthTransacted INT NOT NULL,
    
    PRIMARY KEY(ReceiptID)
);

CREATE TABLE ORDERS(
	OrderID INT NOT NULL AUTO_INCREMENT,
    hrTransacted INT NOT NULL,
    dayTransacted INT NOT NULL,
    monthTransacted INT NOT NULL,
    managerID INT NOT NULL,
    
    PRIMARY KEY(OrderID),
    FOREIGN KEY(managerID) REFERENCES EMPLOYEE(EmployeeID)
    ON UPDATE CASCADE ON DELETE CASCADE

);


CREATE TABLE receiptBought(

	ReceiptID INT NOT NULL AUTO_INCREMENT,
    itemID INT NOT NULL,
    boughtAmount INT DEFAULT 1,
    
    FOREIGN KEY(ReceiptID) REFERENCES Receipt(ReceiptID)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(itemID) REFERENCES Item(itemID) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE itemOrder(
	OrderID INT NOT NULL,
    itemID int NOT NULL,
    orderAmount int DEFAULT 1,
    
    FOREIGN KEY(OrderID) REFERENCES Orders(OrderID)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(itemID) REFERENCES Item(itemID) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO EMPLOYEE(EmployeeID,FirstName,LastName,position) VALUES (1,"Johnny","Sins","manager");
INSERT INTO EMPLOYEE(FirstName,LastName,workLocation,ManagerID,position) VALUES ("Babe", "Truth","Front",1,"stocker");
INSERT INTO EMPLOYEE(FirstName,LastName,workLocation,ManagerID,position) VALUES ("Lanna", "Loanna","Back",1,"stocker");
INSERT INTO EMPLOYEE(FirstName,LastName,workLocation,ManagerID,position) VALUES ("Hefty", "Creft","Middle",1,"stocker");
INSERT INTO EMPLOYEE(EMPLOYEEID,FirstName,LastName,position) VALUES (5,"Clutch","Cargo","manager");
INSERT INTO EMPLOYEE(FirstName,LastName,workLocation,ManagerID,position) VALUES ("Emmanual", "GoldStein","Middle",5,"stocker");
INSERT INTO EMPLOYEE(FirstName,LastName,workLocation,ManagerID,position) VALUES ("Winston", "Smith","Front",5,"stocker");

INSERT INTO ITEM(itemID, buyPrice,sellPrice, location,itemName,itemDescription) VALUES(17,100,150,"front","3KG PEANUTS","Who doesnt like peanuts?");
INSERT INTO ITEM(itemID, buyPrice,sellPrice, location,itemName) VALUES(21,15,30,"back","MEDSHIRT");
INSERT INTO ITEM(itemID, buyPrice,sellPrice, location, itemName) VALUES(86,4,6,"middle","APPLES");
INSERT INTO ITEM(itemID, buyPrice,sellPrice, location, itemName) VALUES(25,5,7,"BACK","ORANGES");
INSERT INTO ITEM(itemID, buyPrice,sellPrice, location,itemName,itemDescription) VALUES(40,16,43,"FRONT","RADIOACTIVE WASTE","Someone buys this for some reason...");
INSERT INTO ITEM(itemID, buyPrice,sellPrice, location, itemName,itemDescription) VALUES(234,400,650,"BACK","TV","Expensive, but who doesnt want one?");

INSERT INTO HAZARD(itemID,HazardType,HazardInfo) VALUES(17,"allergies","Dont let this be exposed to those with allergies");
INSERT INTO HAZARD(itemID,HazardType,HazardInfo) VALUES(40,"Radiation","Even if you are a Cancer, you probably dont WANT Cancer");
INSERT INTO HAZARD(itemID,HazardType,HazardInfo) VALUES(40,"Toxic","Dont let near others.");


INSERT INTO RECEIPT(ReceiptID, hrTransacted, dayTransacted, monthTransacted) VALUES (912, 3,8,12);
INSERT INTO RECEIPT(ReceiptID, hrTransacted, dayTransacted, monthTransacted) VALUES(913,2,8,8);
INSERT INTO RECEIPT(ReceiptID, hrTransacted, dayTransacted, monthTransacted) VALUES(914,2,9,8);
INSERT INTO RECEIPT(ReceiptID, hrTransacted, dayTransacted, monthTransacted) VALUES(1012,7,12,9);


INSERT INTO receiptBought(ReceiptID, itemID, boughtAmount) VALUES (912,17,40);
INSERT INTO receiptBought(ReceiptID, itemID, boughtAmount) VALUES (912,17,2);
INSERT INTO receiptBought(ReceiptID, itemID, boughtAmount) VALUES (912,86,1000);
INSERT INTO receiptBought(ReceiptID, itemID, boughtAmount) VALUES (913,17,8);
INSERT INTO receiptBought(ReceiptID, itemID, boughtAmount) VALUES (913,21,10);
INSERT INTO receiptBought(ReceiptID, itemID, boughtAmount) VALUES (913,25,423);
INSERT INTO receiptBought(ReceiptID, itemID, boughtAmount) VALUES (914,17,1);
INSERT INTO receiptBought(ReceiptID, itemID, boughtAmount) VALUES (914,21,75);
INSERT INTO receiptBought(ReceiptID, itemID, boughtAmount) VALUES (914,25,3);
INSERT INTO receiptBought(ReceiptID, itemID, boughtAmount) VALUES (1012,40,10000);

INSERT INTO ORDERS(OrderID, hrTransacted, dayTransacted, monthTransacted, managerID) VALUES(15,7,12,3,1);
INSERT INTO ORDERS(OrderID, hrTransacted, dayTransacted, monthTransacted, managerID) VALUES(16,9,11,2,5);
INSERT INTO ORDERS(OrderID, hrTransacted, dayTransacted, monthTransacted, managerID) VALUES(17,10,1,4,1);
INSERT INTO ORDERS(OrderID, hrTransacted, dayTransacted, monthTransacted, managerID) VALUES(18,8,3,4,5);

INSERT INTO itemOrder(orderID, itemID, orderAmount) VALUES(15,17,200);
INSERT INTO itemOrder(orderID, itemID, orderAmount) VALUES(15,86,400);
INSERT INTO itemOrder(orderID, itemID, orderAmount) VALUES(16,40,500);
INSERT INTO itemOrder(orderID, itemID, orderAmount) VALUES(16,21,30);
INSERT INTO itemOrder(orderID, itemID, orderAmount) VALUES(16,17,687);
INSERT INTO itemOrder(orderID, itemID, orderAmount) VALUES(17,25,999);
INSERT INTO itemOrder(orderID, itemID, orderAmount) VALUES(18,21,36);
INSERT INTO itemOrder(orderID, itemID, orderAmount) VALUES(18,86,400);