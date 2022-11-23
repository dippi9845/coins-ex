-- ***************************
-- * Standard SQL generation *
-- ***************************


-- DATABASE Section
-- ________________

CREATE USER IF NOT EXISTS 'db-project'@'localhost' IDENTIFIED BY 'db-project';

DROP DATABASE IF EXISTS exchanges_tests;
CREATE DATABASE exchanges_tests;
USE exchanges_tests;

GRANT ALL PRIVILEGES ON exchanges_tests . * TO 'db-project'@'localhost';

-- TABLESpace Section
-- __________________

-- TABLE Section
-- _____________

DROP TABLE IF EXISTS `atm`;
CREATE TABLE `atm` (
  `Via` varchar(255) NOT NULL,
  `Citta` varchar(255) NOT NULL,
  `Provincia` varchar(255) NOT NULL,
  `Codice Icentificativo` varchar(255) NOT NULL,
  `Modello` varchar(255) NOT NULL,
  `Versione Software` varchar(255) NOT NULL,
  `Spread attuale` int NOT NULL,
  PRIMARY KEY (`Codice Icentificativo`),
  CONSTRAINT `atm_chk_1` CHECK ((`Spread attuale` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `contocorrente`;
CREATE TABLE `contocorrente` (
  `UserID` int NOT NULL,
  `Indirizzo` varchar(255) NOT NULL,
  `Saldo` int NOT NULL,
  `Nome` varchar(255) NOT NULL,
  `Ticker` varchar(255) NOT NULL,
  PRIMARY KEY (`Indirizzo`),
  CONSTRAINT `contocorrente_chk_1` CHECK ((`Saldo` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `wallet_utente`;
CREATE TABLE `wallet_utente` (
  `UserID` int NOT NULL,
  `Indirizzo` varchar(255) NOT NULL,
  `Saldo` int NOT NULL,
  `Nome` varchar(255) NOT NULL,
  `Ticker` varchar(255) NOT NULL,
  PRIMARY KEY (`Indirizzo`),
  CONSTRAINT `wallet_utente_chk_1` CHECK ((`Saldo` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `wallet_atm`;
CREATE TABLE `wallet_atm` (
  `ATM_ID` int NOT NULL,
  `Indirizzo` varchar(255) NOT NULL,
  `Saldo` int NOT NULL,
  `Nome` varchar(255) NOT NULL,
  `Ticker` varchar(255) NOT NULL,
  PRIMARY KEY (`Indirizzo`),
  CONSTRAINT `wallet_atm_chk_1` CHECK ((`Saldo` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `fiat`;
CREATE TABLE `fiat` (
  `Nome` varchar(255) NOT NULL,
  `Ticker` varchar(255) NOT NULL,
  PRIMARY KEY (`Ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `crypto`;
CREATE TABLE `crypto` (
  `Nome` varchar(255) NOT NULL,
  `Ticker` varchar(255) NOT NULL,
  PRIMARY KEY (`Ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `dipendente`;
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
  CONSTRAINT `azienda` FOREIGN KEY (`Presso`) REFERENCES `exchange` (`Nome`),
  CONSTRAINT `supervisione` FOREIGN KEY (`Supervisore`) REFERENCES `dipendente` (`Matricola`),
  CONSTRAINT `dipendente_chk_1` CHECK ((`Salario` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `exchange`;
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

DROP TABLE IF EXISTS `ordine`;
CREATE TABLE `ordine` (
  `OrdineID` int NOT NULL AUTO_INCREMENT,
  `UserID` int NOT NULL,
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `transazione`;
CREATE TABLE `transazione` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Indirizzo Entrata` varchar(255) NOT NULL,
  `Indirizzo Uscita` varchar(255) NOT NULL,
  `Ticker` varchar(255) NOT NULL,
  `Quantita` int NOT NULL,
  `Data` date NOT NULL DEFAULT (curdate()),
  `Ora` time NOT NULL DEFAULT (curtime()),
  PRIMARY KEY (`ID`),
  CONSTRAINT `transazione_chk_1` CHECK ((`Quantita` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `transazione_fisica`;
CREATE TABLE `transazione_fisica` (
  `Cambio attuale` int NOT NULL,
  `Quantita` int NOT NULL,
  `Spread` int NOT NULL,
  `Data` date NOT NULL DEFAULT (curdate()),
  `Ora` time NOT NULL DEFAULT (curtime()),
  PRIMARY KEY (`Data`,`Ora`),
  CONSTRAINT `transazione_fisica_chk_1` CHECK ((`Cambio attuale` > 0)),
  CONSTRAINT `transazione_fisica_chk_2` CHECK ((`Quantita` > 0)),
  CONSTRAINT `transazione_fisica_chk_3` CHECK ((`Spread` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `utente`;
CREATE TABLE `utente` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Nome` varchar(255) NOT NULL,
  `Cognome` varchar(255) NOT NULL,
  `Nazionalita` varchar(255) NOT NULL,
  `Residenza` varchar(255) NOT NULL,
  `Numero Di Telefono` varchar(255) NOT NULL,
  `Data di nascita` date NOT NULL,
  `Codice Fiscale` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Codice Fiscale` (`Codice Fiscale`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `registrati`;
CREATE TABLE `registrati` (
  `ID` int NOT NULL,
  `Nome` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `scambio`;
CREATE TABLE `scambio` (
  `Transazione crypto` int NOT NULL,
  `Transazione fiat` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `contante`;
CREATE TABLE `contante` (
  `Ticker fiat` varchar(255) NOT NULL,
  `Codice ATM` varchar(255) NOT NULL,
  `Quantita` int NOT NULL,
  CONSTRAINT `contante_chk_1` CHECK ((`Quantita` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
