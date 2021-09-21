from datetime import datetime as dt 

def printx(arg):
    print(dt.now().strftime('%Y-%m-%d %H:%M:%S'), end=" ")
    print(arg)
