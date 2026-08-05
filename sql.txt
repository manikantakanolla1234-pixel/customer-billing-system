CREATE DATABASE departmental_store;
USE departmental_store;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'customer'
);

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    total_amount DECIMAL(10,2),
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (customer_id)REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2),
FOREIGN KEY (order_id)REFERENCES orders(order_id),
FOREIGN KEY (product_id)REFERENCES products(product_id)
);

CREATE TABLE cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id)REFERENCES users(user_id),
    FOREIGN KEY (product_id)REFERENCES products(product_id),
    UNIQUE(user_id, product_id)
);

INSERT INTO products(product_name, price, stock)VALUES
('Rice 1kg', 65.00, 100),
('Sugar 1kg', 45.00, 80),
('Milk', 30.00, 50),
('Soap', 40.00, 70),
('Cooking Oil 1L', 150.00, 40);

DELIMITER //
CREATE TRIGGER reduce_stock
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE products
    SET stock = stock - NEW.quantity
    WHERE product_id = NEW.product_id;
END //
DELIMITER ;

ALTER TABLE users ADD COLUMN full_name VARCHAR(100);
ALTER TABLE users MODIFY password VARCHAR(255) NOT NULL;
ALTER TABLE orders ADD COLUMN payment_method VARCHAR(30)DEFAULT 'Cash';


SELECT user_id,full_name,username, role FROM users;
SELECT * FROM customers;
SELECT * FROM products;
SELECT * FROM orders;
SELECT * FROM order_items;
SELECT product_id,product_name,stock FROM products;