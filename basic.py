import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
import time

globalStartTime = time.time()



date, bid, ask = np.loadtxt('GBPUSD1d.txt', unpack=True,
        delimiter = ',', converters={0:mdates.strpdate2num('%Y%m%d%H%M%S')})
avg           = ((bid+ask)/2)
patternAr     = []
performanceAr = []
patForRec     = []


def percentChange(start, curr):
    return (float(curr - start) / abs(start)) * 100.0

def getPatterns():
    global avg
    startTime =  time.time()
    x = len(avg)-30
    y = 11

    while y < x:
        pattern = []
        p1  = percentChange(avg[y-10], avg[y-9])
        p2  = percentChange(avg[y-10], avg[y-8])
        p3  = percentChange(avg[y-10], avg[y-7])
        p4  = percentChange(avg[y-10], avg[y-6])
        p5  = percentChange(avg[y-10], avg[y-5])
        p6  = percentChange(avg[y-10], avg[y-4])
        p7  = percentChange(avg[y-10], avg[y-3])
        p8  = percentChange(avg[y-10], avg[y-2])
        p9  = percentChange(avg[y-10], avg[y-1])
        p10 = percentChange(avg[y-10], avg[y])

        outcome = avg[y+20:y+30]
        curr    = avg[y]
        try:
            avgOutcome = (sum(outcome)/len(outcome))
        except Exception as e:
            print(str(e))
            avgOutcome = 0

        futureOutcome = percentChange(curr, avgOutcome)
        pattern.append(p1)
        pattern.append(p2)
        pattern.append(p3)
        pattern.append(p4)
        pattern.append(p5)
        pattern.append(p6)
        pattern.append(p7)
        pattern.append(p8)
        pattern.append(p9)
        pattern.append(p10)

        patternAr.append(pattern)
        performanceAr.append(futureOutcome)

        y += 1
    endTime = time.time()
    print(len(patternAr))
    print(len(performanceAr))
    avg = ((bid+ask)/2)
    print('Pattern storage:', endTime-startTime, ' seconds')


def currentPattern():
    global patForRec

    cp1       = percentChange(avg[-11], avg[-10])
    cp2       = percentChange(avg[-11], avg[-9])
    cp3       = percentChange(avg[-11], avg[-8])
    cp4       = percentChange(avg[-11], avg[-7])
    cp5       = percentChange(avg[-11], avg[-6])
    cp6       = percentChange(avg[-11], avg[-5])
    cp7       = percentChange(avg[-11], avg[-4])
    cp8       = percentChange(avg[-11], avg[-3])
    cp9       = percentChange(avg[-11], avg[-2])
    cp10       = percentChange(avg[-11], avg[-1])

    patForRec.append(cp1)
    patForRec.append(cp2)
    patForRec.append(cp3)
    patForRec.append(cp4)
    patForRec.append(cp5)
    patForRec.append(cp6)
    patForRec.append(cp7)
    patForRec.append(cp8)
    patForRec.append(cp9)
    patForRec.append(cp10)

    print(patForRec)


def patternRec():
    for pattern in patternAr:
        currentSim = [0] * 10
        currentSim[0]   = 100.00 - abs(percentChange(pattern[0], patForRec[0]))
        currentSim[1]   = 100.00 - abs(percentChange(pattern[1], patForRec[1]))
        currentSim[2]   = 100.00 - abs(percentChange(pattern[2], patForRec[2]))
        currentSim[3]   = 100.00 - abs(percentChange(pattern[3], patForRec[3]))
        currentSim[4]   = 100.00 - abs(percentChange(pattern[4], patForRec[4]))
        currentSim[5]   = 100.00 - abs(percentChange(pattern[5], patForRec[5]))
        currentSim[6]   = 100.00 - abs(percentChange(pattern[6], patForRec[6]))
        currentSim[7]   = 100.00 - abs(percentChange(pattern[7], patForRec[7]))
        currentSim[8]   = 100.00 - abs(percentChange(pattern[8], patForRec[8]))
        currentSim[9]   = 100.00 - abs(percentChange(pattern[9], patForRec[9]))

        overallSim = sum(currentSim)/10.00

        if overallSim > 70:
            idx = patternAr.index(pattern)
            print('####################')
            print(patForRec)
            print('===================')
            print('predicted outcome: ', performanceAr[idx])

            xp = range(1,11)
            fig = plt.figure()
            plt.plot(xp, patForRec)
            plt.plot(xp, pattern)
            plt.show()
            print('===================')
            print(pattern)
            print('####################')



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



getPatterns()
currentPattern()
patternRec()



totalTime = time.time() - globalStartTime


print('Entire processing time: ', totalTime, ' seconds')
