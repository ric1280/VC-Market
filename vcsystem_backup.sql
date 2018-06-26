-- MySQL dump 10.13  Distrib 8.0.11, for Win64 (x86_64)
--
-- Host: localhost    Database: vcsystem
-- ------------------------------------------------------
-- Server version	8.0.11

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `client_job`
--

DROP TABLE IF EXISTS `client_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `client_job` (
  `Email` varchar(255) NOT NULL,
  `jobId` int(11) NOT NULL,
  PRIMARY KEY (`Email`,`jobId`),
  KEY `jobId` (`jobId`),
  CONSTRAINT `client_job_ibfk_1` FOREIGN KEY (`jobId`) REFERENCES `job` (`jobid`),
  CONSTRAINT `client_job_ibfk_2` FOREIGN KEY (`Email`) REFERENCES `users` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client_job`
--

LOCK TABLES `client_job` WRITE;
/*!40000 ALTER TABLE `client_job` DISABLE KEYS */;
/*!40000 ALTER TABLE `client_job` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job`
--

DROP TABLE IF EXISTS `job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `job` (
  `jobId` int(11) NOT NULL,
  `credibility` float(4,4) DEFAULT NULL,
  `CPU` int(11) DEFAULT NULL,
  `Disc` int(11) DEFAULT NULL,
  `RAM` int(11) DEFAULT NULL,
  `ExecTime` double DEFAULT NULL,
  `Status` varchar(255) DEFAULT NULL,
  `Price` int(11) DEFAULT NULL,
  `Deadline` int(11) DEFAULT NULL,
  `InitTime` double DEFAULT NULL,
  `RDataPath` varchar(255) DEFAULT NULL,
  `file` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`jobId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job`
--

LOCK TABLES `job` WRITE;
/*!40000 ALTER TABLE `job` DISABLE KEYS */;
/*!40000 ALTER TABLE `job` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `machine_job`
--

DROP TABLE IF EXISTS `machine_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `machine_job` (
  `mid` int(11) NOT NULL,
  `jobId` int(11) NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`mid`,`jobId`),
  KEY `jobId` (`jobId`),
  CONSTRAINT `machine_job_ibfk_1` FOREIGN KEY (`mid`) REFERENCES `machines` (`mid`),
  CONSTRAINT `machine_job_ibfk_2` FOREIGN KEY (`jobId`) REFERENCES `job` (`jobid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `machine_job`
--

LOCK TABLES `machine_job` WRITE;
/*!40000 ALTER TABLE `machine_job` DISABLE KEYS */;
/*!40000 ALTER TABLE `machine_job` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `machines`
--

DROP TABLE IF EXISTS `machines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `machines` (
  `mid` int(11) NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `CPU` int(11) DEFAULT NULL,
  `Disc` int(11) DEFAULT NULL,
  `RAM` int(11) DEFAULT NULL,
  `Price` int(11) DEFAULT NULL,
  `scj` int(11) DEFAULT NULL,
  `credibility` float DEFAULT NULL,
  PRIMARY KEY (`mid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `machines`
--

LOCK TABLES `machines` WRITE;
/*!40000 ALTER TABLE `machines` DISABLE KEYS */;
/*!40000 ALTER TABLE `machines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usermachines`
--

DROP TABLE IF EXISTS `usermachines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `usermachines` (
  `Email` varchar(255) NOT NULL,
  `mid` int(11) NOT NULL,
  KEY `Email` (`Email`),
  KEY `mid` (`mid`),
  CONSTRAINT `UserMachines_ibfk_1` FOREIGN KEY (`Email`) REFERENCES `users` (`email`),
  CONSTRAINT `UserMachines_ibfk_2` FOREIGN KEY (`mid`) REFERENCES `machines` (`mid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usermachines`
--

LOCK TABLES `usermachines` WRITE;
/*!40000 ALTER TABLE `usermachines` DISABLE KEYS */;
/*!40000 ALTER TABLE `usermachines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `users` (
  `Email` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Credits` int(11) DEFAULT NULL,
  PRIMARY KEY (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-26 18:13:07
