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

create table matches(
id serial
);

create table players(
id serial,
name text,
wins numeric(2,0),
matches_played int
);
