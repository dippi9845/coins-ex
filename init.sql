-- ***************************
-- * Standard SQL generation *
-- ***************************


-- DATABASE Section
-- ________________

DROP DATABASE IF EXISTS exchanges;
CREATE DATABASE exchanges;
USE exchanges;

-- TABLESpace Section
-- __________________

-- TABLE Section
-- _____________
DROP TABLE IF EXISTS ATM;
CREATE TABLE ATM (
	Via VARCHAR(255) NOT NULL,
	Citta VARCHAR(255) NOT NULL,
	Provincia VARCHAR(255) NOT NULL,
	`Codice Icentificativo` VARCHAR(255) NOT NULL,
	Modello VARCHAR(255) NOT NULL,
	`Versione Software` VARCHAR(255) NOT NULL,
	`Spread attuale` INT NOT NULL CHECK (`Spread attuale` > 0),
	PRIMARY KEY (`Codice Icentificativo`));

DROP TABLE IF EXISTS ContoCorrente;
CREATE TABLE ContoCorrente (
	UserID INT NOT NULL,
	Indirizzo VARCHAR(255) NOT NULL,
	Saldo INT NOT NULL CHECK(Saldo > 0),
	Nome VARCHAR(255) NOT NULL,
	Ticker VARCHAR(255) NOT NULL,
	PRIMARY KEY (Indirizzo)
);

DROP TABLE IF EXISTS Wallet;
CREATE TABLE Wallet (
	UserID INT NOT NULL,
	Indirizzo VARCHAR(255) NOT NULL,
	Saldo INT NOT NULL CHECK(Saldo > 0),
	Nome VARCHAR(255) NOT NULL,
	Ticker VARCHAR(255) NOT NULL,
	PRIMARY KEY (Indirizzo)
);

DROP TABLE IF EXISTS Fiat;
CREATE TABLE Fiat (
	Nome VARCHAR(255) NOT NULL,
	Ticker VARCHAR(255) NOT NULL,
	PRIMARY KEY (Ticker));

DROP TABLE IF EXISTS Crypto;
CREATE TABLE Crypto (
	Nome VARCHAR(255) NOT NULL,
	Ticker VARCHAR(255) NOT NULL,
	PRIMARY KEY (Ticker));

DROP TABLE IF EXISTS Dipendente;
CREATE TABLE Dipendente (
	Carica VARCHAR(255) NOT NULL,
	Reparto VARCHAR(255) NOT NULL,
	Nome VARCHAR(255) NOT NULL,
	Cognome VARCHAR(255) NOT NULL,
	Residenza VARCHAR(255) NOT NULL,
	Matricola VARCHAR(255) NOT NULL,
	Salario INT NOT NULL CHECK (Salario>0),
	PRIMARY KEY (Matricola));

DROP TABLE IF EXISTS Exchange;
CREATE TABLE Exchange (
	Nome VARCHAR(255) NOT NULL,
	`Sede Operativa` VARCHAR(255) NOT NULL,
	`Sede Legale` VARCHAR(255) NOT NULL,
	Nazione VARCHAR(255) NOT NULL,
	`Sito web` VARCHAR(255) NOT NULL,
	Fondatore VARCHAR(255) NOT NULL,
	UNIQUE (`Sito web`),
	UNIQUE (`Sede Operativa`),
	UNIQUE (`Sede Legale`),
	PRIMARY KEY (Nome));

DROP TABLE IF EXISTS Ordine;
CREATE TABLE Ordine (
	OrdineID INT AUTO_INCREMENT,
	UserID INT NOT NULL,
	`Ticker compro` VARCHAR(255) NOT NULL,
	`Ticker vendo` VARCHAR(255) NOT NULL,
	`Quantita compro` INT NOT NULL CHECK(`Quantita compro` > 0),
	`Quantita vendo` INT NOT NULL CHECK(`Quantita vendo` > 0),
	`Indirizzo compro` VARCHAR(255) NOT NULL,
	`Indirizzo vendo` VARCHAR(255) NOT NULL,
	Data DATE NOT NULL,
	Ora TIME NOT NULL,
	PRIMARY KEY (OrdineID));

DROP TABLE IF EXISTS Transazione;
CREATE TABLE Transazione (
	ID INT AUTO_INCREMENT,
	`Indirizzo Entrata` VARCHAR(255) NOT NULL,
	`Indirizzo Uscita` VARCHAR(255) NOT NULL,
	Ticker VARCHAR(255) NOT NULL,
	Quantita INT NOT NULL CHECK (Quantita > 0),
	Ora DATE NOT NULL,
	Data TIME NOT NULL,
	PRIMARY KEY (ID),

DROP TABLE IF EXISTS Transazione_fisica;
CREATE TABLE Transazione_fisica (
	`Cambio attuale` INT NOT NULL CHECK (`Cambio attuale` > 0),
	Quantita INT NOT NULL CHECK (Quantita>0),
	Spread INT NOT NULL CHECK (Spread > 0),
	Data DATE NOT NULL,
	Ora TIME NOT NULL,
	PRIMARY KEY (Data, Ora));

DROP TABLE IF EXISTS Utente;
CREATE TABLE Utente (
	ID INT AUTO_INCREMENT,
	Email VARCHAR(255) NOT NULL,
	Password VARCHAR(255) NOT NULL,
	Nome VARCHAR(255) NOT NULL,
	Cognome VARCHAR(255) NOT NULL,
	Nazionalita VARCHAR(255) NOT NULL,
	Residenza VARCHAR(255) NOT NULL,
	`Numero Di Telefono` VARCHAR(255) NOT NULL,
	`Data di nascita` DATE NOT NULL,
	`Codice Fiscale` VARCHAR(255) NOT NULL,
	PRIMARY KEY (ID),
	UNIQUE (`Codice Fiscale`));

-- TABLES RELATIONALS

DROP TABLE IF EXISTS registrati;
CREATE TABLE registrati (
	ID INT NOT NULL,
	Nome VARCHAR(255) NOT NULL);

DROP TABLE IF EXISTS scambio;
CREATE TABLE scambio (
	`Compro ID` INT NOT NULL,
	`Vendo ID` INT NOT NULL,
	`Ticker crypto` VARCHAR(255) NOT NULL,
	`Ticker fiat` VARCHAR(255) NOT NULL,
	`Quantita crypto` INT NOT NULL CHECK (`Quantita compro` > 0),
	`Qunatita fiat` INT NOT NULL CHECK (`Quantita vendo` > 0),
	Data DATE NOT NULL,
	Ora TIME NOT NULL
);

-- Instances needed section
INSERT INTO fiat (Nome, Ticker)
VALUES
("Euro, european", "EUR"),
("US dollar", "USD");

-- ConstraINTs Section
-- ___________________


-- Index Section
-- _____________

