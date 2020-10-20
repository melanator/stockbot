CREATE TABLE holders(
    id integer PRIMARY KEY,
    name varchar(255));

CREATE TABLE portfolios(
    id integer PRIMARY KEY AUTOINCREMENT,
    name varchar(60),
    holder_id integer);

CREATE TABLE shares(
    id integer PRIMARY KEY AUTOINCREMENT,
    ticker varchar(15),
    amount interger,
    price real,
    stock varchar(5),
    holder_id interger,
    portfolio_id integer);

CREATE TABLE transactions(
    id integer PRIMARY KEY AUTOINCREMENT,
    ticker varchar(15),
    amount interger,
    price real,
    stock varchar(5),
    holder_id interger,
    portfolio_id integer,
    date datetime);
   



