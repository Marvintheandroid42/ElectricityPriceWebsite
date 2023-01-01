
import requests
import matplotlib.pyplot as plt
import numpy as np
import sklearn as sk
import seaborn as sns
from sklearn.cluster import KMeans
from datetime import datetime, timedelta


def getDates(hist):
    dates = []

    for date in range(1, hist+1):
        dates.append(datetime.strftime(datetime.now() -
                     timedelta(date), '%Y-%m-%d').split("-"))

    return dates


def getData(dates):

    mat = []

    for j in dates:
        response = requests.get(
            f"https://mgrey.se/espot?format=json&date={int(j[0])}-{int(j[1])}-{int(j[2])}")
        d = response.json()
        avgSum = []
        for k in d["SE1"]:
            avgSum.append(k["price_sek"])
        mat.append(avgSum)

    return mat


def trainData(mat):

    X = np.array(mat).T
    Xmean = []
    y = []
    time = 1

    for i in X:
        i = list(i)
        for j in i:
            if j > np.mean(np.array(i))+(np.std(np.array(i))*3) or j < np.mean(np.array(i))-(np.std(np.array(i))*3):
                i.remove(j)
        i = np.array(i)
        Xmean.append(np.mean(i))
        y.append(time)
        time += 1

    return X, Xmean, y


def findCenters(Xmean):
    Xmean = np.array(Xmean).reshape(-1, 1)

    final = KMeans(n_clusters=3, random_state=0, max_iter=300)
    final.fit(Xmean)

    centers = np.sort(np.array(final.cluster_centers_).flatten())

    return centers


def classify(centers, price_sek):
    intervals = centers

    m = []

    for i in price_sek:
        if i <= intervals[0]:
            m.append(0)
        elif i > intervals[0] and i <= intervals[1]:
            m.append(1)
        elif i > intervals[1] and i <= intervals[2]:
            m.append(2)
        else:
            m.append(3)

    return m


def todayData():
    date = datetime.strftime(datetime.now(), '%Y-%m-%d').split("-")
    response = requests.get(
        f"https://mgrey.se/espot?format=json&date={date[0]}-{date[1]}-{date[2]}")
    d = response.json()

    hours = [i["hour"] for i in d["SE1"]]
    price_eur = [i["price_eur"] for i in d["SE1"]]
    price_sek = [i["price_sek"] for i in d["SE1"]]
    kmeans = [i["kmeans"] for i in d["SE1"]]

    return [hours, price_eur, price_sek, kmeans]
