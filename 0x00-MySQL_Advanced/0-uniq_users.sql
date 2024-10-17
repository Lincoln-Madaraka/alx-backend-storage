-- SQL script that creates a table users
CREATE TABLE IF NOT EXISTS users (id INT PRIMARY key AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
