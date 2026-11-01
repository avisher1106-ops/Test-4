-- MySQL dump 10.13  Distrib 8.4.9, for Linux (x86_64)
--
-- Host: localhost    Database: logs_db
-- ------------------------------------------------------
-- Server version	8.4.9

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `logs_db`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `logs_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `logs_db`;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `method` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `route` varchar(512) COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_results` int unsigned NOT NULL DEFAULT '0',
  `client_ip` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_logs_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
INSERT INTO `logs` VALUES (1,'GET','/fruits',49,'127.0.0.1','2026-11-01 17:32:05'),(2,'GET','/fruits/search?q=apple',3,'127.0.0.1','2026-11-01 17:32:06'),(3,'GET','/fruits/calories/50',26,'127.0.0.1','2026-11-01 17:32:06'),(4,'GET','/fruits',49,'127.0.0.1','2026-11-01 17:33:26'),(5,'GET','/fruits/search?q=weter',0,'127.0.0.1','2026-11-01 17:33:53'),(6,'GET','/fruits',49,'127.0.0.1','2026-11-01 17:33:59'),(7,'GET','/fruits/search?q=Banana',1,'127.0.0.1','2026-11-01 17:34:10'),(8,'GET','/fruits/calories/56',28,'127.0.0.1','2026-11-01 17:34:22'),(9,'GET','/fruits',49,'127.0.0.1','2026-11-01 17:34:28'),(10,'GET','/docs',0,'127.0.0.1','2026-11-01 17:36:51'),(11,'GET','/openapi.json',0,'127.0.0.1','2026-11-01 17:36:51'),(12,'GET','/docs/',0,'127.0.0.1','2026-11-01 17:37:13'),(13,'GET','/docs/swagger-ui.css',0,'127.0.0.1','2026-11-01 17:37:13'),(14,'GET','/docs',0,'127.0.0.1','2026-11-01 17:38:14'),(15,'GET','/docs/',0,'127.0.0.1','2026-11-01 17:38:14'),(16,'GET','/docs/index.css',0,'127.0.0.1','2026-11-01 17:38:14'),(17,'GET','/docs/swagger-ui-standalone-preset.js',0,'127.0.0.1','2026-11-01 17:38:15'),(18,'GET','/docs/swagger-ui-bundle.js',0,'127.0.0.1','2026-11-01 17:38:15'),(19,'GET','/docs/swagger-ui.css',0,'127.0.0.1','2026-11-01 17:38:15'),(20,'GET','/openapi.json',0,'127.0.0.1','2026-11-01 17:38:15'),(21,'GET','/docs/favicon-16x16.png',0,'127.0.0.1','2026-11-01 17:38:16'),(22,'GET','/docs/',0,'127.0.0.1','2026-11-01 17:39:16'),(23,'GET','/docs/index.css',0,'127.0.0.1','2026-11-01 17:39:16'),(24,'GET','/docs/swagger-ui.css',0,'127.0.0.1','2026-11-01 17:39:16'),(25,'GET','/docs/swagger-ui-bundle.js',0,'127.0.0.1','2026-11-01 17:39:16'),(26,'GET','/docs/swagger-ui-standalone-preset.js',0,'127.0.0.1','2026-11-01 17:39:16'),(27,'GET','/openapi.json',0,'127.0.0.1','2026-11-01 17:39:16'),(28,'GET','/docs/',0,'127.0.0.1','2026-11-01 17:39:21'),(29,'GET','/docs/index.css',0,'127.0.0.1','2026-11-01 17:39:22'),(30,'GET','/docs/swagger-ui-standalone-preset.js',0,'127.0.0.1','2026-11-01 17:39:22'),(31,'GET','/docs/swagger-ui-bundle.js',0,'127.0.0.1','2026-11-01 17:39:22'),(32,'GET','/docs/swagger-ui.css',0,'127.0.0.1','2026-11-01 17:39:22'),(33,'GET','/openapi.json',0,'127.0.0.1','2026-11-01 17:39:22'),(34,'GET','/fruits',49,'127.0.0.1','2026-11-01 17:48:56'),(35,'GET','/fruits/search?q=apple',3,'127.0.0.1','2026-11-01 17:48:57'),(36,'GET','/fruits/search?q=zzzznotafruit',0,'127.0.0.1','2026-11-01 17:48:57'),(37,'GET','/fruits/calories/50',26,'127.0.0.1','2026-11-01 17:48:57'),(38,'GET','/fruits/calories/0',0,'127.0.0.1','2026-11-01 17:48:57'),(39,'GET','/docs',0,'127.0.0.1','2026-11-01 17:48:57'),(40,'GET','/openapi.json',0,'127.0.0.1','2026-11-01 17:48:57'),(41,'GET','/fruits',49,'127.0.0.1','2026-11-01 17:50:15'),(42,'GET','/fruits',49,'127.0.0.1','2026-11-01 17:50:27'),(43,'GET','/fruits',49,'127.0.0.1','2026-11-01 17:50:49'),(44,'GET','/fruits',49,'127.0.0.1','2026-11-01 17:51:01'),(45,'GET','/fruits/search?q=Bana',1,'127.0.0.1','2026-11-01 17:51:17'),(46,'GET','/fruits/calories/23',2,'127.0.0.1','2026-11-01 17:51:25'),(47,'GET','/fruits',49,'127.0.0.1','2026-11-01 17:51:32'),(48,'GET','/fruits',49,'127.0.0.1','2026-11-01 17:51:46'),(49,'GET','/docs',0,'127.0.0.1','2026-11-01 17:51:47'),(50,'GET','/api/fruits',49,'127.0.0.1','2026-11-01 18:05:09'),(51,'GET','/api/search/apple',3,'127.0.0.1','2026-11-01 18:05:10'),(52,'GET','/api/search/APPLE',3,'127.0.0.1','2026-11-01 18:05:10'),(53,'GET','/api/search/zzzznotafruit',0,'127.0.0.1','2026-11-01 18:05:10'),(54,'GET','/api/calories/50',26,'127.0.0.1','2026-11-01 18:05:11'),(55,'GET','/api/calories/0',0,'127.0.0.1','2026-11-01 18:05:11'),(56,'GET','/api/calories/abc',0,'127.0.0.1','2026-11-01 18:05:11'),(57,'GET','/api/fruits',49,'127.0.0.1','2026-11-01 18:05:25'),(58,'GET','/api/fruits',49,'127.0.0.1','2026-11-01 18:07:01'),(59,'GET','/api/fruits',49,'127.0.0.1','2026-11-01 18:08:40');
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'logs_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-01 18:08:59
