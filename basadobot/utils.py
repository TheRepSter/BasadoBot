from datetime import datetime as dt 

def printx(*args, **kwargs):
    print(dt.now().strftime('%Y-%m-%d %H:%M:%S'), end=" ")
    print(*args, **kwargs)
