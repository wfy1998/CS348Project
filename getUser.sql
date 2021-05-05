DROP PROCEDURE IF EXISTS getUser;
DELIMITER $$

CREATE PROCEDURE getUser(
	IN userId INT
)
BEGIN
	select name, gender, age, city, email
	from user 
	where user_id=userId;
END$$

DELIMITER ;