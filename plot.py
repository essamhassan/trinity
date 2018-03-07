import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
import time

date, bid, ask = np.loadtxt('GBPUSD1d.txt', unpack=True,
        delimiter = ',', converters={0:mdates.strpdate2num('%Y%m%d%H%M%S')})

patternAr     = []
performanceAr = []

def percentChange(start, curr):
    return (float(curr - start) / abs(start)) * 100.0

def getPatterns():
    startTime =  time.time()
    avg = ((bid+ask)/2)
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
    print('Pattern storage:', endTime-startTime, ' seconds')
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
