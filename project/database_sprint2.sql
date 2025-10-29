CREATE USER 'Elly_aou'@'172.56.209.166' IDENTIFIED BY 'aou_cit260';
GRANT ALL PRIVILEGES ON er_system.* TO 'Elly_aou'@'172.56.209.166';
FLUSH PRIVILEGES;

CREATE USER 'Zech_aou'@'192.168.0.159' IDENTIFIED BY 'aou_cit260';
GRANT ALL PRIVILEGES ON er_system.* TO 'Zech_aou'@'192.168.0.159';
FLUSH PRIVILEGES;


USE er_system;

ALTER TABLE Users
MODIFY nshe_id VARCHAR(10) NULL;

ALTER TABLE Users
ADD COLUMN employee_id VARCHAR(15) NULL AFTER nshe_id;

SELECT * 
FROM users;

UPDATE Users 
SET email = CONCAT(nshe_id, '@student.csn.edu')
WHERE role_id = 2 AND email NOT LIKE '%@student.csn.edu';

SELECT * 
FROM courses;

INSERT INTO Majors (name, department_id)
VALUES ('Undeclared', 1);

SELECT * FROM Majors;

UPDATE Users
SET email = CONCAT(nshe_id, '@student.csn.edu')
WHERE role_id = 2 AND email NOT REGEXP '^[0-9]{10}@student\\.csn\\.edu$';

SHOW INDEX FROM users;

ALTER TABLE Users MODIFY major_id INT NULL;

DESCRIBE Users;
ALTER TABLE Users MODIFY department_id INT NULL;


