DROP PROCEDURE IF EXISTS statis;
DELIMITER $$

CREATE PROCEDURE statis(
	IN petid INT
)
BEGIN
	select name, amount, amount*calories/100 as total
    from(select food_id, SUM(amount) as amount from dietRecord join mealrel on dietRecord.meal_id = mealrel.meal_id
		where pet_id= petid group by food_id) as a join food on a.food_id=food.food_id
	order by total desc;
END$$

DELIMITER ;