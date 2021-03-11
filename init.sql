CREATE DATABASE arteia_db;

\c arteia_db


CREATE TABLE items (
    item_id             varchar(50) PRIMARY KEY,
    random_int          integer,
    result              integer
);
