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
	Via char(1) not null,
	Città char(1) not null,
	Provincia char(1) not null,
	Codice Icentificativo char(1) not null,
	Modello char(1) not null,
	Versione Software char(1) not null,
	Spread attuale char(1) not null,
	primary key (Codice Icentificativo));

create table Conto (
	Indirizzo char(1) not null,
	Saldo char(1) not null,
	primary key (Indirizzo));

create table ContoCorrente (
);

create table Crypto (
);

create table Dipendente (
	Carica char(1) not null,
	Reparto char(1) not null,
	Nome char(1) not null,
	Cognome char(1) not null,
	Residenza char(1) not null,
	Matricola char(1) not null,
	Salario char(1) not null,
	primary key (Matricola));

create table Exchange (
	Nome char(1) not null,
	Sede Operativa char(1) not null,
	Sede Legale char(1) not null,
	Nazione char(1) not null,
	Sito web char(1) not null,
	Fondatore char(1) not null,
	New attribute char(1) not null,
	unique (Sito web),
	unique (Sede Operativa),
	unique (Sede Legale),
	primary key (Nome));

create table Fiat (
);

create table Ordine (
	Tipo Ordine char(1) not null,
	Quantità char(1) not null,
	Data char(1) not null,
	Ora char(1) not null,
	primary key (, Data, Ora));

create table Server (
	Host char(1) not null,
	Porta char(1) not null,
	Nome -- ERROR
,
	primary key (Nome -- atr decomp --));

create table Transazione (
	Quantità char(1) not null,
	Ora char(1) not null,
	Data char(1) not null,
	primary key (, Ora, Data),
	unique (, Ora, Data));

create table Transazione_fisica (
	Cambio attuale char(1) not null,
	Quantità char(1) not null,
	Spread char(1) not null,
	Data char(1) not null,
	Ora char(1) not null,
	primary key (Data, Ora));

create table Utente (
	ID char(1) not null,
	Email char(1) not null,
	Password char(1) not null,
	Nome char(1) not null,
	Cognome char(1) not null,
	Nazionalità char(1) not null,
	Residenza char(1) not null,
	Numero Di Telefono char(1) not null,
	Data di nascita char(1) not null,
	Codice Fiscale char(1) not null,
	primary key (ID),
	unique (Codice Fiscale));

create table Valuta (
	Nome char(1) not null,
	Ticker char(1) not null,
	primary key (Ticker));

create table Wallet (
);


-- Constraints Section
-- ___________________


-- Index Section
-- _____________

