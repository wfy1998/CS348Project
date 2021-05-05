-- Scehma of MeowNu
-- important:
-- !!!!All priamry keys are auto increment. No need to include 'id' when insert!!!
--
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
	`user_id` int(11) NOT NULL AUTO_INCREMENT,
	`email` varchar(50) NOT NULL,
    `password` varchar(200) NOT NULL,
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
	`pet_id` int(11) NOT NULL AUTO_INCREMENT,
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
	`meal_id` int(11) NOT NULL AUTO_INCREMENT,
    `type` varchar(50) NOT NULL,
    PRIMARY KEY (meal_id)
) AUTO_INCREMENT = 1 ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `dietRecord` : pet_id, meal_id, date
-- 

CREATE TABLE IF NOT EXISTS `dietRecord` (
	`pet_id` int(11) NOT NULL,
    `meal_id` int(11) NOT NULL,
    `date` varchar(50) NOT NULL,
    FOREIGN KEY (pet_id) REFERENCES pet(pet_id) ON DELETE CASCADE,
    FOREIGN KEY (meal_id) REFERENCES meal(meal_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `food` : food_id, name, calories, moisture, protein, lipid, 
-- 										Ca, P, Fe, Zn, Cu, Mn, I, VB1, Choline, VA, VE, VD
-- 

CREATE TABLE IF NOT EXISTS `food` (
	`food_id` int(11) NOT NULL AUTO_INCREMENT,
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
-- Table structure for table `mealrel` : meal_id, food_id, type, amount
-- 

CREATE TABLE IF NOT EXISTS `mealrel` (
	`meal_id` int(11) NOT NULL,
    `food_id` int(11) NOT NULL,
	`amount` FLOAT(10) NOT NULL,
    FOREIGN KEY (meal_id) REFERENCES meal(meal_id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES food(food_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `suggestion` : suggestion_id, pet_id, date, suggestion
-- 

CREATE TABLE IF NOT EXISTS `suggestion` (
    `suggestion_id` int(11) NOT NULL AUTO_INCREMENT,
    `pet_id` int(11) NOT NULL,
    `date` timestamp DEFAULT CURRENT_TIMESTAMP,
    `suggestion` varchar(50) NOT NULL,
	PRIMARY KEY (suggestion_id),
    FOREIGN KEY (pet_id) REFERENCES pet(pet_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `nutrients` : nutrients_id, pet_id, calories
-- 

CREATE TABLE IF NOT EXISTS `nutrients` (
    `nutrients_id` int(11) NOT NULL AUTO_INCREMENT,
    `pet_id` int(11) NOT NULL,
    `calories` FLOAT(10) NOT NULL,
	PRIMARY KEY (nutrients_id),
    FOREIGN KEY (pet_id) REFERENCES pet(pet_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `food`: food_id, name, calories, moisture, protein, lipid, 
-- 										Ca, P, Fe, Zn, Cu, Mn, I, VB1, Choline, VA, VE, VD
--

INSERT INTO `food` (`name`, `calories`, `moisture`, `protein`, `lipid`, `Ca`, `P`, `Fe`, `Zn`, 
					`Cu`, `Mn`, `I`, `VB1`, `Choline`, `VA`, `VE`, `VD`) VALUES
('chicken liver', 119, 76.46, 16.92, 4.83, 8, 297, 8.99, 2.67, 0.492, 0.255, 0, 0.305, 194.4, 11078, 0.7, 0),
('duck liver', 126, 71.78, 18.74, 4.64, 11, 269, 30.53, 3.07, 5.962	, 0.258, 0, 0.562, 0, 39907, 0, 0),
('foie gras', 133, 71.78, 16.37, 4.28, 43, 261, 30.53, 3.07, 7.522, 0, 0, 0.562, 0, 30998, 0, 0),
('turkey liver', 128, 75.54, 18.26, 5.5, 20, 279, 8.94, 3.07, 0.863, 0.296, 0, 0.206, 221.8, 26901, 0.24, 50),
('beef liver', 135, 70.81, 20.36, 3.63, 5, 387, 4.9, 4, 9.755, 0.31, 0, 0.189, 333.3, 16898, 0.38, 49),
('pork liver', 134, 71.06, 21.39, 3.65, 9, 288, 23.3, 5.76, 0.667, 0.344, 0, 0.283, 0, 21650, 0, 0),
('egg', 143, 76.15, 12.56, 9.51, 56, 198, 1.75, 1.29, 0.072, 0.028, 0, 0.04, 293.8, 540, 1.05, 82),
('duck eggs', 185, 70.83, 12.81, 13.77, 64, 220, 3.85, 1.41, 0.062, 0.038, 0, 0.156, 263.4, 674, 1.34, 69),
('chicken breast', 120, 73.9, 22.5, 2.62, 5, 213, 0.37, 0.68, 0.037, 0.011, 0, 0.094, 82.1, 30, 0.56,1),
('chicken wings', 191, 69.19, 17.52, 12.85, 11, 123,0.46,1.21,0.034,0.011,0,0.054,82,29,0.64,5),
('duck breast', 123,75.51, 19.85, 4.25, 3,187, 4.51, 0.74, 0.33, 0.019, 0, 0.416, 0, 53, 0, 0),
('duck', 135, 73.77, 18.28, 5.95, 11, 203, 2.4, 1.9, 0.253, 0.019, 0, 0.36, 53.6, 79, 0.7, 3),
('pigeons', 294, 56.6, 18.47, 23.8, 12, 248, 3.54, 2.2, 0.437, 0.019, 0, 0.212, 0, 243, 0, 0),
('little steak', 162, 71.15, 18.86, 9.01, 13, 184, 0.86, 3.24, 0.102, 0.027, 0, 0.07, 0, 0, 0.21, 0),
('the calf tendon', 107, 75.85, 19.28, 3.3, 12, 207, 1.17, 3.32, 0.1, 0.01, 0, 0.082, 96.7, 0, 0.17, 31),
('cow ridge', 149, 71.5, 21.67, 6.93, 14, 211, 2.48, 3.2, 0.062, 0.007, 0, 0.053, 56, 15, 0.19, 2),
('pig ridge', 120, 74.97, 20.65, 3.53, 6, 243, 0.97, 1.87, 0.089, 0.014, 0, 0.982, 79.7, 2, 0.22, 10),
('Pig plum', 186, 69.18, 17.42, 12.36, 16, 190, 1.12, 3.09, 0.096, 0.011, 0, 0.52, 73.3, 8, 0.22, 30),
('Sika deer', 147, 71.4, 22.6, 5.2, 4, 210, 3.4, 2.8, 0.14, 0.01 ,0, 0.21, 0, 17, 0.6, 0),
('Blue mussel', 86, 80.58, 11.9, 2.24, 26, 197, 3.95, 1.6, 0.094, 3.4, 0, 0.16, 65, 160, 0.55, 0),
('Mussels', 74, 81.3, 10.7, 1.8, 66, 147, 3.3, 1.13, 0.09, 0.157, 105, 0, 0, 243, 0.97, 44),
('Saury', 297 , 57.7, 17.6, 23.6, 26, 170, 1.3, 0.8, 0.12, 0.02, 21, 0.01, 0, 37 ,1, 520),
('salmon', 208, 64.89, 20.42, 13.42, 9, 240, 0.34, 0.36, 0.045, 0.011, 0, 0.207, 78.5, 193, 3.55, 441);
