#
# Database access functions for the web forum.
#

import psycopg2

## Get posts from database.
def GetAllPosts():
    ## Database connection
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()

    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''

    c.execute("update posts set content='cheese' where content like '%spam%'")
    DB.commit()

    c.execute("delete from posts where content='cheese'")
    DB.commit()

    c.execute("select time, content from posts order by time desc")
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in c.fetchall()]
    posts.sort(key=lambda row: row['time'], reverse=True)

    DB.close()
    return posts

## Add a post to the database.
def AddPost(content):
    ## Database connection
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    c.execute("insert into posts (content) values (%s)",(content,))
    DB.commit()
    DB.close()