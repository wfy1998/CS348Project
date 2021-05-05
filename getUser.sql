DROP PROCEDURE IF EXISTS getUserInfo1;
DELIMITER $$

CREATE PROCEDURE getUserInfo1(
	IN emailAdd VARCHAR(50)
)
BEGIN
	select username, email, gender, age, city
	from user 
	where email = emailAdd;

END$$

DELIMITER ;