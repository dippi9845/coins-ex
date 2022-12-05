-- ***************************
-- * Standard SQL generation *
-- ***************************


-- DATABASE Section
-- ________________

CREATE USER IF NOT EXISTS 'db-project'@'localhost' IDENTIFIED BY 'db-project';

GRANT ALL PRIVILEGES ON exchanges . * TO 'db-project'@'localhost';

CREATE DATABASE  IF NOT EXISTS `exchanges` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `exchanges`;

-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: exchanges
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `atm`
--

DROP TABLE IF EXISTS `atm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `atm` (
  `Codice Icentificativo` int unsigned NOT NULL AUTO_INCREMENT,
  `Via` varchar(255) NOT NULL,
  `Citta` varchar(255) NOT NULL,
  `Provincia` varchar(255) NOT NULL,
  `Modello` varchar(255) NOT NULL,
  `Versione Software` varchar(255) NOT NULL,
  `Presso` varchar(255) NOT NULL,
  `Commissione` int unsigned NOT NULL,
  PRIMARY KEY (`Codice Icentificativo`),
  KEY `exchange_idx` (`Presso`),
  CONSTRAINT `exchange` FOREIGN KEY (`Presso`) REFERENCES `exchange` (`Nome`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contante`
--

DROP TABLE IF EXISTS `contante`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contante` (
  `Ticker fiat` varchar(255) NOT NULL,
  `Codice ATM` varchar(255) NOT NULL,
  `Quantita` int NOT NULL,
  CONSTRAINT `contante_chk_1` CHECK ((`Quantita` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contocorrente`
--

DROP TABLE IF EXISTS `contocorrente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contocorrente` (
  `UserID` int NOT NULL,
  `Indirizzo` varchar(255) NOT NULL,
  `Saldo` int NOT NULL,
  `Nome` varchar(255) NOT NULL,
  `Ticker` varchar(255) NOT NULL,
  PRIMARY KEY (`Indirizzo`),
  KEY `fiat_idx` (`Ticker`),
  CONSTRAINT `fiat` FOREIGN KEY (`Ticker`) REFERENCES `fiat` (`Ticker`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `contocorrente_chk_1` CHECK ((`Saldo` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crypto`
--

DROP TABLE IF EXISTS `crypto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crypto` (
  `Nome` varchar(255) NOT NULL,
  `Ticker` varchar(255) NOT NULL,
  PRIMARY KEY (`Ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dipendente`
--

DROP TABLE IF EXISTS `dipendente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dipendente` (
  `Carica` varchar(255) NOT NULL,
  `Reparto` varchar(255) NOT NULL,
  `Nome` varchar(255) NOT NULL,
  `Cognome` varchar(255) NOT NULL,
  `Residenza` varchar(255) NOT NULL,
  `Matricola` int unsigned NOT NULL AUTO_INCREMENT,
  `Salario` int NOT NULL,
  `Presso` varchar(255) NOT NULL,
  `Supervisore` int unsigned DEFAULT NULL,
  PRIMARY KEY (`Matricola`),
  KEY `supervisione_idx` (`Supervisore`),
  KEY `azienda_idx` (`Presso`),
  CONSTRAINT `azienda` FOREIGN KEY (`Presso`) REFERENCES `exchange` (`Nome`) ON UPDATE CASCADE,
  CONSTRAINT `supervisione` FOREIGN KEY (`Supervisore`) REFERENCES `dipendente` (`Matricola`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `dipendente_chk_1` CHECK ((`Salario` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `exchange`
--

DROP TABLE IF EXISTS `exchange`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exchange` (
  `Nome` varchar(255) NOT NULL,
  `Sede Operativa` varchar(255) NOT NULL,
  `Sede Legale` varchar(255) NOT NULL,
  `Sito web` varchar(255) NOT NULL,
  `Fondatore` varchar(255) NOT NULL,
  PRIMARY KEY (`Nome`),
  UNIQUE KEY `Sito web` (`Sito web`),
  UNIQUE KEY `Sede Operativa` (`Sede Operativa`),
  UNIQUE KEY `Sede Legale` (`Sede Legale`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fiat`
--

DROP TABLE IF EXISTS `fiat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fiat` (
  `Nome` varchar(255) NOT NULL,
  `Ticker` varchar(255) NOT NULL,
  PRIMARY KEY (`Ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ordine`
--

DROP TABLE IF EXISTS `ordine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordine` (
  `OrdineID` int NOT NULL AUTO_INCREMENT,
  `Ticker compro` varchar(255) NOT NULL,
  `Ticker vendo` varchar(255) NOT NULL,
  `Quantita compro` int NOT NULL,
  `Quantita vendo` int NOT NULL,
  `Indirizzo compro` varchar(255) NOT NULL,
  `Indirizzo vendo` varchar(255) NOT NULL,
  `Data` date NOT NULL DEFAULT (curdate()),
  `Ora` time NOT NULL DEFAULT (curtime()),
  PRIMARY KEY (`OrdineID`),
  CONSTRAINT `ordine_chk_1` CHECK ((`Quantita compro` > 0)),
  CONSTRAINT `ordine_chk_2` CHECK ((`Quantita vendo` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=9733 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registrati`
--

DROP TABLE IF EXISTS `registrati`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registrati` (
  `ID` int NOT NULL,
  `Exchange` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `exchange_fk_idx` (`Exchange`),
  CONSTRAINT `exchange_fk` FOREIGN KEY (`Exchange`) REFERENCES `exchange` (`Nome`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Utenti` FOREIGN KEY (`ID`) REFERENCES `utente` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `scambio`
--

DROP TABLE IF EXISTS `scambio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scambio` (
  `Transazione crypto` int unsigned NOT NULL,
  `Transazione fiat` int unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transazione`
--

DROP TABLE IF EXISTS `transazione`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transazione` (
  `ID` int unsigned NOT NULL AUTO_INCREMENT,
  `Indirizzo Entrata` varchar(255) NOT NULL,
  `Indirizzo Uscita` varchar(255) NOT NULL,
  `Ticker` varchar(255) NOT NULL,
  `Quantita` int NOT NULL,
  `Data` date NOT NULL DEFAULT (curdate()),
  `Ora` time NOT NULL DEFAULT (curtime()),
  PRIMARY KEY (`ID`),
  CONSTRAINT `transazione_chk_1` CHECK ((`Quantita` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=18924 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transazione_fisica`
--

DROP TABLE IF EXISTS `transazione_fisica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transazione_fisica` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Quantita` int unsigned NOT NULL,
  `Data` date NOT NULL DEFAULT (curdate()),
  `Ora` time NOT NULL DEFAULT (curtime()),
  `Tipo` enum('Prelievo','Deposito') NOT NULL,
  `Conto` varchar(255) NOT NULL,
  `ATM` int unsigned NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `conto_corrente_fk_idx` (`Conto`),
  KEY `ATM_fk_idx` (`ATM`),
  CONSTRAINT `ATM_fk` FOREIGN KEY (`ATM`) REFERENCES `atm` (`Codice Icentificativo`),
  CONSTRAINT `conto_corrente_fk` FOREIGN KEY (`Conto`) REFERENCES `contocorrente` (`Indirizzo`),
  CONSTRAINT `transazione_fisica_chk_2` CHECK ((`Quantita` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `utente`
--

DROP TABLE IF EXISTS `utente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utente` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Nome` varchar(255) NOT NULL,
  `Cognome` varchar(255) NOT NULL,
  `Nazionalita` varchar(255) NOT NULL,
  `Residenza` varchar(255) NOT NULL,
  `Numero Di Telefono` varchar(255) NOT NULL,
  `Data di nascita` date NOT NULL,
  `Codice Fiscale` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Codice Fiscale` (`Codice Fiscale`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wallet`
--

DROP TABLE IF EXISTS `wallet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wallet` (
  `UserID` int NOT NULL,
  `Indirizzo` varchar(255) NOT NULL,
  `Saldo` int NOT NULL,
  `Nome` varchar(255) NOT NULL,
  `Ticker` varchar(255) NOT NULL,
  PRIMARY KEY (`Indirizzo`),
  CONSTRAINT `wallet_chk_1` CHECK ((`Saldo` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-05 22:37:58


INSERT INTO fiat (Nome, Ticker)
VALUES
("Euro, european", "EUR"),
("US dollar", "USD");

INSERT INTO crypto (Nome, Ticker)
VALUES
("Bitcoin", "BTC"),
("Etherium", "ETH");



-- CREATE INDEX FK_Dipendente_Dipendente ON Dipendente (Supervisore);
-- CREATE INDEX FK_Exchange_Dipendente ON Dipendente (Presso);
-- ALTER TABLE Dipendente ADD CONSTRAINT FK_Dipendente_Dipendente FOREIGN KEY (Supervisore) REFERENCES Dipendente(Matricola);
-- ALTER TABLE Dipendente ADD CONSTRAINT FK_Exchange_Dipendente FOREIGN KEY (Presso) REFERENCES Dipendente(Presso);
