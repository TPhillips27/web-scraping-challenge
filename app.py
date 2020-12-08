from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
# mongo = PyMongo(app)


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    #Find record of data from mongo database
    mars = mongo.db.collection.find_one()
    #Return template and data
    return render_template("index.html", mars=mars)

#ROute that will trigger scrape function
@app.route("/scrape")
def scraper():
    
    #Run scrape function
    mars_data = scrape_mars.scrape()
    #Update mongo database using update and upsert
    mongo.db.collection.update({}, mars_data, upsert=True)
    #Redirect to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

