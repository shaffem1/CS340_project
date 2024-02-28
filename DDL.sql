
USE trailhead;

SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;
DROP TABLE IF EXISTS Customers, Products, Invoices, Returns, Reviews;



CREATE TABLE Customers (
customerID INT auto_increment NOT NULL PRIMARY KEY,
nameFirst VARCHAR(50) NOT NULL,
nameLast VARCHAR(50) NOT NULL,
address VARCHAR(50),
email VARCHAR(40) NOT NULL,
isPremiumMember BOOLEAN,
cellPhone VARCHAR(15),
homePhone VARCHAR(15),
CONSTRAINT fullName UNIQUE (nameFirst, nameLast)
);

CREATE TABLE Products (
	productID INT auto_increment NOT NULL PRIMARY KEY,
	brand VARCHAR(30) NOT NULL,
	productName VARCHAR(50) NOT NULL,
	price DECIMAL(19,2) NOT NULL,
	stockQty VARCHAR(5) NOT NULL,
	backOrdered BOOLEAN NOT NULL,
    	discontinued BOOLEAN NOT NULL,
	CONSTRAINT productName UNIQUE (brand, productName)
);

CREATE TABLE Invoices (
invoiceID INT auto_increment NOT NULL PRIMARY KEY,
	customerID INT NOT NULL,
	productID INT NOT NULL,
	invoiceDate DATE NOT NULL,
	invoiceAmount DECIMAL(19,2) NOT NULL,
	paymentMethod VARCHAR(10) NOT NULL,
	FOREIGN KEY (customerID) REFERENCES Customers(customerID) ON DELETE CASCADE,
	FOREIGN KEY (productID) REFERENCES Products(productID) ON DELETE CASCADE
	);

CREATE TABLE Returns (
	returnID INT auto_increment NOT NULL PRIMARY KEY,
	customerID INT NOT NULL,
	invoiceID INT NOT NULL,
	productID INT NOT NULL,
	FOREIGN KEY (productID) REFERENCES Products(productID) ON DELETE CASCADE,
	FOREIGN KEY (customerID) REFERENCES Customers(customerID) ON DELETE CASCADE,
	FOREIGN KEY (invoiceID) REFERENCES Invoices(invoiceID) ON DELETE CASCADE
	);

CREATE TABLE Reviews (
	reviewID INT auto_increment NOT NULL PRIMARY KEY,
	customerID INT,
	productID INT NOT NULL,
	reviewText VARCHAR(255),
	starRating DECIMAL,
	FOREIGN KEY (customerID) REFERENCES Customers(customerID) ON DELETE CASCADE,
	FOREIGN KEY (productID) REFERENCES Products(productID) ON DELETE CASCADE
	);

INSERT INTO Customers (nameFirst, nameLast, address, email, isPremiumMember, cellPhone, homePhone) VALUES ('Bob','Smith','5234 Main Street', 'bobsmith@gmail.com', '1', '202234523', '7032342124');

INSERT INTO Customers (nameFirst, nameLast, address, email, isPremiumMember, cellPhone, homePhone) VALUES ('Susan','Summers','123 First Street', 'susans@gmail.com', '0', '1234567890', '5552134545');

INSERT INTO Customers (nameFirst, nameLast, address, email, isPremiumMember, cellPhone, homePhone) VALUES ('Jane','Thomas','843 A Street', 'thomas_jane@gmail.com', '1', '6457421843', '8462578165');


INSERT INTO Products (brand, productName, price, stockQty, backOrdered, discontinued) VALUES ('North Face', 'Jacket', 175.00, '5', '0', '0');

INSERT INTO Products (brand, productName, price, stockQty, backOrdered, discontinued) VALUES ('Columbia', 'Pants', 109.50, '10', '0', '1');

INSERT INTO Products (brand, productName, price, stockQty, backOrdered, discontinued) VALUES ('Leki', 'Hiking Poles', 44.99, '3', '1', '0');


INSERT INTO Invoices (customerID, productID, invoiceDate, invoiceAmount, paymentMethod) VALUES ((SELECT customerID from Customers WHERE nameFirst = 'Jane' AND nameLast = 'Thomas'), (SELECT productID FROM Products WHERE brand = 'North Face' AND productName = 'Jacket'), 20240802, 175.00, 'Card');

INSERT INTO Invoices (customerID, productID, invoiceDate, invoiceAmount, paymentMethod) VALUES ((SELECT customerID from Customers WHERE nameFirst = 'Bob' AND nameLast = 'Smith'), (SELECT productID FROM Products WHERE brand = 'Columbia' AND productName = 'Pants'), 20240714, 109.50, 'Cash');

INSERT INTO Invoices (customerID, productID, invoiceDate, invoiceAmount, paymentMethod) VALUES ((SELECT customerID from Customers WHERE nameFirst = 'Bob' AND nameLast = 'Smith'), (SELECT productID FROM Products WHERE brand = 'Leki' AND productName = 'Hiking Poles'), 20240124, 44.99, 'Cash');


INSERT INTO Returns (productID, customerID, invoiceID) VALUES ((SELECT productID FROM Products WHERE brand = 'Columbia' AND productName = 'Pants'),
(SELECT customerID from Customers WHERE nameFirst = 'Bob' AND nameLast = 'Smith'),(SELECT invoiceID FROM Invoices WHERE customerID = (SELECT customerID from Customers WHERE nameFirst = 'Bob' AND nameLast = 'Smith') AND productID = (SELECT productID FROM Products WHERE brand = 'Columbia' AND productName = 'Pants'))
);

INSERT INTO Returns (productID, customerID, invoiceID) VALUES ((SELECT productID FROM Products WHERE brand = 'North Face' AND productName = 'Jacket'),(SELECT customerID from Customers WHERE nameFirst = 'Jane' AND nameLast = 'Thomas'),(SELECT invoiceID FROM Invoices WHERE customerID = (SELECT customerID from Customers WHERE nameFirst = 'Jane' AND nameLast = 'Thomas') AND productID = (SELECT productID FROM Products WHERE brand = 'North Face' AND productName = 'Jacket'))
);

INSERT INTO Returns (productID, customerID, invoiceID) VALUES ((SELECT productID FROM Products WHERE brand = 'Leki' AND productName = 'Hiking Poles'),(SELECT customerID from Customers WHERE nameFirst = 'Bob' AND nameLast = 'Smith'),(SELECT invoiceID FROM Invoices WHERE customerID = (SELECT customerID from Customers WHERE nameFirst = 'Bob' AND nameLast = 'Smith') AND productID = (SELECT productID FROM Products WHERE brand = 'Leki' AND productName = 'Hiking Poles'))
);


INSERT INTO Reviews (customerID, productID, reviewText, starRating) VALUES ((SELECT customerID from Customers WHERE nameFirst = 'Bob' AND nameLast = 'Smith'), (SELECT productID FROM Products WHERE brand = 'North Face' AND productName = 'Jacket'), 'Product works great!', 5);

INSERT INTO Reviews (customerID, productID, reviewText, starRating) VALUES ((SELECT customerID from Customers WHERE nameFirst = 'Susan' AND nameLast = 'Summers'), (SELECT productID FROM Products WHERE brand = 'Leki' AND productName = 'Hiking Poles'), 'Poles helped my stability on rough terrain!', 5);

INSERT INTO Reviews (customerID, productID, reviewText, starRating) VALUES ((SELECT customerID from Customers WHERE nameFirst = 'Jane' AND nameLast = 'Thomas'), (SELECT productID FROM Products WHERE brand = 'Columbia' AND productName = 'Pants'), 'Fit was not as expected.', 2);


SET FOREIGN_KEY_CHECKS=1;
COMMIT;
