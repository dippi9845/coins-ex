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
	Via varchar(255) not null,
	Citta varchar(255) not null,
	Provincia varchar(255) not null,
	`Codice Icentificativo` varchar(255) not null,
	Modello varchar(255) not null,
	`Versione Software` varchar(255) not null,
	`Spread attuale` int not null CHECK (`Spread attuale` > 0),
	primary key (`Codice Icentificativo`));

DROP TABLE IF EXISTS ContoCorrente;
CREATE TABLE ContoCorrente (
	Indirizzo varchar(255) not null,
	Saldo varchar(255) not null,
	primary key (Indirizzo)
);

DROP TABLE IF EXISTS Wallet;
CREATE TABLE Wallet (
	Indirizzo varchar(255) not null,
	Saldo varchar(255) not null,
	primary key (Indirizzo)
);

DROP TABLE IF EXISTS Fiat;
CREATE TABLE Fiat (
	Nome varchar(255) not null,
	Ticker varchar(255) not null,
	primary key (Ticker));

DROP TABLE IF EXISTS Crypto;
CREATE TABLE Crypto (
	Nome varchar(255) not null,
	Ticker varchar(255) not null,
	primary key (Ticker));

DROP TABLE IF EXISTS Dipendente;
CREATE TABLE Dipendente (
	Carica varchar(255) not null,
	Reparto varchar(255) not null,
	Nome varchar(255) not null,
	Cognome varchar(255) not null,
	Residenza varchar(255) not null,
	Matricola varchar(255) not null,
	Salario int not null CHECK (Salario>0),
	primary key (Matricola));

DROP TABLE IF EXISTS Exchange;
CREATE TABLE Exchange (
	Nome varchar(255) not null,
	`Sede Operativa` varchar(255) not null,
	`Sede Legale` varchar(255) not null,
	Nazione varchar(255) not null,
	`Sito web` varchar(255) not null,
	Fondatore varchar(255) not null,
	unique (`Sito web`),
	unique (`Sede Operativa`),
	unique (`Sede Legale`),
	primary key (Nome));

DROP TABLE IF EXISTS Ordine;
CREATE TABLE Ordine (
	`Tipo Ordine` ENUM("Vende", "Compra") not null,
	Quantita int not null CHECK (Quantita > 0),
	Data date not null,
	Ora time not null,
	primary key (Data, Ora));

DROP TABLE IF EXISTS Server;
CREATE TABLE Server (
	Host varchar(255) not null,
	Porta int not null,
	CONSTRAINT Hosting UNIQUE (Host,Porta));

DROP TABLE IF EXISTS Transazione;
CREATE TABLE Transazione (
	Quantita int not null CHECK (Quantita > 0),
	Ora date not null,
	Data time not null,
	primary key (Ora, Data),
	unique (Ora, Data));

DROP TABLE IF EXISTS Transazione_fisica;
CREATE TABLE Transazione_fisica (
	`Cambio attuale` int not null CHECK (`Cambio attuale` > 0),
	Quantita int not null CHECK (Quantita>0),
	Spread int not null CHECK (Spread > 0),
	Data date not null,
	Ora time not null,
	primary key (Data, Ora));

DROP TABLE IF EXISTS Utente;
CREATE TABLE Utente (
	ID int AUTO_INCREMENT,
	Email varchar(255) not null,
	Password varchar(255) not null,
	Nome varchar(255) not null,
	Cognome varchar(255) not null,
	Nazionalita varchar(255) not null,
	Residenza varchar(255) not null,
	`Numero Di Telefono` varchar(255) not null,
	`Data di nascita` date not null,
	`Codice Fiscale` varchar(255) not null,
	primary key (ID),
	unique (`Codice Fiscale`));

-- Constraints Section
-- ___________________


-- Index Section
-- _____________

