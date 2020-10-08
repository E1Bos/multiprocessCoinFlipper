import concurrent.futures
from multiprocessing import cpu_count
from coinDefs import *


def main():
    # DEFINING VARIABLES

    rawData, totalHeads, totalTails = [], 0, 0
    rawDataLineDivider = ';'
    coinFlipTime = startTimer()
    RAWDATAFILENAME = 'rawData.txt'
    FINALDATAFILENAME = 'finalData.txt'

    # TOTAL COIN FLIPS
    coinFlips = input('Coin Flips: ')
    try:
        coinFlips = int(coinFlips)
    except ValueError:
        exit()

    # INCLUDING RAW DATA (Y/N)
    useRawData = input('Include Raw Data (y/n): ')
    if useRawData.lower() == 'y':
        useRawData = True
    else:
        useRawData = False

    totalCores = cpu_count()
    for i in range(totalCores, 0, -1):
        if coinFlips % i == 0:
            totalProcesses = i
            break
    print(f'\nBest Amount of Threads Found :: {totalProcesses}\n')
    if totalProcesses == 1:
        ifPrime = input('-** WARNING **-\nOnly ONE Thread Will Be Used.\nThis Will Run Extremely Slow For Any Large Number\n(y/n): ')
        if ifPrime.lower() == 'y':
            pass
        else:
            exit()

    if useRawData:
        with open(RAWDATAFILENAME, 'w') as raw:
            raw.write('')
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(flipCoinsWithRawData, coinFlips//totalProcesses) for _ in range(totalProcesses)]
            for f in concurrent.futures.as_completed(results):
                tempList, tempHeads, tempTails = f.result()
                rawData += tempList
                totalHeads += tempHeads
                totalTails += tempTails
        print(endTimer('flipping coins', coinFlipTime))

        exportRawDataTime = startTimer()
        exportRawStats(RAWDATAFILENAME, rawData, rawDataLineDivider)
        print(endTimer('writing raw data', exportRawDataTime))

    else:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(flipCoins, coinFlips//totalProcesses) for _ in range(totalProcesses)]
            for f in concurrent.futures.as_completed(results):
                tempHeads, tempTails = f.result()
                totalHeads += tempHeads
                totalTails += tempTails
        print(endTimer('flipping coins', coinFlipTime))

    exportTotalStats(FINALDATAFILENAME, coinFlips, totalHeads, totalTails)

    print('Process Complete, Press Enter to Close.')
    input()

    exit()

if __name__ == '__main__':
    main()








