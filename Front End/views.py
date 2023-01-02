from flask import Blueprint, render_template
from scrape import currentPrice
import requests
import scrape

views = Blueprint(__name__, "views")


@views.route("/")
def home():
    scrape.todayPricePlot()
    scrape.comparisonPlot()
    scrape.monthsCandelstick()
    return render_template("home.html", price=round(currentPrice(), 2), catagory=scrape.classify([int(currentPrice())]))
