-- MySQL dump 10.13  Distrib 8.0.12, for Win64 (x86_64)
--
-- Host: localhost    Database: vcsystem
-- ------------------------------------------------------
-- Server version	8.0.12

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
-- Table structure for table `availability`
--

DROP TABLE IF EXISTS `availability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `availability` (
  `mid` int(11) NOT NULL,
  `uptime` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `availability`
--

LOCK TABLES `availability` WRITE;
/*!40000 ALTER TABLE `availability` DISABLE KEYS */;
INSERT INTO `availability` VALUES (1,211),(1,66.6570000648),(1,553.57400012),(1,457.099999905),(1,316.815000057),(1,344.438000202),(1,414.376999855),(3,492.578000069),(2,288.690000057);
/*!40000 ALTER TABLE `availability` ENABLE KEYS */;
UNLOCK TABLES;

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
  `MeanUptime` double DEFAULT NULL,
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
-- Table structure for table `job_quiz`
--

DROP TABLE IF EXISTS `job_quiz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `job_quiz` (
  `jobId` int(11) NOT NULL,
  `input` int(11) DEFAULT NULL,
  PRIMARY KEY (`jobId`),
  KEY `input` (`input`),
  CONSTRAINT `job_quiz_ibfk_1` FOREIGN KEY (`input`) REFERENCES `market_quiz` (`input`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_quiz`
--

LOCK TABLES `job_quiz` WRITE;
/*!40000 ALTER TABLE `job_quiz` DISABLE KEYS */;
/*!40000 ALTER TABLE `job_quiz` ENABLE KEYS */;
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
  `RDataPath` varchar(255) DEFAULT NULL,
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
INSERT INTO `machines` VALUES (1,'Machine2',500000000,100000,2048,5,10,0.9988),(2,'Machine1',500000000,100000,2048,5,3,0.996),(3,'Machine3',500000000,100000,2048,5,7,0.998286);
/*!40000 ALTER TABLE `machines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `market_quiz`
--

DROP TABLE IF EXISTS `market_quiz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `market_quiz` (
  `input` int(11) NOT NULL,
  `output` double DEFAULT NULL,
  PRIMARY KEY (`input`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `market_quiz`
--

LOCK TABLES `market_quiz` WRITE;
/*!40000 ALTER TABLE `market_quiz` DISABLE KEYS */;
INSERT INTO `market_quiz` VALUES (207,88),(657,51),(724,20),(800,28),(822,134),(1090,44),(1454,47),(2251,37),(2346,120),(2635,53),(2702,159),(3177,53),(3404,61),(3479,56),(3517,149),(3641,118),(3805,30),(4936,134),(5070,85),(5457,67),(5519,160),(5905,142),(5933,142),(6304,31),(6445,23),(7032,150),(7503,62),(7693,52),(7936,114),(8282,127),(8627,52),(8778,140),(9001,140),(9441,104),(10212,179),(10344,104),(10659,55),(10683,99),(11080,68),(11287,86),(11642,143),(11707,143),(11841,187),(11874,143),(12239,63),(12295,50),(12550,37),(12824,63),(12847,76),(12871,169),(13374,50),(13389,94),(13395,94),(13671,120),(13945,151),(13974,151),(14218,120),(15320,177),(15356,115),(15366,40),(15779,102),(16362,66),(16809,159),(16867,84),(16915,58),(17153,66),(17499,110),(17715,110),(17723,97),(17784,185),(18051,48),(18463,61),(18793,110),(18946,61),(19722,74),(19944,136),(20072,136),(20088,92),(20104,136),(20142,136),(20215,87),(20266,35),(20456,136),(20482,180),(20736,30),(21761,69),(22395,74),(22568,38),(22873,69),(22952,38),(23593,82),(24289,51),(24635,157),(24729,157),(24864,38),(25181,126),(25316,157),(25413,56),(25458,108),(25763,126),(25888,51),(26139,108),(26439,77),(27842,108),(27871,152),(28612,77),(28720,72),(29129,59),(29236,134),(29648,134),(30159,103),(30605,41),(31022,54),(31221,178),(31521,178),(31848,28),(31857,28),(32468,41),(32975,98),(33100,98),(33384,129),(33553,67),(33582,67),(33823,204),(34008,85),(34013,85),(34378,28),(34823,173),(35026,80),(35546,98),(35721,72),(36315,49),(38141,106),(38146,54),(38570,23),(38653,186),(38954,137),(39170,168),(39465,106),(40177,93),(40612,62),(40751,36),(42131,106),(42742,132),(43064,75),(43180,70),(43266,163),(43581,101),(43607,163),(43749,163),(44138,132),(44458,132),(44514,132),(44763,114),(45535,83),(45929,132),(46060,114),(46568,145),(46692,83),(46935,145),(47545,52),(47652,114),(47669,52),(48159,189),(48197,44),(48542,251),(48677,158),(49286,158),(50012,114),(51317,52),(51513,52),(51669,78),(51789,127),(51938,140),(52640,140),(52743,78),(52915,140),(53014,78),(53164,78),(53210,47),(53403,140),(53657,78),(54965,153),(55033,153),(55152,60),(55370,78),(55441,91),(56693,60),(57060,52),(57207,52),(57209,166),(57549,166),(57789,158),(57872,166),(57991,135),(58714,197),(58977,148),(59169,60),(59172,60),(60063,117),(60094,65),(60157,272),(60776,73),(60817,60),(60900,86),(61343,91),(61686,166),(61720,55),(62057,117),(62518,135),(62699,135),(63332,148),(63556,55),(63969,148),(64621,104),(64878,192),(64894,153),(65004,99),(65022,86),(65039,73),(66155,143),(66290,104),(66533,205),(66561,55),(66606,68),(67576,161),(67653,86),(68212,130),(68324,174),(68676,81),(68765,143),(68822,130),(68852,112),(69016,55),(69065,130),(69598,205),(70071,205),(70181,218),(70454,104),(70856,112),(71291,99),(71651,94),(71883,94),(71964,143),(72148,143),(72964,63),(72985,218),(73191,63),(73474,187),(73568,156),(73649,50),(73889,81),(73948,94),(74119,143),(74313,112),(74581,125),(74715,187),(74753,94),(74831,187),(75724,63),(75757,94),(76081,55),(76351,81),(76759,107),(76958,169),(77257,107),(77451,76),(77707,63),(77708,50),(78257,182),(78643,50),(78922,99),(79078,125),(79580,138),(79707,81),(79763,76),(80233,94),(80430,120),(80540,213),(81314,76),(81556,182),(81636,89),(82924,164),(82996,45),(83078,89),(83130,107),(83190,213),(83341,45),(83734,133),(83841,89),(83930,89),(83959,89),(84303,195),(84602,81),(84767,133),(84819,133),(85054,63),(85316,195),(85543,151),(85664,76),(85916,195),(85991,195),(86309,195),(86681,71),(87067,195),(87493,45),(87870,58),(88311,120),(88652,71),(88719,120),(88801,102),(88807,102),(89545,71),(89680,102),(89698,71),(89768,89),(90292,89),(90551,102),(90715,63),(90976,177),(91028,133),(91214,84),(91308,84),(91334,133),(91839,208),(92536,133),(92726,208),(92844,177),(93374,58),(93417,208),(93522,71),(93559,84),(93614,146),(93783,133),(94705,102),(94714,177),(94775,84),(95697,146),(95846,190),(96043,84),(96274,71),(96822,84),(96923,159),(97292,66),(97343,151),(98266,71),(98528,159),(99164,159),(99584,128),(99841,97);
/*!40000 ALTER TABLE `market_quiz` ENABLE KEYS */;
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
INSERT INTO `usermachines` VALUES ('Test@gmail.com',1),('Test@gmail.com',2),('Test@gmail.com',3);
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
INSERT INTO `users` VALUES ('Test@gmail.com','pw',500);
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

-- Dump completed on 2018-08-27 17:39:53
