import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np


def graphRaw(path):
    date, bid, ask = np.loadtxt(path, unpack=True,
            delimiter = ',', converters={0:mdates.strpdate2num('%Y%m%d%H%M%S')})
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
