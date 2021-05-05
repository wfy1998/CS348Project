DROP PROCEDURE IF EXISTS statis;
DELIMITER $$

CREATE PROCEDURE statis(
	IN pet_id INT
)
BEGIN
	select name, amount*calories/100 as total
    from(select food_id, SUM(amount) as amount from dietRecord join mealrel on dietRecord.meal_id = mealrel.meal_id
		where pet_id=1 group by food_id) as a join food on a.food_id=food.food_id
	order by total desc;
END$$

DELIMITER ;