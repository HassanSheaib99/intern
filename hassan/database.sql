CREATE DATABASE HR CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
use HR;
CREATE TABLE auth_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE,
    password VARCHAR(128),
    first_name VARCHAR(30),
    last_name VARCHAR(150),
    email VARCHAR(254),
    is_staff BOOLEAN,
    is_active BOOLEAN,
    date_joined DATETIME
);

CREATE TABLE employee_management_employee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    title VARCHAR(100),
    department VARCHAR(100),
    email VARCHAR(254),
    phone_number VARCHAR(15),
    vacation_days INT DEFAULT 15,
    position VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES auth_user(id)
);
CREATE TABLE employee_management_attendancerecord (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    check_in TIMESTAMP,
    check_out TIMESTAMP,
    date DATE,
    FOREIGN KEY (employee_id) REFERENCES employee_management_employee(id)
);
ALTER TABLE auth_user
ADD COLUMN last_login DATETIME;
ALTER TABLE auth_user
ADD COLUMN is_superuser DATETIME;

INSERT INTO auth_user (id,username, password, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES (1,'yami', 'yami123', 'hassan', 'sheaib', 'hassansheaib34@gmail.com', 0, 1, NOW());
INSERT INTO employee_management_employee (user_id, title, department, email, phone_number, position)
VALUES (1, 'Developer', 'Development', 'yami@gmail.com', '76518233', 'Intern');




SHOW TABLES LIKE 'auth_user';
SELECT * FROM django_migrations WHERE app='auth';
