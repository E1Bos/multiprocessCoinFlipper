import concurrent.futures
from multiprocessing import cpu_count
from coinDefs import *


def main():
    # DEFINING VARIABLES
    rawData, totalHeads, totalTails = [], 0, 0
    rawDataLineDivider = ';'
    RAWDATAFILENAME = 'rawData.txt'
    FINALDATAFILENAME = 'finalData.txt'

    # TOTAL COIN FLIPS
    coinFlips = input('Coin Flips: ')
    try:
        coinFlips = int(coinFlips)
    except ValueError:
        exit()

    # INCLUDING RAW DATA
    wT_ET = round(0.0553 + 1.04E-07 * coinFlips + 4.59E-17 * coinFlips ** 2, 2)
    useRawDataInp = input(f'\nInclude Raw Data? (Write Time ET {wT_ET}s) (y/n): ')

    useRawData = False
    if useRawDataInp.lower() == 'y':
        useRawData = True

    # FASTEST AMOUNT OF THREADS
    totalCores = cpu_count()
    for i in range(totalCores, 0, -1):
        if coinFlips % i == 0:
            totalProcesses = i
            break
    print(f'\nFastest Amount of Threads Found :: {totalProcesses}\n')
    if totalProcesses == 1:
        ifPrime = input('-** WARNING **-\nOnly ONE Thread Will Be Used.\nThis Will Run Extremely Slow For Any Large Number\n(y/n): ')
        if ifPrime.lower() == 'y':
            print()
        else:
            exit()

    # ESTIMATES
    if useRawData == True:
        fT_ET = round((0.811 + 2.77E-08 * coinFlips + 7.4E-17 * coinFlips ** 2) * (10 / totalProcesses), 2)
        mb_ET = round(7.45E-06 * coinFlips + 1.61)
        isContinue = input(f'\n{coinFlips:,} Coin Flips:\n\tET Flip Time\t::\t{fT_ET}s\n\tET Write Time\t::\t{wT_ET}s\n\tET File Size\t::\t{mb_ET}mb\n\tConfirm (y/n)\t:: ')
    else:
        fT_ET = round((1.65E-08 * coinFlips + 0.531) * (10 / totalProcesses), 2)
        isContinue = input(f'\n{coinFlips:,} Coin Flips:\n\tET Flip Time\t::\t{fT_ET}s\n\tConfirm (y/n)\t:: ')

    if isContinue.lower() != 'y':
        exit()

    print(f'\nStarted Flipping {coinFlips:,} coins.\n')


    # FLIP COINS
    coinFlipTime = startTimer()

    if useRawData == True:
        with open(RAWDATAFILENAME, 'w') as raw:
            raw.write('')

        # totalRepeats = 1
        # tempCoinFlips = coinFlips
        # for _ in range(coinFlips % 1_000_000_000):
        #     tempCoinFlips -= 1_000_000_000
        #     totalRepeats += 1
        #     if tempCoinFlips <= 1_000_000_000:
        #         break

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(flipCoinsWithRawData, coinFlips//totalProcesses) for _ in range(totalProcesses)]
            for f in concurrent.futures.as_completed(results):
                tempList, tempHeads, tempTails = f.result()
                rawData += tempList
                totalHeads += tempHeads
                totalTails += tempTails

        exportTotalStats(FINALDATAFILENAME, coinFlips, totalHeads, totalTails)
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
        exportTotalStats(FINALDATAFILENAME, coinFlips, totalHeads, totalTails)
        print(endTimer('flipping coins', coinFlipTime))



    print('Process Complete, Press Enter to Close.')
    input()

    exit()

if __name__ == '__main__':
    main()
