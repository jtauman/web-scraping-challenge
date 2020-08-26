# web-scraping-challenge


## Assignment: Build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

Located within the Mission_to_Mars folder, the Jupyter notebook entitled, *mission_to_mars.ipynb*, includes the code for scraping 4 different websites related to the Mission to Mars, including the latest news article, the featured image from NASA's Mars website, information about mars and images of the 4 Martian hemispheres.


To generate and display the scraped information onto a single HTML page, *scrape_mars.py* was made which includes the scraping code from *mission_to_mars.ipynb* as a function, which is called by *app.py*, the program the generates the web page.  The code for the html page, *index.html* is located in the templates folder.

Running *app.py* will create a single html page, mission_to_mars.  Clicking on the button will result in the scrape function to be used to: scrape the different web-pages, store the data in a MongoDB database(mars_app), and return the data elements to the html page.
