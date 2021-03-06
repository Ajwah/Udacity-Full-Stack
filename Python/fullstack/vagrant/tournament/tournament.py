#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament


import psycopg2
import random
import math
from collections import namedtuple

global_tmp = 0
def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records FROM the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records FROM the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(name) FROM players")
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
    c.execute("INSERT INTO players VALUES (DEFAULT, %s,0,0,0, 0.000, 0.000)",(name,))
    DB.commit()
    DB.close()

def assertEvenNumberPlayers():
    if len(playerStandings()) % 2 == 1:
        registerPlayer("***")

def initOpponentHistory():
    DB = connect()
    c = DB.cursor()
    c.execute("DROP TABLE IF EXISTS opponentHistory")
    DB.commit()
    c.execute("CREATE TABLE opponentHistory AS SELECT id FROM players")
    DB.commit()
    DB.close()

def addColumnToOpponentHist(matchid):
    DB = connect()
    c = DB.cursor()
    c.execute('ALTER TABLE opponentHistory ADD COLUMN "%s" INT',(matchid,))
    DB.commit()
    DB.close()

def updateOpponentHistory(matchid, player, opponent):
    DB = connect()
    c = DB.cursor()
    c.execute('UPDATE opponenthistory SET "%(m_id)s"=%(opponent_id)s WHERE id=%(player_id)s' % {"m_id": matchid, "opponent_id": opponent, "player_id": player})
    c.execute('UPDATE opponenthistory SET "%(m_id)s"=%(player_id)s WHERE id=%(opponent_id)s' % {"m_id": matchid, "opponent_id": opponent, "player_id": player})
    DB.commit()
    DB.close()

def getMainColumnsPlayersTable():
    DB = connect()
    c = DB.cursor()
    c.execute('SELECT id, name, mw FROM players ORDER BY mw DESC, omw DESC')
    columns = c.fetchall()
    DB.close()
    return columns

def getOpponentHistory(briefly=True,column="1"):
    #Retrieve opponent history of all the players in the order of the current hierarchy from strongest to weakest players.
    DB = connect()
    c = DB.cursor()
    if briefly:
        c.execute('SELECT o.* FROM opponenthistory o, players p WHERE o.id=p.id ORDER BY p.mw DESC, p.omw DESC')
    else:
        if len(getColumnsTable('opponenthistory')) == 1:
            DB.close()
            return []
        else:
            c.execute('SELECT A.id, A.name, A.mw, B."{0}",B.name,B.mw FROM (SELECT o.id, name, mw, omw FROM opponenthistory o, players p where o.id=p.id ORDER BY mw DESC, omw DESC) as A JOIN (SELECT z.id, q.name, "{0}", q.mw FROM (SELECT o.id, "{0}",pl.name, pl.mw FROM opponenthistory o, players pl WHERE o.id=pl.id) z, players q WHERE "{0}"=q.id) AS B ON A.id=B.id ORDER BY A.mw DESC, A.omw DESC'.format(column))
    history = c.fetchall()
    DB.close()
    return history

def getColumnsTable(table):
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s'"%table)
    columns = c.fetchall()
    DB.close()
    return columns

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
    c.execute("SELECT id, name, wins, losses, draws, MW, OMW FROM players ORDER BY mw DESC, omw DESC")
    records = c.fetchall()
    DB.close()
    return records

def reportMatch(p1, p2, draw):
    """Records the outcome of a single match between two players.

    Args:
      In case of no draw:
        p1:  the id number of the player who won
        p2:  the id number of the player who lost
    """

    Score = namedtuple("Score", 'Id W L D')
    DB = connect()
    c = DB.cursor()
    if draw:
        p1s = Score(p1, 0, 0, 1)
        p2s = Score(p2, 0, 0, 1)
    else:
        p1s = Score(p1, 1, 0, 0)
        p2s = Score(p2, 0, 1, 0)
    c.execute("UPDATE players SET wins = wins + {0.W}, losses = losses + {0.L}, draws = draws + {0.D} WHERE id={0.Id}".format(p1s))
    c.execute("UPDATE players SET wins = wins + {0.W}, losses = losses + {0.L}, draws = draws + {0.D} WHERE id={0.Id}".format(p2s))

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
    tmpStack = []
    records = playerStandings()
    history = getOpponentHistory()

    for i in xrange(0,len(records),2):
        playerHistory = [element for element in history if element[0] == records[i][0]]
        #print "for loop: ", records[i][0], " vs ", records[i+1][0], "Does ",records[i+1][0]," occur in list: ", playerHistory[0], any(d == records[i+1][0] for d in playerHistory[0])
        #print i+1, len(records), len(playerHistory[0])
        #print
        while any(d == records[i+1][0] for d in playerHistory[0]) and (i < len(records) - 2):
            #print 'before', i+1, len(records), len(playerHistory[0])
            tmpStack.append(records[i+1])
            records.remove(records[i+1])
            #print i+1, len(records), len(playerHistory[0])
            #print "        while loop:", tmpStack, records
        if tmpStack != []:
            records[i+2:i+2] = tmpStack
            tmpStack = []

        swiss_pairings.append((records[i][0], records[i][1], records[i+1][0], records[i+1][1]))
        updateOpponentHistory(global_tmp, records[i][0], records[i+1][0])
    return swiss_pairings

def play():
    global global_tmp
    global_tmp += 1
    addColumnToOpponentHist(global_tmp)
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

def update_MW_OMW():
    DB = connect()
    c = DB.cursor()
    #UPDATE MW in players table
    c.execute("UPDATE players SET MW=(wins*3+draws)/(3*(wins + losses + draws))")
    c.execute("UPDATE players SET MW=0.333 WHERE MW<0.333")
    DB.commit()

    #UPDATE OMW in players table - (In multiple mini PSQL steps)
    #   Create a temporary table OMW AS an exact copy of opponenthistory,
    #   ADD COLUMN omw,
    #   add corresponding MW of various columns contained by OMW to column omw
    #   UPDATE players table with value of omw
    c.execute('DROP TABLE IF EXISTS omw')
    DB.commit()
    c.execute("CREATE TABLE omw AS (SELECT * FROM opponenthistory)")
    DB.commit()
    c.execute("SELECT * FROM omw")
    colnames = [desc[0] for desc in c.description]
    del colnames[0]
    c.execute("ALTER TABLE omw ADD COLUMN omw NUMERIC(5,3)")
    c.execute("UPDATE omw t1 SET omw=0.000")
    DB.commit()
    for col in colnames:
        c.execute('UPDATE omw t1 SET omw=t1.omw+(t2.mw/%(tot)s) FROM players t2 WHERE t2.id=t1."%(col)s"'% {"tot": len(colnames), "col": col})
    DB.commit()

    #UPDATE OMW in players table - (In one PSQL query)
    #   First reset column OMW to 0.000
    #   Based on table opponenthistory, UPDATE the OMW column

    #Retrieve all the column names of table opponenthistory
    c.execute("SELECT * FROM opponenthistory")
    colnames = [desc[0] for desc in c.description]
    #Remove id column.
    del colnames[0]
    #reset OMW column to 0.000
    c.execute("UPDATE players t0 SET omw=0.000")
    DB.commit()
    #Loop through all the columns of opponenthistory,
    #Look up the corresponding MW value FROM players table
    #Add that value to OMW column
    #Calculate average by dividing by amount of opponents faced so far
    for col in colnames:
        query = '''UPDATE players t0 SET omw=(omw + (t3.mw/%(tot)s))
                     FROM (
                            SELECT t1.id, t2.mw FROM (
                                                        SELECT id, "%(col)s" FROM opponenthistory
                                                     )  AS t1,
                                                     (
                                                        SELECT "%(col)s", mw FROM players RIGHT OUTER JOIN opponenthistory ON (players.id=opponenthistory."%(col)s")
                                                     )  AS t2
                                                WHERE t1."%(col)s"=t2."%(col)s"
                           ) AS t3
                    WHERE t3.id=t0.id'''% {"tot": len(colnames), "col": col}
        c.execute(query)
    DB.commit()
    DB.close()

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
    #registerPlayer("Shubacka Kabaka")

    assertEvenNumberPlayers()
    initOpponentHistory()

    for i in xrange(0,int(math.floor(math.log(len(playerStandings()),2)))):
        play()
        update_MW_OMW()
    display("players")
    display("opponenthistory")

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
    if table == "players":
        c.execute("SELECT * FROM players ORDER BY mw DESC, omw DESC")
    else:
        c.execute("SELECT * FROM %s" % table)
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

