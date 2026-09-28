DROP DATABASE IF EXISTS FoodTruckFestival;
CREATE DATABASE FoodTruckFestival;
USE FoodTruckFestival;

/* Location Table */
CREATE TABLE Location (
    LocationID INT PRIMARY KEY,
    LocationName VARCHAR(100),
    StreetAddress VARCHAR(100),
    City VARCHAR(50),
    State VARCHAR(50),
    Zipcode VARCHAR(10)
);

/* Vendor Table */
CREATE TABLE Vendor (
    VendorID INT PRIMARY KEY,
    CompanyName VARCHAR(100),
    ContactName VARCHAR(100),
    Email VARCHAR(100),
    Phone VARCHAR(15),
    TaxID VARCHAR(20)
);

/* Customer Table */
CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100),
    Phone VARCHAR(15),
    CreatedAt DATETIME
);

/* Event Table */
CREATE TABLE `Event` (
    EventID INT PRIMARY KEY,
    EventName VARCHAR(100),
    StartDateTime DATETIME,
    EndDateTime DATETIME,
    LocationID INT,
    FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
);

/* FoodTruck Table */
CREATE TABLE FoodTruck (
    TruckID INT PRIMARY KEY,
    TruckName VARCHAR(100),
    LicensePlate VARCHAR(20),
    VendorID INT,
    FOREIGN KEY (VendorID) REFERENCES Vendor(VendorID)
);

/* EventRegistration Table */
CREATE TABLE EventRegistration (
    RegistrationID INT PRIMARY KEY,
    BoothNumber VARCHAR(20),
    RegistrationDate DATE,
    EventID INT,
    TruckID INT,
    FOREIGN KEY (EventID) REFERENCES `Event`(EventID),
    FOREIGN KEY (TruckID) REFERENCES FoodTruck(TruckID)
);

/* MenuItem Table */
CREATE TABLE MenuItem (
    MenuItemID INT PRIMARY KEY,
    ItemName VARCHAR(100),
    Description TEXT,
    Price DECIMAL(6,2),
    DietaryFlags VARCHAR(50),
    Availability BOOLEAN,
    TruckID INT,
    FOREIGN KEY (TruckID) REFERENCES FoodTruck(TruckID)
);

/* CustomerOrder Table */
CREATE TABLE CustomerOrder (
    OrderID INT PRIMARY KEY,
    OrderDateTime DATETIME,
    OrderStatus VARCHAR(20),
    TotalAmount DECIMAL(8,2),
    PaymentMethod VARCHAR(50),
    CustomerID INT,
    RegistrationID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (RegistrationID) REFERENCES EventRegistration(RegistrationID)
);

/* OrderItem Table */
CREATE TABLE OrderItem (
    OrderID INT,
    MenuItemID INT,
    Quantity INT,
    UnitPriceAtSale DECIMAL(6,2),
    PRIMARY KEY (OrderID, MenuItemID),
    FOREIGN KEY (OrderID) REFERENCES CustomerOrder(OrderID),
    FOREIGN KEY (MenuItemID) REFERENCES MenuItem(MenuItemID)
);

/* SAMPEL DATA */
/* Sample data was created by chatGPT but verified by us*/

INSERT INTO Location
(LocationID, LocationName, StreetAddress, City, State, Zipcode)
VALUES
(1, 'Prescott Courthouse Plaza', '120 S Cortez St', 'Prescott', 'AZ', '86303'),
(2, 'Watson Lake Park', '3101 Watson Lake Rd', 'Prescott', 'AZ', '86301');

/* Vendors */
INSERT INTO Vendor
(VendorID, CompanyName, ContactName, Email, Phone, TaxID)
VALUES
(1, 'High Desert Eats LLC', 'Maria Lopez', 'maria@highdeserteats.com', '928-555-0101', 'AZ-10001'),
(2, 'Copper State Foods LLC', 'Daniel Kim', 'daniel@copperstatefoods.com', '928-555-0102', 'AZ-10002'),
(3, 'Mountain Sweets Co', 'Rachel Green', 'rachel@mountainsweets.com', '928-555-0103', 'AZ-10003');

/* Customers */
INSERT INTO Customer
(CustomerID, FirstName, LastName, Email, Phone, CreatedAt)
VALUES
(1, 'James', 'Carter', 'jcarter@example.com', '928-555-0201', '2026-09-20 10:15:00'),
(2, 'Olivia', 'Martinez', 'olivia.m@example.com', '928-555-0202', '2026-09-21 13:30:00'),
(3, 'Ethan', 'Brooks', 'ethan.b@example.com', '928-555-0203', '2026-09-22 09:45:00'),
(4, 'Sophia', 'Nguyen', 'sophia.n@example.com', '928-555-0204', '2026-09-23 16:20:00');

/* Events */
INSERT INTO `Event`
(EventID, EventName, StartDateTime, EndDateTime, LocationID)
VALUES
(1, 'Prescott Fall Food Truck Festival', '2026-10-10 11:00:00', '2026-10-10 19:00:00', 1),
(2, 'Watson Lake Food Truck Night', '2026-10-24 16:00:00', '2026-10-24 21:00:00', 2);

/* Food Trucks */
INSERT INTO FoodTruck
(TruckID, TruckName, LicensePlate, VendorID)
VALUES
(1, 'Desert Taco Co.', 'AZTACO1', 1),
(2, 'Copper Burger Bus', 'AZBURG2', 2),
(3, 'Summit Sweets', 'AZSWT03', 3);

INSERT INTO EventRegistration
(RegistrationID, BoothNumber, RegistrationDate, EventID, TruckID)
VALUES
(1, 'A1', '2026-09-15', 1, 1),
(2, 'A2', '2026-09-16', 1, 2),
(3, 'B1', '2026-09-17', 1, 3),
(4, 'C1', '2026-09-20', 2, 1),
(5, 'C2', '2026-09-21', 2, 2);

/* Menu Items */
INSERT INTO MenuItem
(MenuItemID, ItemName, Description, Price, DietaryFlags, Availability, TruckID)
VALUES
(1, 'Carne Asada Taco', 'Grilled steak taco with onion and cilantro', 4.50, NULL, TRUE, 1),
(2, 'Veggie Taco', 'Roasted vegetable taco with salsa verde', 4.00, 'Vegetarian', TRUE, 1),
(3, 'Classic Burger', 'Beef burger with lettuce, tomato, and house sauce', 9.50, NULL, TRUE, 2),
(4, 'Loaded Fries', 'French fries topped with cheese and grilled onions', 6.50, 'Vegetarian', TRUE, 2),
(5, 'Churro Bites', 'Cinnamon sugar churro bites', 5.00, 'Vegetarian', TRUE, 3),
(6, 'Chocolate Brownie', 'Fudge brownie with powdered sugar', 4.50, 'Vegetarian', FALSE, 3);

/* Customer Orders */
INSERT INTO CustomerOrder
(OrderID, OrderDateTime, OrderStatus, TotalAmount, PaymentMethod, CustomerID, RegistrationID)
VALUES
(1, '2026-10-10 12:05:00', 'Completed', 13.00, 'Card', 1, 1),
(2, '2026-10-10 12:20:00', 'Completed', 16.00, 'Cash', 2, 2),
(3, '2026-10-10 14:10:00', 'Completed', 10.00, 'Card', 3, 3),
(4, '2026-10-24 17:35:00', 'Completed', 8.50, 'Card', 4, 4);

/* Order Items */
INSERT INTO OrderItem
(OrderID, MenuItemID, Quantity, UnitPriceAtSale)
VALUES
(1, 1, 2, 4.50),
(1, 2, 1, 4.00),
(2, 3, 1, 9.50),
(2, 4, 1, 6.50),
(3, 5, 2, 5.00),
(4, 1, 1, 4.50),
(4, 2, 1, 4.00);

/*VERIFICAITON*/

SHOW TABLES;

SELECT * FROM Location;
SELECT * FROM Vendor;
SELECT * FROM Customer;
SELECT * FROM `Event`;
SELECT * FROM FoodTruck;
SELECT * FROM EventRegistration;
SELECT * FROM MenuItem;
SELECT * FROM CustomerOrder;
SELECT * FROM OrderItem;


