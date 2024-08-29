-- Create the database
CREATE DATABASE chatbot_db;

-- Use the chatbot_db database
USE chatbot_db;

-- Create the Business Information table
CREATE TABLE businesses (
    business_id INT AUTO_INCREMENT PRIMARY KEY,
    business_name VARCHAR(255) NOT NULL,
    business_type VARCHAR(100),
    business_description TEXT
);

-- Create the FAQs and Responses table
CREATE TABLE faqs (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    business_id INT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    FOREIGN KEY (business_id) REFERENCES businesses(business_id)
);

-- Create the Customer Interactions table
CREATE TABLE interactions (
    interaction_id INT AUTO_INCREMENT PRIMARY KEY,
    business_id INT,
    customer_query TEXT NOT NULL,
    response TEXT,
    FOREIGN KEY (business_id) REFERENCES businesses(business_id)
);

-- Create the Learning Data table
CREATE TABLE learning_data (
    learning_id INT AUTO_INCREMENT PRIMARY KEY,
    interaction_id INT,
    correct_response TEXT NOT NULL,
    FOREIGN KEY (interaction_id) REFERENCES interactions(interaction_id)
);
