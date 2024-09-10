def up_or_down(data):
    if(not data):
        return "DOWN"
    onesCount = 0
    for each in data:
        onesCount += each[0]
    dataLength = len(data)
    if((onesCount / dataLength) == 0.6):
        return "DOWN"
    else:
        return "UP"
# Export the function
__all__ = ['up_or_down']
