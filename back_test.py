#!/usr/bin/python2

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
import time
import sys

globalStartTime = time.time()

date, bid, ask = np.loadtxt('GBPUSD1d.txt', unpack=True,
            delimiter = ',', converters={0:mdates.strpdate2num('%Y%m%d%H%M%S')})
allData = ((bid+ask)/2)

def percentChange(start, curr):
    try:
       x = (float(curr - start) / abs(start)) * 100.0
       if x==0:
           return 0.0000000001
       else:
           return x
    except Exception as e:
        return 0.000000001

def getPatterns(levels):
    global avg
    print('LENGTH', len(avg))
    startTime =  time.time()
    x = len(avg)-30-levels # trace here
    y = 1 + levels
    # Alternative model is to try reversed percentChange "end to start" and benchmark
    # custom weights for older patterns
    # opportunity vs accuracy
    while y < x:
        pattern = [0] * levels
        for level in list(reversed(range(levels))):
            pattern[levels-level-1]  = percentChange(avg[y-levels], avg[y-level])

        outcome = avg[y+20:y+30]
        curr    = avg[y]
        try:
            avgOutcome = (sum(outcome)/len(outcome))
        except Exception as e:
            print(str(e))
            avgOutcome = 0

        futureOutcome = percentChange(curr, avgOutcome)
        patternAr.append(pattern)
        performanceAr.append(futureOutcome)

        y += 1
    endTime = time.time()
    print(len(patternAr))
    print(len(performanceAr))
    print('Pattern storage:', endTime-startTime, ' seconds')


def currentPattern(levels):
    global patForRec
    patForRec = [0] * levels

    for level in list(reversed(range(levels))):
        patForRec[levels-level-1]       = percentChange(avg[-1-levels], avg[-1-level])

    print(patForRec)


def patternRec(levels):
    foundMatch = False
    plots = []
    predictedOutcomes = []

    for pattern in patternAr:
        currentSim = [0] * levels
        for level in range(levels):
            currentSim[level]   = 100.00 - abs(percentChange(pattern[level], patForRec[level]))
            overallSim = sum(currentSim)/float(levels)

            if overallSim > 70:
                idx = patternAr.index(pattern)
                foundMatch = True
                """print('####################')
                print(patForRec)
                print('===================')
                print('predicted outcome: ', performanceAr[idx])"""

                plots.append(pattern)

                """fig = plt.figure()
                plt.plot(xp, patForRec)
                plt.plot(xp, pattern)
                plt.show()"""
                """print('===================')
                print(pattern)
                print('####################')"""

    predArray = []
    if foundMatch:
        xp = range(1, levels+1)
        #fig = plt.figure(figsize=(10,6))
        for plot in plots:
            futureIdx = patternAr.index(plot)

            if performanceAr[futureIdx] > patForRec[levels-1]:
                pcolor = '#24bc00'
                predArray.append(1.00)
            else:
                pcolor = '#d40000'
                predArray.append(-1.00)

        #   plt.plot(xp, plot)
            predictedOutcomes.append(performanceAr[futureIdx])
        #  plt.scatter(35, performanceAr[futureIdx],c=pcolor, alpha=.3 )


        realOutcomeRange         = allData[toLimit+20:toLimit+30]
        realOutcomeAverage       = sum(realOutcomeRange)/len(realOutcomeRange)
        predictedOutcomesAverage = sum(predictedOutcomes)/len(predictedOutcomes)

        realMovement       = percentChange(allData[toLimit], realOutcomeAverage)


        print(predArray)
        predAvg = sum(predArray)/len(predArray)
        print(predAvg)

        if predAvg < 0:
            print('drop predicted')
            print(patForRec[levels-1])
            print(realMovement)
            if realMovement < patForRec[levels-1]:
                accuracy.append(100)
            else: accuracy.append(0)
        elif predAvg > 0:
            print('rise predicted')
            print(patForRec[levels-1])
            print(realMovement)
            if realMovement > patForRec[levels-1]:
                accuracy.append(100)
            else: accuracy.append(0)

        #plt.scatter(40, realMovement, c='#54fff7', s=25)
        #plt.scatter(40, predictedOutcomesAverage, c='b', s=25)

        #plt.plot(xp, patForRec,'#54fff7', linewidth=3 )
        #plt.grid(True)
        #plt.title('Matching patterns')
        #plt.show()




def graphRaw():
    fig = plt.figure(figsize=(10,7))
    axl = plt.subplot2grid((40,40),(0,0), rowspan=40, colspan=40)
    axl.plot(date, bid)
    axl.plot(date, ask)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)

    axl.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    for label in axl.xaxis.get_ticklabels():
        label.set_rotation(45)

    axl_2 = axl.twinx()
    axl_2.fill_between(date, 0, (ask-bid), facecolor='g', alpha=.3)
    plt.subplots_adjust(bottom=.23)

    plt.grid(True)
    plt.show()

dataLength = int(bid.shape[0])

print('data length is', dataLength)

toLimit = 37000
levels  = 10
try:
    levels = int(sys.argv[1])
except Exception as e:
    print('Falling back to default length 10')

print('Pattern level', levels)
accuracy = []
samps = 0


while toLimit < dataLength:
    avg           = allData[:toLimit]
    patternAr     = []
    performanceAr = []
    patForRec     = []
    getPatterns(levels)
    currentPattern(levels)
    patternRec(levels)
    toLimit += 1
    samps += 1
    totalTime = time.time() - globalStartTime
    accuracyAvg = sum(accuracy)/len(accuracy)
    print('Backtested Accuracy is ' + str(accuracyAvg)+'% after '+ str(samps)+' samples')
    print('Entire processing time: ', totalTime, ' seconds')

    #moveOn = raw_input('press ENTER to continue...')
