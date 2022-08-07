-- ***************************
-- * Standard SQL generation *
-- ***************************


-- Database Section
-- ________________

create database Exchange;


-- TableSpace Section
-- __________________

-- Table Section
-- _____________

create table ATM (
	Via varchar(255) not null,
	Città varchar(255) not null,
	Provincia varchar(255) not null,
	`Codice Icentificativo` varchar(255) not null,
	Modello varchar(255) not null,
	`Versione Software` varchar(255) not null,
	`Spread attuale` int not null CHECK (`Spread attuale` > 0),
	primary key (Codice Icentificativo));

create table Conto (
	Indirizzo varchar(255) not null,
	Saldo varchar(255) not null,
	primary key (Indirizzo));

create table ContoCorrente (
);

create table Crypto (
);

create table Dipendente (
	Carica varchar(255) not null,
	Reparto varchar(255) not null,
	Nome varchar(255) not null,
	Cognome varchar(255) not null,
	Residenza varchar(255) not null,
	Matricola varchar(255) not null,
	Salario int not null CHECK (Salario>0),
	primary key (Matricola));

create table Exchange (
	Nome varchar(255) not null,
	`Sede Operativa` varchar(255) not null,
	`Sede Legale` varchar(255) not null,
	Nazione varchar(255) not null,
	`Sito web` varchar(255) not null,
	Fondatore varchar(255) not null,
	unique (Sito web),
	unique (Sede Operativa),
	unique (Sede Legale),
	primary key (Nome));

create table Fiat (
);

create table Ordine (
	`Tipo Ordine` ENUM("Vende", "Compra") not null,
	Quantità int not null CHECK (Quantità > 0),
	Data date DEFAULT CURDATE(),
	Ora time DEFAULT CURTIME(),
	primary key (, Data, Ora));

create table Server (
	Host varchar(255) not null,
	Porta int not null,
	CONSTRAINT Hosting UNIQUE (Host,Porta);

create table Transazione (
	Quantità int not null CHECK (Quantità > 0),
	Ora date DEFAULT CURDATE(),
	Data time DEFAULT CURTIME(),
	primary key (, Ora, Data),
	unique (, Ora, Data));

create table Transazione_fisica (
	`Cambio attuale` int not null CHECK (`Cambio attuale` > 0),
	Quantità int not null CHECK (Quantità>0),
	Spread int not null CHECK (Spread > 0),
	Data date DEFAULT CURDATE(),
	Ora time DEFAULT CURTIME(),
	primary key (Data, Ora));

create table Utente (
	ID int AUTO_INCREMENT,
	Email varchar(255) not null,
	Password varchar(255) not null,
	Nome varchar(255) not null,
	Cognome varchar(255) not null,
	Nazionalità varchar(255) not null,
	Residenza varchar(255) not null,
	`Numero Di Telefono` varchar(255) not null,
	`Data di nascita` date not null,
	`Codice Fiscale` varchar(255) not null,
	primary key (ID),
	unique (Codice Fiscale));

create table Valuta (
	Nome varchar(255) not null,
	Ticker varchar(255) not null,
	primary key (Ticker));

create table Wallet (
);


-- Constraints Section
-- ___________________


-- Index Section
-- _____________

