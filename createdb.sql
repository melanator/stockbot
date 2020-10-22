CREATE TABLE holders(
    id integer PRIMARY KEY,
    name varchar(255));

CREATE TABLE portfolios(
    id integer PRIMARY KEY AUTOINCREMENT,
    name varchar(60),
    holder_id integer,
    margin real,
    broker varchar);

CREATE TABLE shares(
    id integer PRIMARY KEY AUTOINCREMENT,
    ticker varchar(15),
    amount integer,
    price real,
    stock varchar(5),
    holder_id integer,
    currency varchar,
    portfolio_id integer);

CREATE TABLE transactions(
    id integer PRIMARY KEY AUTOINCREMENT,
    ticker varchar(15),
    amount integer,
    price real,
    broker varchar(20),
    margin real,
    holder_id integer,
    portfolio_id integer,
    date datetime);
   



