-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

drop table if exists matches;
drop table if exists players;
drop table if exists opponenthistory;
drop table if exists omw;
drop table if exists potential_opponents;

create table matches(
id serial
);

create table players(
id serial,
name text,
wins numeric(2,0),
losses numeric(2,0),
draws numeric(2,0),
MW numeric(4,3),
OMW numeric(4,3)
);

create table potential_opponents(
  id int,
  "1" int,
  "2" int,
  "3" int,
  "4" int,
  "5" int,
  "6" int,
  "7" int,
  "8" int,
  "9" int,
  "10" int,
  "11" int,
  "12" int,
  "13" int,
  "14" int,
  "15" int,
  "16" int
);