/* Location Table */
CREATE TABLE Location (
	LocationID INT PRIMARY KEY, 
    LocationName VARCHAR(100), 
    StreetAddress VARCHAR(100), 
    City VARCHAR(50), 
    State VARCHAR(50), 
    Zipcode INT
); 

/* Vendor Table */
CREATE TABLE Vendor(
	VendorID INT PRIMARY KEY,
    CompanyName VARCHAR(100), 
    ContactName VARCHAR(100), 
    Email VARCHAR(100), 
    Phone VARCHAR(15), 
    TaxID VARCHAR(20)
);

/* Customer Table */
CREATE TABLE Customer(
	CustomerID INT PRIMARY KEY, 
    FirstName VARCHAR(50), 
    LastName VARCHAR(50), 
    Email VARCHAR(100), 
    Phone VARCHAR(15), 
    CreatedAt DATETIME
); 

/* Event Table */
CREATE TABLE Event(
	EventID INT PRIMARY KEY, 
    EventName VARCHAR(100), 
    StartDateTime DATETIME, 
    EndDateTime DATETIME, 
    LocationID INT, 
    FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
);

/* FoodTruck Table */
CREATE TABLE FoodTruck(
	TruckID INT PRIMARY KEY, 
    TruckName VARCHAR(100), 
    LicensePlate VARCHAR(20), 
    VendorID INT, 
    FOREIGN KEY (VendorID) REFERENCES Vendor(VendorID)
); 

/* EventRegistration Table */
CREATE TABLE EventRegistration(
	RegistrationID INT PRIMARY KEY, 
    BoothNumber VARCHAR(20), 
    RegistrationDate DATE, 
    EventID INT, 
    TruckID INT, 
    FOREIGN KEY (EventID) REFERENCES Event(EventID), 
    FOREIGN KEY (TruckID) REFERENCES FoodTruck(TruckID)
); 

/* MenuItem Table */
CREATE TABLE MenuItem(
	MenuItemID INT PRIMARY KEY, 
    ItemName VARCHAR(100), 
    Description TEXT, 
    Price DECIMAL(6,2), 
    DietaryFlags VARCHAR(50), 
    Availability VARCHAR(45), 
    TruckID INT, 
    FOREIGN KEY (TruckID) REFERENCES FoodTruck(TruckID)
);

/* CustomerOrder Table */
CREATE TABLE CustomerOrder(
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
CREATE TABLE OrderItem(
	OrderID INT, 
    MenuItem INT, 
    Quantity INT, 
    UnitPriceAtSale DECIMAL(6,2),
    PRIMARY KEY (OrderID, MenuItemID), 
    FOREIGN KEY (OrderID) REFERENCES CustomerOrder(OrderID), 
    FOREIGN KEY (MenuItemID) REFERENCES MenuItem(MenuItemID)
); 
