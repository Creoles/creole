-- MySQL dump 10.13  Distrib 5.7.17, for Linux (x86_64)
--
-- Host: localhost    Database: creole
-- ------------------------------------------------------
-- Server version	5.7.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attraction`
--

DROP TABLE IF EXISTS `attraction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attraction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `country_id` int(11) NOT NULL,
  `city_id` int(11) NOT NULL,
  `address` varchar(80) NOT NULL,
  `name` varchar(30) NOT NULL,
  `name_en` varchar(30) NOT NULL,
  `adult_fee` float NOT NULL,
  `child_fee` float NOT NULL,
  `intro_cn` varchar(128) DEFAULT NULL,
  `intro_en` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `name_en` (`name_en`),
  KEY `ix_updated_at` (`updated_at`),
  KEY `ix_country_id` (`country_id`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_city_id` (`city_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(20) NOT NULL,
  `name_en` varchar(40) NOT NULL,
  `country_id` int(11) NOT NULL,
  `abbreviation` varchar(3) NOT NULL,
  `note` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `name_en` (`name_en`),
  UNIQUE KEY `idx_name_name_en` (`name`,`name_en`),
  KEY `ix_country_id` (`country_id`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_name` (`name`),
  KEY `ix_updated_at` (`updated_at`),
  KEY `ix_name_en` (`name_en`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(20) NOT NULL,
  `name_en` varchar(40) NOT NULL,
  `nationality` varchar(30) NOT NULL,
  `language` varchar(20) NOT NULL,
  `area_code` varchar(8) NOT NULL,
  `country_code` varchar(10) NOT NULL,
  `note` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `name_en` (`name_en`),
  UNIQUE KEY `idx_name_name_en` (`name`,`name_en`),
  KEY `ix_updated_at` (`updated_at`),
  KEY `ix_name_en` (`name_en`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `meal`
--

DROP TABLE IF EXISTS `meal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `restaurant_id` int(11) NOT NULL,
  `meal_type` tinyint(4) NOT NULL,
  `adult_fee` float NOT NULL,
  `adult_cost` float NOT NULL,
  `child_fee` float NOT NULL,
  `child_cost` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_updated_at` (`updated_at`),
  KEY `ix_restaurant_id` (`restaurant_id`),
  KEY `ix_created_at` (`created_at`),
  KEY `idx_restaurant_id_meal_type` (`restaurant_id`,`meal_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `restaurant`
--

DROP TABLE IF EXISTS `restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `restaurant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(30) NOT NULL,
  `name_en` varchar(30) NOT NULL,
  `nickname_en` varchar(20) NOT NULL,
  `restaurant_type` tinyint(4) NOT NULL,
  `country_id` int(11) NOT NULL,
  `city_id` int(11) NOT NULL,
  `address` varchar(100) NOT NULL,
  `intro_cn` varchar(128) DEFAULT NULL,
  `intro_en` varchar(128) DEFAULT NULL,
  `environ_level` tinyint(4) NOT NULL,
  `taste_level` tinyint(4) NOT NULL,
  `service_level` tinyint(4) NOT NULL,
  `cost_level` tinyint(4) NOT NULL,
  `cooperation_level` tinyint(4) NOT NULL,
  `recommend_level` tinyint(4) NOT NULL,
  `contact_one` varchar(20) NOT NULL,
  `position_one` varchar(20) NOT NULL,
  `telephone_one` varchar(20) NOT NULL,
  `email_one` varchar(30) NOT NULL,
  `contact_two` varchar(20) NOT NULL,
  `position_two` varchar(20) NOT NULL,
  `telephone_two` varchar(20) NOT NULL,
  `email_two` varchar(30) NOT NULL,
  `contact_three` varchar(20) DEFAULT NULL,
  `position_three` varchar(20) DEFAULT NULL,
  `telephone_three` varchar(20) DEFAULT NULL,
  `email_three` varchar(30) DEFAULT NULL,
  `standard_meal_intro_cn` varchar(500) DEFAULT NULL,
  `standard_meal_intro_en` varchar(800) DEFAULT NULL,
  `upgrade_meal_intro_cn` varchar(500) DEFAULT NULL,
  `upgrade_meal_intro_en` varchar(800) DEFAULT NULL,
  `luxury_meal_intro_cn` varchar(500) DEFAULT NULL,
  `luxury_meal_intro_en` varchar(800) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `name_en` (`name_en`),
  UNIQUE KEY `nickname_en` (`nickname_en`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_name_en` (`name_en`),
  KEY `ix_updated_at` (`updated_at`),
  KEY `ix_name` (`name`),
  KEY `ix_city_id` (`city_id`),
  KEY `ix_country_id` (`country_id`),
  KEY `ix_restaurant_type` (`restaurant_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `restaurant_account`
--

DROP TABLE IF EXISTS `restaurant_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `restaurant_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `currency` tinyint(4) NOT NULL,
  `bank_name` varchar(30) NOT NULL,
  `deposit_bank` varchar(30) NOT NULL,
  `payee` varchar(20) NOT NULL,
  `account` varchar(20) NOT NULL,
  `swift_code` varchar(20) DEFAULT NULL,
  `note` varchar(40) NOT NULL,
  `restaurant_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account` (`account`),
  KEY `ix_updated_at` (`updated_at`),
  KEY `ix_restaurant_id` (`restaurant_id`),
  KEY `ix_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `restaurant_company`
--

DROP TABLE IF EXISTS `restaurant_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `restaurant_company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(30) NOT NULL,
  `name_en` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `name_en` (`name_en`),
  UNIQUE KEY `idx_name_name_en` (`name`,`name_en`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_updated_at` (`updated_at`),
  KEY `ix_name_en` (`name_en`),
  KEY `ix_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shop`
--

DROP TABLE IF EXISTS `shop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(40) NOT NULL,
  `name_en` varchar(60) NOT NULL,
  `address` varchar(100) NOT NULL,
  `telephone` varchar(20) NOT NULL,
  `country_id` int(11) NOT NULL,
  `city_id` int(11) NOT NULL,
  `company_id` int(11) DEFAULT NULL,
  `shop_type` tinyint(4) NOT NULL,
  `contact` varchar(16) NOT NULL,
  `fee_person` float NOT NULL,
  `commission_ratio` float NOT NULL,
  `average_score` float DEFAULT NULL,
  `intro_cn` varchar(160) DEFAULT NULL,
  `intro_en` varchar(160) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_company_id` (`company_id`),
  KEY `idx_country_id_city_id_company_id_shop_type` (`country_id`,`city_id`,`company_id`,`shop_type`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_country_id` (`country_id`),
  KEY `ix_average_score` (`average_score`),
  KEY `ix_city_id` (`city_id`),
  KEY `ix_shop_type` (`shop_type`),
  KEY `ix_updated_at` (`updated_at`),
  KEY `idx_name_name_en` (`name`,`name_en`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shop_company`
--

DROP TABLE IF EXISTS `shop_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop_company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(40) NOT NULL,
  `name_en` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `name_en` (`name_en`),
  UNIQUE KEY `idx_name_name_en` (`name`,`name_en`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_updated_at` (`updated_at`),
  KEY `ix_name_en` (`name_en`),
  KEY `ix_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shop_image`
--

DROP TABLE IF EXISTS `shop_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `shop_id` int(11) NOT NULL,
  `image_hash` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tour_guide`
--

DROP TABLE IF EXISTS `tour_guide`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tour_guide` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `guide_type` tinyint(4) NOT NULL,
  `country_id` int(11) NOT NULL,
  `name` varchar(10) DEFAULT NULL,
  `name_en` varchar(20) NOT NULL,
  `nickname_en` varchar(10) DEFAULT NULL,
  `gender` tinyint(4) NOT NULL,
  `birthday` smallint(6) NOT NULL,
  `start_work` smallint(6) NOT NULL,
  `first_language` varchar(20) NOT NULL,
  `first_language_level` tinyint(4) NOT NULL,
  `second_language` varchar(20) NOT NULL,
  `second_language_level` tinyint(4) NOT NULL,
  `third_language` varchar(20) DEFAULT NULL,
  `third_language_level` tinyint(4) DEFAULT NULL,
  `certificate_type` tinyint(4) NOT NULL,
  `certificate_number` varchar(20) NOT NULL,
  `tour_guide_number` varchar(20) NOT NULL,
  `passport_country` varchar(30) NOT NULL,
  `passport_type` tinyint(4) NOT NULL,
  `passport_note` varchar(128) DEFAULT NULL,
  `telephone_one` varchar(20) NOT NULL,
  `telephone_two` varchar(20) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `company_id` int(11) NOT NULL,
  `intro` varchar(256) DEFAULT NULL,
  `image_hash` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_gender` (`gender`),
  KEY `ix_name_en` (`name_en`),
  KEY `ix_created_at` (`created_at`),
  KEY `idx_country_id_gender` (`country_id`,`gender`),
  KEY `idx_name_name_en` (`name`,`name_en`),
  KEY `ix_updated_at` (`updated_at`),
  KEY `ix_country_id` (`country_id`),
  KEY `ix_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tour_guide_account`
--

DROP TABLE IF EXISTS `tour_guide_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tour_guide_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `currency` tinyint(4) NOT NULL,
  `bank_name` varchar(30) NOT NULL,
  `deposit_bank` varchar(30) NOT NULL,
  `payee` varchar(20) NOT NULL,
  `account` varchar(20) NOT NULL,
  `swift_code` varchar(20) DEFAULT NULL,
  `note` varchar(40) NOT NULL,
  `tour_guide_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account` (`account`),
  KEY `ix_tour_guide_id` (`tour_guide_id`),
  KEY `ix_updated_at` (`updated_at`),
  KEY `ix_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tour_guide_fee`
--

DROP TABLE IF EXISTS `tour_guide_fee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tour_guide_fee` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `tour_guide_id` int(11) NOT NULL,
  `currency` tinyint(4) NOT NULL,
  `base_fee` float NOT NULL,
  `service_type` tinyint(4) NOT NULL,
  `service_fee` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tour_guide_id` (`tour_guide_id`),
  KEY `ix_tour_guide_id` (`tour_guide_id`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_name` varchar(40) NOT NULL,
  `password_hash` varchar(70) NOT NULL,
  `uuid` varchar(40) NOT NULL,
  `session_id` varchar(128) DEFAULT NULL,
  `session_create_time` datetime DEFAULT NULL,
  `role` tinyint(4) NOT NULL,
  `customer_name` varchar(40) DEFAULT NULL,
  `address` varchar(256) NOT NULL,
  `telephone` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_name` (`user_name`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_role` (`role`),
  KEY `ix_customer_name` (`customer_name`),
  KEY `ix_session_id` (`session_id`),
  KEY `ix_user_name` (`user_name`),
  KEY `ix_uuid` (`uuid`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vehicle`
--

DROP TABLE IF EXISTS `vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `country_id` int(11) NOT NULL,
  `city_id` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  `license` varchar(10) NOT NULL,
  `insurance_number` varchar(30) NOT NULL,
  `start_use` varchar(4) NOT NULL,
  `register_number` varchar(20) NOT NULL,
  `vehicle_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `license` (`license`),
  KEY `ix_updated_at` (`updated_at`),
  KEY `ix_created_at` (`created_at`),
  KEY `idx_country_id_city_id_company_id_vehicle_type_id` (`country_id`,`city_id`,`company_id`,`vehicle_type_id`),
  KEY `ix_country_id` (`country_id`),
  KEY `ix_city_id` (`city_id`),
  KEY `ix_company_id` (`company_id`),
  KEY `ix_vehicle_type_id` (`vehicle_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vehicle_company`
--

DROP TABLE IF EXISTS `vehicle_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicle_company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `company_type` tinyint(4) NOT NULL,
  `country_id` int(11) NOT NULL,
  `city_id` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `name_en` varchar(60) NOT NULL,
  `nickname_en` varchar(30) NOT NULL,
  `vehicle_number` smallint(6) NOT NULL,
  `register_number` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `name_en` (`name_en`),
  UNIQUE KEY `nickname_en` (`nickname_en`),
  UNIQUE KEY `idx_name_name_en` (`name`,`name_en`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_updated_at` (`updated_at`),
  KEY `ix_name_en` (`name_en`),
  KEY `ix_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vehicle_company_account`
--

DROP TABLE IF EXISTS `vehicle_company_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicle_company_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `currency` tinyint(4) NOT NULL,
  `bank_name` varchar(30) NOT NULL,
  `deposit_bank` varchar(30) NOT NULL,
  `payee` varchar(20) NOT NULL,
  `account` varchar(20) NOT NULL,
  `swift_code` varchar(20) DEFAULT NULL,
  `note` varchar(40) NOT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account` (`account`),
  KEY `ix_company_id` (`company_id`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vehicle_contact`
--

DROP TABLE IF EXISTS `vehicle_contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicle_contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `contact` varchar(16) NOT NULL,
  `position` varchar(30) NOT NULL,
  `telephone` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_company_id` (`company_id`),
  KEY `ix_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vehicle_fee`
--

DROP TABLE IF EXISTS `vehicle_fee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicle_fee` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `vehicle_type_id` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  `unit_price` float NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `confirm_person` varchar(30) DEFAULT NULL,
  `attachment_hash` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vehicle_image`
--

DROP TABLE IF EXISTS `vehicle_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicle_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `vehicle_id` int(11) NOT NULL,
  `image_hash` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vehicle_type`
--

DROP TABLE IF EXISTS `vehicle_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicle_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `vehicle_type` tinyint(4) NOT NULL,
  `brand` varchar(20) NOT NULL,
  `seat` tinyint(4) NOT NULL,
  `available_seat` tinyint(4) NOT NULL,
  `passenger_count` tinyint(4) NOT NULL,
  `note` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_created_at` (`created_at`),
  KEY `ix_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vehicle_user_account`
--

DROP TABLE IF EXISTS `vehicle_user_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicle_user_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `currency` tinyint(4) NOT NULL,
  `bank_name` varchar(30) NOT NULL,
  `deposit_bank` varchar(30) NOT NULL,
  `payee` varchar(20) NOT NULL,
  `account` varchar(20) NOT NULL,
  `note` varchar(40) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account` (`account`),
  KEY `idx_user_id_account` (`user_id`,`account`),
  KEY `ix_updated_at` (`updated_at`),
  KEY `ix_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-05-14  9:27:00
