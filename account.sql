DROP USER IF EXISTS 'ftf_app'@'localhost'; 

CREATE USER 'ftf_app'@'localhost' IDENTIFIED BY 'AppSecurePass2026!'; 

GRANT SELECT ON FoodTruckFestival.* TO 'ftf_app'@'localhost'; 
GRANT INSERT ON FoodTruckFestival.Customer TO 'ftf_app'@'localhost'; 
GRANT INSERT ON FoodTruckFestival.CustomerOrder TO 'ftf_app'@'localhost'; 
GRANT INSERT ON FoodTruckFestival.OrderItem TO 'ftf_app'@'localhost'; 
GRANT UPDATE ON FoodTruckFestival.Customer TO 'ftf_app'@'localhost'; 
GRANT UPDATE ON FoodTruckFestival.CustomerOrder TO 'ftf_app'@'localhost'; 

FLUSH PRIVILEGES; 