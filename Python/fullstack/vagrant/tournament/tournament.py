#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2
import random

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from matches")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from players")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("select count(name) from players")
    amount = c.fetchall()[0][0]
    DB.close()
    return amount

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("insert into players values (default, %s,0.0,0)",(name,))
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("select id, name, wins, matches_played from players order by wins desc")
    records = c.fetchall()
    DB.close()
    return records

def reportMatch(winner, loser, draw):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    if draw:
        print "draw"
        c.execute("update players set wins = wins + 0.5 where id=%s",(winner,))
        c.execute("update players set matches_played = matches_played + 1 where id=%s",(winner,))
        c.execute("update players set wins = wins + 0.5 where id=%s",(loser,))
        c.execute("update players set matches_played = matches_played + 1 where id=%s",(loser,))
    else:
        c.execute("update players set wins = wins + 1 where id=%s",(winner,))
        c.execute("update players set matches_played = matches_played + 1 where id=%s",(winner,))
        c.execute("update players set matches_played = matches_played + 1 where id=%s",(loser,))
    DB.commit()
    DB.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    swiss_pairings = []
    if len(playerStandings()) % 2 == 1:
        registerPlayer("***")
    records = playerStandings()
    for i in xrange(0,len(records),2):
        swiss_pairings.append((records[i][0], records[i][1], records[i+1][0], records[i+1][1]))
    return swiss_pairings