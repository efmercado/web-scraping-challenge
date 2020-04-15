# Importing Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import time

# Initializing browser
def init_browser():
	executable_path = {'executable_path':"/usr/local/bin/chromedriver"}
	return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict ={}
    
    # Mars news URL of page to be scrapped
    news_url = 'https://mars.nasa.gov/news/'
    # Requesting data files from the news page
    page = requests.get(news_url)
    # Using BeautifulSoup to parse the html data/files
    news_soup = BeautifulSoup(page.content, 'html.parser')
    # Retrieving the latest news title and paragraph
    news_title = news_soup.find_all('div', class_='content_title')[0].get_text()
    news_p = news_soup.find_all('div', class_='rollover_description_inner')[0].get_text()
    print(news_title.replace('\n',''))
    print('-'*90)
    print(news_p.replace('\n',''))
    print(browser)

    # Jet propulsion laboratory (JPL) URL
    jpl_nasa_url = "https://www.jpl.nasa.gov"
    # Mars' featured image to be scraped
    jpl_images_url ="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # Using spliter to navigate and download the site
    browser.visit(jpl_images_url)
    html = browser.html
    # Using BeautifulSoup to parse the html page
    jpl_images_soup = BeautifulSoup(html, 'html.parser')
    # Retrieving featured Mars image link
    image_path = jpl_images_soup.find_all('img')[3]['src']
    featured_image_url = jpl_nasa_url + image_path
    print(featured_image_url)
    
    # Mars weather twitter page to be scrapped
    mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'
    # Requesting data files from the twitter page
    page = requests.get(mars_twitter_url)
    # Using BeautifulSoup to parse the html data/files
    mars_weather_soup = BeautifulSoup(page.content,'html.parser')
    # Retrieving the latest Mars weather update tweet
    weather_span = mars_weather_soup.find_all('p', class_='TweetTextSize')[0].get_text()
    # Assigning tweet to mars_weather variable
    mars_weather = weather_span
    print(mars_weather)
    
    
  # Mars facts to be scraped
    mars_facts_url = 'https://space-facts.com/mars/'
    # Using Pandas to scrape the table containing Mars' facts
    mars_html = pd.read_html(mars_facts_url)[0]
    # Renaming columns
    mars_html = mars_html.rename(columns = {0:'Description', 1:'Value'}).set_index('Description')
    print(mars_html)
    # Converting the data to an HTML table string
    mars_table_html =  mars_html.to_html()
    print(mars_table_html)
    
    # USGS Astrology site
    usgs_url = 'https://astrogeology.usgs.gov'

    # Mars hemispheres page to be scraped
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # Using spliter to navigate and download the site
    browser.visit(hemispheres_url)
    hemisphere_html = browser.html
    # Using BeautifulSoup to parse the html page
    hemispheres_soup = BeautifulSoup(hemisphere_html, 'html.parser')

    # Navigating to the HTML element that contains the descriptive page data
    hemispheres_page_description = hemispheres_soup.find_all('div', class_='description')
    # Blank list that will be populated with the image URLs
    hemisphere_image_urls = []
    # For loop that will navigate the HTML element and retrieve the necessary data
    for link in hemispheres_page_description:
    
        # Hemisphere title
        hemisphere_title = link.h3.text
        # Using splinter to navigate new page
        browser.visit(usgs_url + link.a['href'])
        # Downloading/requesting/parsing HTML files
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')
        # Pulling the image URL
        image_link = image_soup.find('div', class_='downloads').li.a['href']
        # Saving the image title and URL into a dictionary
        image_dictionary = {}
        image_dictionary['title'] = hemisphere_title
        image_dictionary['img_url'] = image_link
        # Appending to list
        hemisphere_image_urls.append(image_dictionary)
        
    print(hemisphere_image_urls)
    
    # Dictionary of all the data collected
    mars_dict = {
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "mars_weather": mars_weather,
            "fact_table": str(mars_table_html),
            "hemisphere_images": hemisphere_image_urls
            }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict
