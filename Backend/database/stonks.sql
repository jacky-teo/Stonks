DROP DATABASE IF EXISTS `stonks`;
CREATE DATABASE IF NOT EXISTS `stonks` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `stonks`;


-- User Account Table -- 
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
   `user_acc_id` varchar(50) NOT NULL,
   `user_pin` int NOT NULL,
   `settlement_acc` int NOT NULL,
   PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `users`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

INSERT INTO `users` (`user_id`, `username`, `password`,`user_acc_id`,`user_pin`,`settlement_acc`) VALUES
(1, 'admin', 'admin','Z312312','148986','0000009301'),
(2, 'user2', 'user2','B930284','828676','0000009302');
-- Funds ownd by custoemr -- 
DROP TABLE IF EXISTS `funds`;
CREATE TABLE IF NOT EXISTS `fund` (
  `fund_id` int(11) NOT NULL AUTO_INCREMENT,
  `fund_name` varchar(50) NOT NULL,
  `fund_investment_amount` float Not Null, 
  `fund_creation_date`	timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`fund_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `funds` (`fund_id`, `fund_name`, `fund_investment_amount`,`fund_creation_date`) VALUES
(1, 'My First Fund', 3589,'2020-10-27 00:00:00'),
(2, 'My Second Fund', 3589,'2020-10-27 00:00:00');


-- Stocks available for trade with Stonks -- 
DROP TABLE IF EXISTS `stocks`;
CREATE TABLE IF NOT EXISTS `stocks` (
  `stock_id` int not null auto_increment,
  `stock_symbol` varchar (10) not null,
  `stock_name` varchar(50) NOT NULL,
  PRIMARY KEY (`stock_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `stocks` (`stock_id`,`stock_name`, `stock_symbol`) VALUES
(1,'YZJ Shipbldg SGD', 'BS6.SI'),
(2,'Singtel', 'Z74.SI'),
(3,'DBS', 'D05.SI'),
(4,'Comfortdelgro Corporation Ltd','C52.SI'),
(5,'Jardine Cycle & Carriage Ltd','C07.SI'),
(6,'StarHub Ltd','CC3.SI'),
(7,'Singapore Exchange Limited','S68.SI'),
(8,'Olam Group Limited','VC2.SI'),
(9,'Panacea Acquisition Corp. II','PANA.SI'),
(10,'Alphabet Inc.','GOOG');


--  Fund has what stock -- 

DROP TABLE IF EXISTS `funds_stocks`;
CREATE TABLE IF NOT EXISTS `funds_stocks` (
  `fund_id` int NOT NULL,
  `stock_id` int NOT NULL,
  `allocation`float Not Null,
  PRIMARY KEY (`fund_id`,`stock_id`),
  FOREIGN KEY (`fund_id`) REFERENCES funds(`fund_id`),
  FOREIGN KEY (`stock_id`) REFERENCES stocks(`stock_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `funds_stocks` (`fund_id`, `stock_id`,`allocation`) VALUES
(1, 1,0.4),
(1, 2,0.3),
(1, 3,0.3);

-- Who owns which fund --
DROP TABLE IF EXISTS `users_funds`;
CREATE TABLE IF NOT EXISTS `users_funds` (
  `user_id` int NOT NULL,
  `fund_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`fund_id`),
  FOREIGN KEY (`user_id`) REFERENCES users(`user_id`),
  FOREIGN KEY (`fund_id`) REFERENCES funds(`fund_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `users_funds` (`user_id`, `fund_id`) VALUES
(1, 1),
(1, 2);

-- Stocks available in the marketplace this will act as the CDP -- 
DROP TABLE IF EXISTS `marketplace`;
CREATE TABLE IF NOT EXISTS `marketplace`(
    `marketplace_id` int not Null,
    `marketplace_name` varchar(50) NOT NULL,
     PRIMARY KEY (`marketplace_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

    
INSERT INTO `marketplace` (`marketplace_id`, `marketplace_name`) VALUES
(1,'Stonk Stock Exchange');


-- Marketplace and number of stocks available for that marketplace --
DROP TABLE IF EXISTS `marketplace_stocks`;
CREATE TABLE IF NOT EXISTS `marketplace_stocks`(
	`marketplace_id` int not Null,
    `stock_id` int NOT NULL,
	`volume_in_market` int Not Null,
    PRIMARY KEY (`marketplace_id`,`stock_id`),
    FOREIGN KEY (`marketplace_id`) REFERENCES marketplace(`marketplace_id`),
	FOREIGN KEY (`stock_id`) REFERENCES stocks(`stock_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `marketplace_stocks` (`marketplace_id`, `stock_id`,`volume_in_market`) VALUES
(1,1,1000000),
(1,2,1000000),
(1,3,1000000);


-- This will be an insert only table -- 
-- Store all transaction data --
DROP TABLE IF EXISTS `transactions`;
CREATE TABLE IF NOT EXISTS `transactions`(
    `transaction_id` int not Null,
	`user_id` int NOT NULL,
    `marketplace_id` int NOT NULL,
    `stock_id` int NOT NULL,
    `stock_price` float not Null,
    `volume` int not Null,
    `date` datetime not null,
	PRIMARY KEY (`transaction_id`),
    FOREIGN KEY (`user_id`) REFERENCES users(`user_id`),
	FOREIGN KEY (`stock_id`) REFERENCES stocks(`stock_id`),
    FOREIGN KEY (`marketplace_id`) REFERENCES marketplace(`marketplace_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- all transactions with marketplace will be reflected here -- 
INSERT INTO `transactions` (`transaction_id`, `user_id`,`marketplace_id`, `stock_id`,`stock_price`,`volume`,`date`) VALUES
(1,1, 1,1, 0.5, 1000, '2020-01-01 00:00:00'),
(2,1, 1,2, 3.5, -1000, '2020-01-01 00:00:00'),
(3,1, 1,3, 22.5, 1000, '2020-01-01 00:00:00'),
(4,2, 1,3, 22.5, 1000, '2020-01-01 00:00:00');