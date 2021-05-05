DROP PROCEDURE IF EXISTS getView;
DELIMITER $$

CREATE PROCEDURE getView(
	IN mealid INT
)
BEGIN
	select name, amount, calories, moisture, protein, lipid 
	from mealrel join food on mealrel.food_id = food.food_id 
	where meal_id=mealid;
END$$

DELIMITER ;
