import requests
import sklearn as sk
from datetime import datetime as dt
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import mlPipeline
import os
from datetime import datetime, timedelta
import seaborn as sns
import pandas as pd


def currentPrice():

    response = requests.get(f"https://mgrey.se/espot?format=json")
    d = response.json()

    count = 0

    for i in range(1, len(d)):

        count += d[list(d.keys())[i]][0]["price_sek"]

    return count/(len(d)-1)


def classify(currentPrice):
    X, Xmean, y = mlPipeline.trainData(
        mlPipeline.getData(mlPipeline.getDates(5)))

    centers = mlPipeline.findCenters(Xmean)

    preds = mlPipeline.classify(centers, currentPrice)

    print(preds)
    if preds[0] == 0:
        return "Extremely low"

    if preds[0] == 1:
        return "Lower than average"

    if preds[0] == 2:
        return "Higher than average"
    
    if preds[0] == 3:
        return "Extremely High"


def todayPricePlot():
    today = mlPipeline.todayData()

    X, Xmean, y = mlPipeline.trainData(
        mlPipeline.getData(mlPipeline.getDates(5)))

    centers = mlPipeline.findCenters(Xmean)

    preds = np.array(mlPipeline.classify(centers, today[2]))

    response = requests.get(f"https://mgrey.se/espot?format=json")
    d = response.json()

    plt.style.use("seaborn-darkgrid")
    plt.plot(today[0], today[2], marker="x",
             linewidth=1, color="steelblue", alpha=0.75)
    plt.scatter(x=np.array(today[0])[np.where(preds == 0)], y=np.array(
        today[2])[np.where(preds == 0)], marker="o", color="green")
    plt.scatter(x=np.array(today[0])[np.where(preds == 2)], y=np.array(
        today[2])[np.where(preds == 2)], marker="o", color="red")
    plt.xlabel("Hour")
    plt.ylabel("Price in öre")

    path = r"static"
    os.remove(path + r"\todayPricePlot.png")
    plt.savefig(path + r"\todayPricePlot.png")


def monthsCandelstick():
    data = []
    today = datetime.now()

    listVar = []
    mat = []

    for monthD in range(1, 61):
        if monthD % 20 == 0:
            mat.append(listVar)
            listVar = []
        date = datetime.strftime(
            (today - timedelta(monthD)), '%Y-%m-%d').split("-")
        response = requests.get(
            f"https://mgrey.se/espot?format=json&date={date[0]}-{date[1]}-{date[2]}")
        d = response.json()
        for i in d["SE1"]:
            listVar.append(float(i["price_sek"]))

    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111)
    plt.style.use("seaborn-darkgrid")
    plt.boxplot(mat, notch=True, )

    ax.set_xticklabels(['20 Days', '40 Days',
                        '60 Days'])

    plt.ylabel("Price in öre")

    path = r"static"
    try:
        os.remove(path + r"\monthCandlestick.png")
    except:
        pass
    plt.savefig(path + r"\monthCandlestick.png")


def comparisonPlot():
    today = mlPipeline.todayData()

    X, Xmean, y = mlPipeline.trainData(
        mlPipeline.getData(mlPipeline.getDates(5)))

    plt.style.use("seaborn-darkgrid")
    plt.plot(today[0], today[2], color="steelblue", label="Today's Prices")
    plt.plot(today[0], Xmean, color="red", label="5 Day Average Price")
    plt.xlabel(" Hours ")
    plt.ylabel(" Price in Öre")
    plt.legend()

    path = r"static"
    try:
        os.remove(path + r"\comparisonPlot.png")
    except:
        pass
    plt.savefig(path + r"\comparisonPlot.png")

# Should also plot the predictions and k means for the day?, do all the different electricity streams SE1,2,3,4
