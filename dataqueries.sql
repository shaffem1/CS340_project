Customers operations

Create
INSERT INTO Customers (nameFirst, nameLast, address, email, isPremiumMember, cellPhone, homePhone)
VALUES ('John', 'Doe', '123 Main St', 'john.doe@example.com', 1, '123-456-7890', '098-765-4321');
Read
SELECT * FROM Customers;
Update 
UPDATE Customers
SET address = ‘123 Main Street’
WHERE CustomerID=1;
Delete
DELETE FROM Customers
WHERE CustomerID=1;

Products operations
Create
INSERT INTO Products (brand, productName, price, stockQty, backOrdered, discontinued)
VALUES ('Nike', 'Running Shoes', 99.99, '10', 0, 0);
Read
SELECT * FROM Products;
Update
UPDATE Products
SET price=145.34
WHERE ProductID=3;
Delete
DELETE FROM Products WHERE productID=1;

Invoices operations
Create
Read
SELECT * FROM Invoices;
Update
Delete
DELETE FROM Invoices WHERE invoiceID=2;

Returns operations
Create
INSERT INTO Invoices (customerID, productID, invoiceDate, invoiceAmount, paymentMethod)
VALUES (1, 1, '2024-02-15', 99.99, 'Credit Card');
Read
SELECT * FROM Returns;
Update
UPDATE Invoices
SET paymentMethod=’PayPal’
WHERE invoiceID=3;
Delete
DELETE FROM Returns WHERE returnID=2;

Reviews operations
Create 
INSERT INTO Reviews (customerID, productID, reviewText, starRating)
VALUES (1, 1, 'Great product!', 5);
Read
SELECT * FROM Reviews;
Update 
UPDATE Reviews
SET starRating=4
WHERE reviewID=2;
Delete
DELETE FROM Reviews WHERE reviewID=4;

