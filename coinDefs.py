from random import getrandbits
import time

def flipCoinsWithRawData(totalFlips, tempList=None):
    if tempList is None:
        tempList = []
        totalHeads, totalTails = 0, 0
    for _ in range(totalFlips):
        isHead = True if getrandbits(1) == 1 else False
        if isHead:
            tempList.append('Heads')
            totalHeads += 1
        else:
            tempList.append('Tails')
            totalTails += 1
    return tempList, totalHeads, totalTails

def flipCoins(totalFlips):
    totalHeads, totalTails = 0, 0
    for _ in range(totalFlips):
        isHead = True if getrandbits(1) == 1 else False
        if isHead:
            totalHeads += 1
        else:
            totalTails += 1
    return totalHeads, totalTails

def exportRawStats(filename, rawData, rawDataLineDivider = ';'):
    with open(filename, 'w') as raw:
        stringList = f'{rawDataLineDivider}\n'.join(rawData)
        raw.write(stringList)

def exportTotalStats(filename, coinFlips, totalHeads, totalTails):
    with open(filename, 'w') as final:
        final.write(
            f'''| Total Flips :: {coinFlips:,}
| Total Heads :: {totalHeads:,}
| Total Tails :: {totalTails:,}\n\n''')

def startTimer():
    return time.perf_counter()

def endTimer(message, name):
    return f'Finished {message} in {round(time.perf_counter() - name, 2)} seconds.'