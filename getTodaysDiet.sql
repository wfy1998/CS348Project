DROP PROCEDURE IF EXISTS GetTodaysDiet;
DELIMITER $$

CREATE PROCEDURE GetTodaysDiet(
	 IN t_date VARCHAR(50), 
     IN p_id INT)
BEGIN
	SELECT meal.type, food.name, amount, amount * calories * 0.01
    FROM dietrecord
    JOIN meal ON dietrecord.meal_id = meal.meal_id
    JOIN mealrel ON dietrecord.meal_id = mealrel.meal_id
    JOIN food ON mealrel.food_id = food.food_id
    WHERE dietrecord.date = t_date AND dietrecord.pet_id = p_id;
    
END $$

DELIMITER ;
	