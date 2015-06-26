import time
import webbrowser

count = 0
while (count < 3):
    time.sleep(2)
    webbrowser.open("http:\\google.ca")
    print 'The count is:', count
    count = count + 1 

print "Good bye!"
