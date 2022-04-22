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
	itemID int(9) NOT NULL,
    price int(10) DEFAULT 0,
    quantity int(5) DEFAULT 0,
    itemName varchar(100) NOT NULL,
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
	ReceiptID INT NOT NULL,
    hrTransacted INT NOT NULL,
    dayTransacted INT NOT NULL,
    monthTransacted INT NOT NULL,
    
    PRIMARY KEY(ReceiptID)
);

CREATE TABLE ORDERS(
	OrderID INT NOT NULL,
    hrTransacted INT NOT NULL,
    dayTransacted INT NOT NULL,
    monthTransacted INT NOT NULL,
    managerID INT NOT NULL,
    
    PRIMARY KEY(OrderID),
    FOREIGN KEY(managerID) REFERENCES EMPLOYEE(EmployeeID)
    ON UPDATE CASCADE ON DELETE CASCADE

);


CREATE TABLE receiptBought(

	ReceiptID INT NOT NULL,
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

INSERT INTO ITEM(itemID, price, quantity,location,itemName) VALUES(17,100,30,"front","3KG PEANUTS");
INSERT INTO ITEM(itemID, price, quantity,location,itemName) VALUES(21,15,200,"back","MEDSHIRT");
INSERT INTO ITEM(itemID, price, quantity,location, itemName) VALUES(86,4,1000,"middle","APPLES");

INSERT INTO HAZARD(itemID,HazardType,HazardInfo) VALUES(17,"allergies","Dont let this be exposed to those with allergies");

INSERT INTO RECEIPT(ReceiptID, hrTransacted, dayTransacted, monthTransacted) VALUES (912, 3,8,21);


INSERT INTO receiptBought(ReceiptID, itemID, boughtAmount) VALUES (912,17,40);
INSERT INTO receiptBought(ReceiptID, itemID, boughtAmount) VALUES (912,17,2);

INSERT INTO ORDERS(OrderID, hrTransacted, dayTransacted, monthTransacted, managerID) VALUES (15,7,12,3,1);

INSERT INTO itemOrder(orderID, itemID, orderAmount) VALUES(15,17,200);
INSERT INTO itemOrder(orderID, itemID, orderAmount) VALUES(15,86,400);


CREATE TABLE LoginInformation
(
	username VARCHAR(20) NOT NULL,
    pssword VARCHAR(20) NOT NULL,
    EmployeeID int NOT NULL,
    
    PRIMARY KEY(username,EmployeeID),
    FOREIGN KEY(EmployeeID) REFERENCES EMPLOYEE(EmployeeID)
    
);

INSERT INTO LoginInformation(username,pssword,EmployeeID) VALUES("username","password",1);
INSERT INTO LoginInformation(username,pssword,EmployeeID) VALUES("bobby","mypass",2);
INSERT INTO LoginInformation(username,pssword,EmployeeID) VALUES("jonny","mypass",3);
INSERT INTO LoginInformation(username,pssword,EmployeeID) VALUES("donny","mypass",2);

