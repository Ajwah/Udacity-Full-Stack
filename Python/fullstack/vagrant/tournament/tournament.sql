-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

drop table if exists matches;
drop table if exists players;

create table matches(
player1 text,
player2 text
);

create table players(
id serial,
name text,
wins numeric(2,1),
matches_played int
);
