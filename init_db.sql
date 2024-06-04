-- CREATE DATABASE IF NOT EXISTS creditcard;
-- CREATE USER 'admin'@'%' IDENTIFIED BY '123456';
-- GRANT ALL PRIVILEGES ON creditcard.* TO 'admin'@'%';
-- FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS creditcard;

-- Check if the user 'admin' exists and only create it if it does not exist
SET @user_exists = (SELECT COUNT(*) FROM mysql.user WHERE user = 'admin' AND host = '%');
SET @create_user_stmt = IF(@user_exists = 0, 'CREATE USER \'admin\'@\'%\' IDENTIFIED BY \'123456\'', 'SELECT "User already exists"');
PREPARE stmt FROM @create_user_stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

GRANT ALL PRIVILEGES ON creditcard.* TO 'admin'@'%';
FLUSH PRIVILEGES;