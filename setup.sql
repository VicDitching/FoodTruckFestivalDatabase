/* FoodTruckFestival setup script: schema, constraints, and all sample data.
   Run as root. Then run account.sql to create the application account. */

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

/* SAMPLE DATA */
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

/* ADDITIONAL SAMPLE DATA (generated with AI help, verified by us) */

INSERT INTO Location
(LocationID, LocationName, StreetAddress, City, State, Zipcode)
VALUES
(3, 'Pioneer Park', '1200 Commerce Dr', 'Prescott', 'AZ', '86305'),
(4, 'Prescott Valley Civic Center', '7501 E Skoog Blvd', 'Prescott Valley', 'AZ', '86314'),
(5, 'Chino Valley Memory Park', '1020 W Palomino Rd', 'Chino Valley', 'AZ', '86323');

INSERT INTO Vendor
(VendorID, CompanyName, ContactName, Email, Phone, TaxID)
VALUES
(4, 'Thumb Butte Grill LLC', 'Marcus Reed', 'marcus@thumbbuttegrill.com', '928-555-0104', 'AZ-10004'),
(5, 'Granite Dells Kitchen', 'Priya Shah', 'priya@granitedellskitchen.com', '928-555-0105', 'AZ-10005'),
(6, 'Whiskey Row BBQ Co', 'Tom Hollis', 'tom@whiskeyrowbbq.com', '928-555-0106', 'AZ-10006'),
(7, 'Saguaro Street Food LLC', 'Ana Torres', 'ana@saguarostreetfood.com', '928-555-0107', 'AZ-10007'),
(8, 'Bradshaw Bowls', 'Kevin Park', 'kevin@bradshawbowls.com', '928-555-0108', 'AZ-10008'),
(9, 'Pinon Pizza Works', 'Laura Bennett', 'laura@pinonpizza.com', '928-555-0109', 'AZ-10009'),
(10, 'Verde Valley Coffee Co', 'Sam Ortiz', 'sam@verdevalleycoffee.com', '928-555-0110', 'AZ-10010');

INSERT INTO Customer
(CustomerID, FirstName, LastName, Email, Phone, CreatedAt)
VALUES
(5, 'Liam', 'Walker', 'liam.walker@example.com', '928-555-0210', '2026-09-24 09:00:00'),
(6, 'Emma', 'Johnson', 'emma.johnson@example.com', '928-555-0211', '2026-09-24 10:13:00'),
(7, 'Noah', 'Garcia', 'noah.garcia@example.com', '928-555-0212', '2026-09-24 11:26:00'),
(8, 'Ava', 'Brown', 'ava.brown@example.com', '928-555-0213', '2026-09-25 12:39:00'),
(9, 'Mason', 'Davis', 'mason.davis@example.com', '928-555-0214', '2026-09-25 13:52:00'),
(10, 'Isabella', 'Wilson', 'isabella.wilson@example.com', '928-555-0215', '2026-09-25 14:05:00'),
(11, 'Lucas', 'Anderson', 'lucas.anderson@example.com', '928-555-0216', '2026-09-26 15:18:00'),
(12, 'Mia', 'Thomas', 'mia.thomas@example.com', '928-555-0217', '2026-09-26 16:31:00'),
(13, 'Elijah', 'Moore', 'elijah.moore@example.com', '928-555-0218', '2026-09-26 17:44:00'),
(14, 'Harper', 'Martin', 'harper.martin@example.com', '928-555-0219', '2026-09-27 09:57:00'),
(15, 'Benjamin', 'Lee', 'benjamin.lee@example.com', '928-555-0220', '2026-09-27 10:10:00'),
(16, 'Amelia', 'Clark', 'amelia.clark@example.com', '928-555-0221', '2026-09-27 11:23:00');

INSERT INTO `Event`
(EventID, EventName, StartDateTime, EndDateTime, LocationID)
VALUES
(3, 'Pioneer Park Harvest Feast', '2026-11-07 11:00:00', '2026-11-07 18:00:00', 3),
(4, 'Prescott Valley Holiday Bites', '2026-12-05 12:00:00', '2026-12-05 20:00:00', 4),
(5, 'Chino Valley Spring Food Fest', '2027-04-17 10:00:00', '2027-04-17 17:00:00', 5),
(6, 'Courthouse Plaza Summer Nights', '2027-06-12 17:00:00', '2027-06-12 22:00:00', 1);

/* More locations and events (AI-generated sample data) */
INSERT INTO Location
(LocationID, LocationName, StreetAddress, City, State, Zipcode)
VALUES
(6, 'Goldwater Lake Park', '2401 Senator Hwy', 'Prescott', 'AZ', '86303'),
(7, 'Yavapai County Fairgrounds', '10501 AZ-89A', 'Prescott Valley', 'AZ', '86315'),
(8, 'Fain Park', '3501 N Fain Rd', 'Prescott Valley', 'AZ', '86314'),
(9, 'Granite Creek Park', '554 6th St', 'Prescott', 'AZ', '86301'),
(10, 'Dewey-Humboldt Town Green', '2735 S Corral St', 'Dewey-Humboldt', 'AZ', '86327');

INSERT INTO `Event`
(EventID, EventName, StartDateTime, EndDateTime, LocationID)
VALUES
(7, 'Goldwater Lake Taco Takeover', '2027-05-08 11:00:00', '2027-05-08 17:00:00', 6),
(8, 'Yavapai County Fair Food Row', '2027-08-19 10:00:00', '2027-08-22 22:00:00', 7),
(9, 'Fain Park Fall Festival', '2027-09-25 11:00:00', '2027-09-25 18:00:00', 8),
(10, 'Granite Creek BBQ & Brews', '2027-07-17 16:00:00', '2027-07-17 22:00:00', 9),
(11, 'Dewey-Humboldt Pumpkin Patch Eats', '2027-10-16 10:00:00', '2027-10-16 16:00:00', 10),
(12, 'Watson Lake Winter Warm-Up', '2027-01-23 11:00:00', '2027-01-23 16:00:00', 2);

INSERT INTO FoodTruck
(TruckID, TruckName, LicensePlate, VendorID)
VALUES
(4, 'Thumb Butte Smash Burgers', 'AZTBSB4', 4),
(5, 'Dells Dumpling Wagon', 'AZDDW05', 5),
(6, 'Whiskey Row Smokehouse', 'AZWRS06', 6),
(7, 'Saguaro Elote Cart', 'AZSEC07', 7),
(8, 'Bradshaw Poke Bowls', 'AZBPB08', 8),
(9, 'Pinon Wood-Fired Pizza', 'AZPWF09', 9),
(10, 'Verde Valley Espresso', 'AZVVE10', 10),
(11, 'Desert Taco Co. Two', 'AZTACO2', 1),
(12, 'Pinon Slice Truck', 'AZPST12', 9);

INSERT INTO MenuItem
(MenuItemID, ItemName, Description, Price, DietaryFlags, Availability, TruckID)
VALUES
(7, 'Al Pastor Taco', 'Marinated pork taco with pineapple', 4.75, NULL, TRUE, 1),
(8, 'Chili Cheese Burger', 'Burger topped with green chile and pepper jack', 10.50, NULL, TRUE, 2),
(9, 'Lemon Bar', 'Shortbread lemon bar', 3.75, 'Vegetarian', TRUE, 3),
(10, 'Double Smash Burger', 'Two smashed patties with American cheese', 11.00, NULL, TRUE, 4),
(11, 'Garlic Parmesan Fries', 'Fries tossed in garlic butter and parmesan', 5.50, 'Vegetarian', TRUE, 4),
(12, 'Pork Dumplings (6)', 'Steamed pork and ginger dumplings', 8.00, NULL, TRUE, 5),
(13, 'Veggie Dumplings (6)', 'Cabbage, carrot, and mushroom dumplings', 7.50, 'Vegan', TRUE, 5),
(14, 'Brisket Plate', 'Smoked brisket with slaw and cornbread', 15.00, 'Gluten-Free', TRUE, 6),
(15, 'Pulled Pork Sandwich', 'Pulled pork on a brioche bun', 11.50, NULL, TRUE, 6),
(16, 'Mac and Cheese Cup', 'Smoked gouda mac and cheese', 5.00, 'Vegetarian', FALSE, 6),
(17, 'Street Corn (Elote)', 'Grilled corn with cotija, lime, and chile', 5.00, 'Vegetarian,Gluten-Free', TRUE, 7),
(18, 'Esquites Cup', 'Corn salad cup with crema and cotija', 5.50, 'Vegetarian,Gluten-Free', TRUE, 7),
(19, 'Ahi Poke Bowl', 'Ahi tuna over rice with edamame', 14.50, 'Gluten-Free', TRUE, 8),
(20, 'Tofu Poke Bowl', 'Marinated tofu over rice with seaweed salad', 12.50, 'Vegan', TRUE, 8),
(21, 'Margherita Pizza', 'Tomato, mozzarella, and basil', 13.00, 'Vegetarian', TRUE, 9),
(22, 'Pepperoni Pizza', 'Wood-fired pepperoni pizza', 14.00, NULL, TRUE, 9),
(23, 'Iced Latte', 'Double shot iced latte', 5.25, 'Vegetarian,Gluten-Free', TRUE, 10),
(24, 'Prickly Pear Lemonade', 'House prickly pear lemonade', 4.50, 'Vegan,Gluten-Free', TRUE, 10),
(25, 'Fish Taco', 'Beer-battered cod taco with cabbage slaw', 5.25, NULL, TRUE, 11),
(26, 'Bean and Cheese Burrito', 'Refried beans and cheddar burrito', 7.00, 'Vegetarian', TRUE, 11),
(27, 'Cheese Slice', 'Large New York style cheese slice', 4.50, 'Vegetarian', TRUE, 12),
(28, 'Garlic Knots (4)', 'Garlic knots with marinara', 5.00, 'Vegetarian', TRUE, 12);

INSERT INTO EventRegistration
(RegistrationID, BoothNumber, RegistrationDate, EventID, TruckID)
VALUES
(6, 'A3', '2026-09-18', 1, 4),
(7, 'A4', '2026-09-19', 1, 6),
(8, 'A5', '2026-09-20', 1, 7),
(9, 'B3', '2026-10-01', 2, 3),
(10, 'B4', '2026-10-02', 2, 5),
(11, 'B5', '2026-10-03', 2, 8),
(12, 'C1', '2026-10-10', 3, 1),
(13, 'C2', '2026-10-11', 3, 4),
(14, 'C3', '2026-10-12', 3, 5),
(15, 'C4', '2026-10-13', 3, 6),
(16, 'C5', '2026-10-14', 3, 9),
(17, 'C6', '2026-10-15', 3, 10),
(18, 'D1', '2026-11-02', 4, 2),
(19, 'D2', '2026-11-03', 4, 3),
(20, 'D3', '2026-11-04', 4, 7),
(21, 'D4', '2026-11-05', 4, 8),
(22, 'D5', '2026-11-06', 4, 11),
(23, 'E1', '2027-02-10', 5, 1),
(24, 'E2', '2027-02-11', 5, 9),
(25, 'E3', '2027-02-12', 5, 12),
(26, 'F1', '2027-04-20', 6, 4),
(27, 'F2', '2027-04-21', 6, 6),
(28, 'F3', '2027-04-22', 6, 10),
(29, 'G1', '2027-03-15', 7, 1),
(30, 'G2', '2027-03-16', 7, 11),
(31, 'G3', '2027-03-18', 7, 7),
(32, 'H1', '2027-06-01', 8, 2),
(33, 'H2', '2027-06-02', 8, 6),
(34, 'H3', '2027-06-05', 8, 9),
(35, 'H4', '2027-06-07', 8, 10),
(36, 'I1', '2027-08-01', 9, 3),
(37, 'I2', '2027-08-03', 9, 5),
(38, 'J1', '2027-05-20', 10, 6),
(39, 'J2', '2027-05-22', 10, 4),
(40, 'K1', '2027-09-01', 11, 3),
(41, 'K2', '2027-09-02', 11, 12),
(42, 'L1', '2026-11-01', 12, 10),
(43, 'L2', '2026-11-03', 12, 8);

INSERT INTO CustomerOrder
(OrderID, OrderDateTime, OrderStatus, TotalAmount, PaymentMethod, CustomerID, RegistrationID)
VALUES
(5, '2026-10-10 11:45:00', 'Completed', 27.50, 'Mobile Pay', 16, 6),
(6, '2026-10-10 13:58:00', 'Completed', 33.00, 'Cash', 4, 6),
(7, '2026-10-10 15:27:00', 'Completed', 9.25, 'Card', 1, 1),
(8, '2026-10-10 11:49:00', 'Completed', 18.75, 'Mobile Pay', 15, 3),
(9, '2026-10-10 12:06:00', 'Completed', 13.75, 'Cash', 1, 3),
(10, '2026-10-24 18:11:00', 'Completed', 17.50, 'Mobile Pay', 12, 4),
(11, '2026-10-24 16:02:00', 'Completed', 38.50, 'Card', 7, 10),
(12, '2026-10-24 17:49:00', 'Completed', 26.25, 'Card', 12, 4),
(13, '2026-10-24 20:26:00', 'Completed', 29.00, 'Cash', 10, 11),
(14, '2026-10-24 19:48:00', 'Completed', 19.50, 'Cash', 2, 5),
(15, '2026-11-07 14:00:00', 'Completed', 14, 'Mobile Pay', 12, 16),
(16, '2026-11-07 14:02:00', 'Completed', 15.00, 'Card', 13, 14),
(17, '2026-11-07 11:22:00', 'Completed', 11, 'Card', 11, 13),
(18, '2026-11-07 15:40:00', 'Completed', 14, 'Cash', 16, 16),
(19, '2026-11-07 15:45:00', 'Completed', 31.00, 'Card', 9, 14),
(20, '2026-11-07 12:51:00', 'Refunded', 16, 'Card', 7, 14),
(21, '2026-11-07 13:21:00', 'Cancelled', 24, 'Cash', 6, 14);

INSERT INTO OrderItem
(OrderID, MenuItemID, Quantity, UnitPriceAtSale)
VALUES
(5, 10, 1, 11),
(5, 11, 3, 5.50),
(6, 11, 2, 5.50),
(6, 10, 2, 11),
(7, 7, 1, 4.75),
(7, 1, 1, 4.50),
(8, 9, 1, 3.75),
(8, 5, 3, 5.00),
(9, 9, 1, 3.75),
(9, 5, 2, 5.00),
(10, 2, 1, 4.00),
(10, 1, 3, 4.50),
(11, 12, 2, 8),
(11, 13, 3, 7.50),
(12, 2, 3, 4.00),
(12, 7, 3, 4.75),
(13, 19, 2, 14.50),
(14, 4, 3, 6.50),
(15, 22, 1, 14),
(16, 13, 2, 7.50),
(17, 10, 1, 11),
(18, 22, 1, 14),
(19, 12, 2, 8),
(19, 13, 2, 7.50),
(20, 12, 2, 8),
(21, 12, 3, 8);



/*VERIFICATION*/

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


