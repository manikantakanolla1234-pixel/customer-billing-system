# Customer-Billing-System
Departmental Store Billing System

This is a project that I developed as part of the Database Management Systems (DBMS) course laboratory during my undergraduate studies.

The project is designed to automate the billing process of a departmental store. It allows users to register and log in, view available products, add products to a shopping cart, calculate the total bill with GST, complete payments, and generate invoices. The system also manages product stock automatically using database triggers and maintains data consistency through SQL transactions.

Backend (Database): MySQL

Backend (Application): Python Flask

Frontend (Web Technologies): HTML5 and CSS3

Database Connector: MySQL Connector/Python

Web Server: Flask Development Server



The project implements important DBMS concepts such as:

Database tables

Primary keys

Foreign keys

SQL queries

JOIN operations

INSERT, SELECT, UPDATE, and DELETE operations

Database transactions

COMMIT and ROLLBACK

Database triggers

Automatic inventory/stock management

User authentication

Billing and invoice generation



The project includes the following main modules:

User Registration and Login - 
Users can create an account and securely log in to the system.

Product Management - 
The system displays available products along with their prices and stock quantities.

Shopping Cart - 
Users can add multiple products to the cart, update quantities, and remove products.

Billing System - 
The system automatically calculates the subtotal, GST, and final payable amount.

Payment and Checkout - 
Customer details and payment methods are recorded during checkout.

Database Transactions - 
Customer information, order details, and purchased items are stored using SQL transactions. If an error occurs, the transaction is rolled back to maintain data consistency.

Database Trigger - 
A MySQL trigger automatically reduces the available product stock after a successful purchase.
Invoice Generation
A final bill is generated after successful payment, including customer details, purchased products, GST, payment method, and total amount.
