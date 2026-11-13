DROP USER IF EXISTS 'ftf_app'@'localhost'; 

CREATE USER 'ftf_app'@'localhost' IDENTIFIED BY 'AppSecurePass2026!'; 

GRANT SELECT ON FoodTruckFestival.* TO 'ftf_app'@'localhost'; 
GRANT INSERT ON FoodTruckFestival.Customer TO 'ftf_app'@'localhost'; 
GRANT INSERT ON FoodTruckFestival.CustomerOrder TO 'ftf_app'@'localhost'; 
GRANT INSERT ON FoodTruckFestival.OrderItem TO 'ftf_app'@'localhost'; 
GRANT UPDATE ON FoodTruckFestival.Customer TO 'ftf_app'@'localhost'; 
GRANT UPDATE ON FoodTruckFestival.CustomerOrder TO 'ftf_app'@'localhost'; 

DROP USER IF EXISTS 'ftf_vendor'@'localhost'; 
CREATE USER 'ftf_vendor'@'localhost' IDENTIFIED BY 'VendorSecurePass2026!'; 

GRANT SEECT ON FoodTruckFestival.* TO 'ftf_vendor'@'localhost'; 
GRANT INSERT, UPDATE ON FoodTruckFestival.MenuItem TO 'ftf_vendor'@'localhost'; 
GRANT UPDATE ON FoodTruckFestival.FoodTruck TO 'ftf_vendor'@'localhost'; 

FLUSH PRIVILEGES; 
