-- Active: 1701103046373@@127.0.0.1@3306@epicevents

CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) NOT NULL UNIQUE,
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
  FOREIGN KEY (`sales_contact`) REFERENCES `user`(`id`) ON DELETE CASCADE
);


CREATE TABLE `contract` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sales_contact_id` int DEFAULT NULL,
  `client_id` int DEFAULT NULL,
  `creation_date` datetime NOT NULL,
  `update_date` datetime NOT NULL,
  `status_contract` tinyint(1) NOT NULL DEFAULT '0',
  `total_amount` double NOT NULL DEFAULT '0',
  `remaining_amount` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `sales_contact_id` (`sales_contact_id`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `contract_ibfk_1` FOREIGN KEY (`sales_contact_id`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `contract_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`) ON DELETE SET NULL
);
