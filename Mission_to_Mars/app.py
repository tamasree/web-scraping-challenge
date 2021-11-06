from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db
collection = db.mars_details


# Route to render index.html template using data from Mongo


@app.route("/")
def home():
    scrape()

    # Find one record of data from the mongo database
    destination_data = collection.find_one()

    print(destination_data)

    # Return template and data
    return render_template("index.html", destination_data=destination_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database
    collection.drop()
    collection.insert_one(mars_data)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
