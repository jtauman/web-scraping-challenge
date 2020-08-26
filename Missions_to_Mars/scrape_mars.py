from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    #########################
    #    get latest news    #
    #########################

    #visit mars.nasa.gov/news/ website
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(1)

    # Scrape page into Soup
    html= browser.html
    soup=bs(html, 'html.parser')

    #find information for the latest news item
    news = soup.find('div', class_="list_text")
    news_title = news.find('a').text
    news_p = news.find('div', class_="article_teaser_body").text

    #print results
    print("------")
    print(news_title)
    print(news_p)
    print("------")

    #########################
    #  get featured image   #
    #########################

    #visit www.jpl.nasa.gov/spaceimages/?search=&category=Mars website
    featured_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_url)
    time.sleep(1)

    #move through webpages to get to full resolution image
    browser.click_link_by_id('full_image')
    browser.links.find_by_partial_text('more info').click()
    browser.links.find_by_partial_text('jpg').click()

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    #get link for full resolution image
    featured_image = soup.find('img')['src']

    #print results
    print("------")
    print(featured_image)
    print("------")


    #########################
    # get mars facts table  #
    #########################

    #visit space-facts.com/mars/ website and get table
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)[0]
    facts_df=tables.rename(columns={0:"Parameter", 1:"Mars"})

    #convert to html table string
    mars_table = facts_df.to_html(index=False, justify='center', classes="table-striped")
    mars_table = mars_table.replace('\n', '')

    #print results
    print("------")
    print(mars_table)
    print("------")


    #########################
    # get hemisphere images #
    #########################

    #visit website
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    #scrape for hemisphere image names
    hemispheres = soup.find_all("div", class_="item")
    hemisphere_names = []

    #loop through hemisphere image names and append to list
    for hemisphere in hemispheres:
        hemisphere_title = hemisphere.find('h3').text
        hemisphere_names.append(hemisphere_title)

    #set empty list for urls
    hemisphere_urls = []

    #loop through names to get individual titles and urls, then save to dictionary
    for name in hemisphere_names:
        
        try:
            #use splinter to click on enhanced link
            browser.links.find_by_partial_text(name).click()
            
            #scrape page into bs
            html = browser.html
            soup = bs(html, 'html.parser')
            
            title=soup.find('div', class_='container').find('h2', class_='title').text
            url=soup.find('div', class_='container').find('div', class_='downloads').find('a')['href']
            
            # print data
            print('-----------------')
            print(title)
            print(url)

            # add data to dctionary
            hemisphere_dictionary = ({"title": title, "url": url})
            
            #add dictionary to list
            hemisphere_urls.append(hemisphere_dictionary)

            # go back after scraping
            browser.back()
        except Exception as e:
            print(e)

    #print results
    print("------")
    print(hemisphere_urls)
    print("------")

    # Store data in a dictionary
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image,
        "mars_table": mars_table,
        "hemispheres": hemisphere_urls  
    }

    # Quite the browser after scraping
    browser.quit()

    # Return results
    return mars_dict