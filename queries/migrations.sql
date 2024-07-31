-- Create Customers table
CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(255)
);

-- Create Orders table
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

-- Insert data into Customers table
INSERT INTO Customers (customer_id, name, email, phone, address) VALUES
(1, 'Alice Smith', 'alice@example.com', '123-456-7890', '123 Maple St.'),
(2, 'Bob Johnson', 'bob@example.com', '234-567-8901', '456 Oak St.'),
(3, 'Charlie Brown', 'charlie@example.com', '345-678-9012', '789 Pine St.'),
(4, 'David Green', 'david@example.com', '456-789-0123', '1010 Birch St.'),
(5, 'Eva White', 'eva@example.com', '567-890-1234', '2020 Cedar St.');

-- Insert data into Orders table
INSERT INTO Orders (order_id, customer_id, order_date, total_amount) VALUES
(1, 1, '2024-06-20', 150.50),
(2, 2, '2024-06-21', 200.00),
(3, 3, '2024-06-22', 99.99),
(4, 1, '2024-06-23', 250.75),
(5, 4, '2024-06-24', 300.20),
(6, 5, '2024-06-25', 50.00),
(7, 3, '2024-06-26', 120.15),
(8, 2, '2024-06-27', 220.45),
(9, 5, '2024-06-28', 180.80),
(10, 4, '2024-06-29', 210.90),
(11, 1, '2024-06-30', 310.65),
(12, 3, '2024-07-01', 450.50),
(13, 2, '2024-07-02', 399.99),
(15, 4, '2024-07-04', 320.40),
(16, 2, '2024-07-02', 300.20);