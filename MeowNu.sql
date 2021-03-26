SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS pet;
DROP TABLE IF EXISTS dietRecord;
DROP TABLE IF EXISTS meal;
DROP TABLE IF EXISTS food;
DROP TABLE IF EXISTS suggestion;
DROP TABLE IF EXISTS nutrients;
DROP TABLE IF EXISTS mealrel;
SET FOREIGN_KEY_CHECKS = 1;

--
-- Table structure for table `user` : user_id, email, password, username, age, gender, city
-- 

CREATE TABLE IF NOT EXISTS `user` (
	`user_id` int(11) NOT NULL,
	`email` varchar(50) NOT NULL,
    `password` varchar(50) NOT NULL,
    `username` varchar(50) NOT NULL,
    `age` int(11),
    `gender` varchar(50),
    `city` varchar(50),
    PRIMARY KEY (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `pet` : pet_id, user_id, name, species, age, gender, weight, status
-- 

CREATE TABLE IF NOT EXISTS `pet` (
	`pet_id` int(11) NOT NULL,
    `user_id` int(11) NOT NULL,
    `name` varchar(50) NOT NULL,
    `species` varchar(50) NOT NULL,
    `age` int(11) NOT NULL,
    `gender` varchar(50) NOT NULL,
    `weight` FLOAT(10) NOT NULL,
    `status` varchar(50) NOT NULL,
    PRIMARY KEY (pet_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `meal` : meal_id, type
-- 

CREATE TABLE IF NOT EXISTS `meal` (
	`meal_id` int(11) NOT NULL,
    `type` varchar(50) NOT NULL,
    PRIMARY KEY (meal_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `dietRecord` : pet_id, meal_id, date
-- 

CREATE TABLE IF NOT EXISTS `dietRecord` (
	`pet_id` int(11) NOT NULL,
    `meal_id` int(11) NOT NULL,
    `date` timestamp DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pet_id) REFERENCES pet(pet_id) ON DELETE CASCADE,
    FOREIGN KEY (meal_id) REFERENCES meal(meal_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `food` : food_id, name, calories, moisture, protein, lipid, 
-- 										Ca, P, Fe, Zn, Cu, Mn, I, VB1, Choline, VA, VE, VD
-- 

CREATE TABLE IF NOT EXISTS `food` (
	`food_id` int(11) NOT NULL,
    `name` varchar(50) NOT NULL,
	`calories` FLOAT(10) NOT NULL,
    `moisture` FLOAT(10) NOT NULL,
    `protein` FLOAT(10) NOT NULL,
    `lipid` FLOAT(10) NOT NULL,
    `Ca` FLOAT(10) NOT NULL,
    `P` FLOAT(10) NOT NULL,
    `Fe` FLOAT(10) NOT NULL,
    `Zn` FLOAT(10) NOT NULL,
    `Cu` FLOAT(10) NOT NULL,
    `Mn` FLOAT(10) NOT NULL,
    `I` FLOAT(10) NOT NULL,
    `VB1` FLOAT(10) NOT NULL,
    `Choline` FLOAT(10) NOT NULL,
    `VA` FLOAT(10) NOT NULL,
    `VE` FLOAT(10) NOT NULL,
    `VD` FLOAT(10) NOT NULL,
    PRIMARY KEY (food_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `meal` : meal_id, food_id, type, amount
-- 

CREATE TABLE IF NOT EXISTS `mealrel` (
	`meal_id` int(11) NOT NULL,
    `food_id` int(11) NOT NULL,
	`amount` FLOAT(10) NOT NULL,
    FOREIGN KEY (meal_id) REFERENCES meal(meal_id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES food(food_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `advice` : advice_id, species, age, gender, status, required_caloreis, required_meat
-- 

CREATE TABLE IF NOT EXISTS `suggestion` (
    `suggestion_id` int(11) NOT NULL,
    `pet_id` int(11) NOT NULL,
    `date` timestamp DEFAULT CURRENT_TIMESTAMP,
    `suggestion` varchar(50) NOT NULL,
	PRIMARY KEY (suggestion_id),
    FOREIGN KEY (pet_id) REFERENCES pet(pet_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `advice` : advice_id, species, age, gender, status, required_caloreis, required_meat
-- 

CREATE TABLE IF NOT EXISTS `nutrients` (
    `nutrients_id` int(11) NOT NULL,
    `pet_id` int(11) NOT NULL,
    `calories` FLOAT(10) NOT NULL,
	PRIMARY KEY (nutrients_id),
    FOREIGN KEY (pet_id) REFERENCES pet(pet_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `food`: food_id, name, calories, moisture, protein, lipid, 
-- 										Ca, P, Fe, Zn, Cu, Mn, I, VB1, Choline, VA, VE, VD
--

INSERT INTO `food` (`food_id`, `name`, `calories`, `moisture`, `protein`, `lipid`, `Ca`, `P`, `Fe`, `Zn`, 
					`Cu`, `Mn`, `I`, `VB1`, `Choline`, `VA`, `VE`, `VD`) VALUES
(1, 'chiken liver', 119, 76.46, 16.92, 4.83, 8, 297, 8.99, 2.67, 0.492, 0.255, 0, 0.305, 194.4, 11078, 0.7, 0);
