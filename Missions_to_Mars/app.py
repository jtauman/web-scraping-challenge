from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection to the mars_app db
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_dict = mongo.db.mars_dict.find_one()

    # Return template and data
    return render_template("index.html", mars_dict=mars_dict)

#route to render scrape function to update mongo db with scraped items
@app.route("/scrape")
def scraper():
    #assign dictionary to mongo collection
    mars_dict = mongo.db.mars_dict
    #call scrape function to get data
    mars_data = scrape_mars.scrape()
    #update mongo collection
    mars_dict.update({}, mars_data, upsert=True)

    #return to home
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)