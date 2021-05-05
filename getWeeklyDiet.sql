DROP PROCEDURE IF EXISTS GetWeeklyDiet;
DELIMITER $$

CREATE PROCEDURE GetWeeklyDiet(
     IN p_id INT)
BEGIN
	SELECT date, SUM(amount * calories * 0.01)
    FROM dietrecord
    JOIN mealrel ON dietrecord.meal_id = mealrel.meal_id
    JOIN food ON mealrel.food_id = food.food_id
    WHERE dietrecord.pet_id = p_id
    GROUP BY date;
    
END $$

DELIMITER ;