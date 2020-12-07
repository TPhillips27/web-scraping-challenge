from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    #Find record of data from mongo database
    mars = mongo.db.listings.find_one()
    #REturn template and data
    return render_template("index.html", mars=mars)

#ROute that will trigger scrape function
@app.route("/scrape")
def scraper():
    #mars = mongo.db.mars
    #Run scrape function
    mars_data = scrape_mars.scrape()
    #Update mongo database using update and upsert
    mars.db.collection.update({}, mars_data, upsert=True)
    #Redirect to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

