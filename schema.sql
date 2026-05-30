-- Student Management System Database Schema
-- Run this script to create the required tables.

CREATE DATABASE IF NOT EXISTS student_details;
USE student_details;

-- Student table
CREATE TABLE IF NOT EXISTS student (
    roll_no INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100) NOT NULL,
    mother_name VARCHAR(100) NOT NULL,
    address TEXT,
    phone_no VARCHAR(15) NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Exam table with foreign key to student
CREATE TABLE IF NOT EXISTS exam (
    id INT PRIMARY KEY AUTO_INCREMENT,
    roll_no INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    class INT NOT NULL,
    section VARCHAR(10) NOT NULL,
    total_marks INT NOT NULL,
    percentage DECIMAL(5,2) NOT NULL,
    grade VARCHAR(5) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (roll_no) REFERENCES student(roll_no) ON DELETE CASCADE
);
