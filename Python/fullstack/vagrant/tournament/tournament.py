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

def play():
    pairings = swissPairings()
    for i in xrange(0,len(pairings)):
        if pairings[i][1] == "***":
            reportMatch(pairings[i][2],pairings[i][0], False)
        elif pairings[i][3] == "***":
            reportMatch(pairings[i][0],pairings[i][2], False)
        else:
            outcome = random.randint(1,3)
            if outcome == 1:
                reportMatch(pairings[i][0],pairings[i][2], False)
            elif outcome == 2:
                reportMatch(pairings[i][2],pairings[i][0], False)
            else:
                reportMatch(pairings[i][0],pairings[i][2], True)

def create_tournament():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    registerPlayer("Chandra Nalaar")
    '''
    registerPlayer("Shubacka Kabaka")
    '''
    play()
    display("players")
    play()
    display("players")
    play()
    display("players")

def display(table):

    def stringify(ch, a):
        s = ''
        for i in xrange(0,a):
            s += ch
        return s

    def determine_column_sizes(colnames, tableContents):
        sizes = []
        for i in xrange(0,len(colnames)):
            if len(tableContents) == 0:
                maxSize = 0
            else:
                maxSize = max([len(str(desc[i])) for desc in tableContents])
            if maxSize > len(colnames[i]):
                sizes.append(maxSize)
            else:
                sizes.append(len(colnames[i]))
        return sizes

    def helper_column_headings(f, colnames, s1, s2, sizes):
        heading = ''
        for i in xrange(0,len(colnames)):
            t = f(colnames[i])
            size = len(t)
            heading += s1 + t + stringify(s1, sizes[i] - size) + s1 + s2
        return heading

    def create_title(colnames, sizes):
        return helper_column_headings(lambda x: x, colnames, ' ', '|', sizes)

    def underline_title(colnames, sizes):
        return helper_column_headings(lambda x: stringify('-', len(x)), colnames, '-', '+', sizes)

    def upperline_title(colnames, sizes):
        return helper_column_headings(lambda x: stringify('-', len(x)), colnames, '-', '-', sizes)

    def create_rows(max, tableContents, sizes):
        rows = []
        for i in xrange(0,len(tableContents)):
            row = ''
            for j in xrange(0, max):
                spaces = stringify(' ', sizes[j] - len(str(tableContents[i][j])))
                row += ' ' + str(tableContents[i][j]) + spaces + ' |'
            rows.append(row)
        return rows

    def display(s):
        spaces = '                  |'
        print spaces + s

    DB = connect()
    c = DB.cursor()
    c.execute("select * from %s order by wins desc" % table)
    colnames = [desc[0] for desc in c.description] #Obtain the various column names of 'table'
    tableContents = c.fetchall()
    sizes = determine_column_sizes(colnames, tableContents)
    rows = create_rows(len(colnames), tableContents, sizes)
    line = upperline_title(colnames, sizes)
    print ""
    display(line)
    display(stringify(' ', len(line) / 2 - (len(table) / 2)) + table)
    display(line)
    display(create_title(colnames, sizes))
    display(underline_title(colnames, sizes))
    for row in rows: display(row)
    display(line)
    print ""
    DB.close()

if __name__ == '__main__':
    create_tournament()

