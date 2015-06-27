import urllib

def read_text():
    quotes = open ("/Users/Coder/Documents/Python/movie_quotes.txt")
    contents = quotes.read()
    print(contents)
    quotes.close()
    check_profanity(contents)

def check_profanity(text_to_check):
    connection = urllib.urlopen("http://www.wdyl.com/profanity?q=" + text_to_check)
    output = connection.read()
    connection.close()
    print(output)
    
read_text()
