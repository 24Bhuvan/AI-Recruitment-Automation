-- Create database
CREATE DATABASE IF NOT EXISTS airesumescreening;
USE airesumescreening;

-- Candidates table
CREATE TABLE IF NOT EXISTS candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    dob DATE,
    gender VARCHAR(20),
    objective TEXT,
    phone VARCHAR(20),
    email VARCHAR(255) UNIQUE,
    github VARCHAR(255)
);

-- Education table
CREATE TABLE IF NOT EXISTS education (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    degree VARCHAR(255),
    institution VARCHAR(255),
    year INT,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

-- Internships & Training table
CREATE TABLE IF NOT EXISTS internships_training (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    title VARCHAR(255),
    organization VARCHAR(255),
    duration VARCHAR(100),
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    title VARCHAR(255),
    description TEXT,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

-- Skills table
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    skill_name VARCHAR(255),
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

-- Achievements & Certifications table
CREATE TABLE IF NOT EXISTS achievements_certifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    title VARCHAR(255),
    year INT,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

-- Workshops & Events table
CREATE TABLE IF NOT EXISTS workshops_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    title VARCHAR(255),
    date DATE,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);

-- Interests & Hobbies table
CREATE TABLE IF NOT EXISTS interests_hobbies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    interest_name VARCHAR(255),
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);
