
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL UNIQUE,
  `password` varchar(128) NOT NULL,
  `email` varchar(255) NOT NULL UNIQUE,
  `department` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
);


CREATE TABLE `client` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL UNIQUE,
  `phone_number` varchar(20) NOT NULL,
  `company_name` varchar(255) NOT NULL,
  `creation_date` date NOT NULL,
  `last_contact` date DEFAULT NULL,
  `sales_contact` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`sales_contact`) REFERENCES `user`(`id`)
);
