from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt
import time

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_p = mars_news(browser)
    
    # Run all scraping functions and store results in a dictionary
    listings = {
        "news_title": news_title,
        "news_p": news_p,
        "image_link_url": find_image(browser),
        "mars_table": mars_table(),
        "hemi_dict": hemispheres(browser),
        #"last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return listings

def mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")
    time.sleep(5)

    #Attribute Error error handling
    try:
        news_title = soup.find("div", class_="bottom_gradient").get_text()
        news_p = soup.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

    
def find_image(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser('chrome', **executable_path)
    browser.visit(url)
    time.sleep(5)
    browser.click_link_by_id("full_image")
    time.sleep(5)
    soup = bs(browser.html,'html.parser')
    data = soup.find("img", class_="fancybox-image")
    image_link = data["src"]
    image_link_url = f"https://www.jpl.nasa.gov/{image_link}"

    return image_link_url

def mars_table():
    marstable_df = pd.read_html('http://space-facts.com/mars/')[0]
    marstable_df.columns=['Description', 'Mars']
    marstable_df.set_index('Description', inplace=True)  
    mars_table = marstable_df.to_html()  

    return mars_table

def hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)  
    #create empty list for hemisphere image urls
    hemisphere_image_urls = []

    html = browser.html
    soup = bs(html, "html.parser")

    #get the urls
    hemisphere = soup.find_all("div", class_="item")
    hemisphere

    for i in hemisphere:
        title = i.find('h3').text
        url = i.find('a', class_ = "itemLink product-item")["href"]
        img_url = "https://astrogeology.usgs.gov" + url
        browser.visit(img_url) 
        html = browser.html
        soup = bs(html, "html.parser")
        downloads= soup.find('div', class_ = "downloads")
        full_img_url =downloads.find('a')['href']
    

        hem_dict = {"title": title, "url":full_img_url }
        hemisphere_image_urls.append(hem_dict)

    return hemisphere_image_urls

# def scrape():
#     #browser = init_browser()
#     listings = {'news_title': "NASA's Ingenuity Mars Helicopter Recharges Its Batteries in Flight",
#  'news_p': 'Headed to the Red Planet with the Perseverance rover, the pioneering helicopter is powered up for the first time in interplanetary space as part of a systems check.',
#  'image_link_url': 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA22893_ip.jpg', 'mars_table': '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>Mars</th>\n    </tr>\n    <tr>\n      <th>Description</th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>Equatorial Diameter:</th>\n      <td>6,792 km</td>\n    </tr>\n    <tr>\n      <th>Polar Diameter:</th>\n      <td>6,752 km</td>\n    </tr>\n    <tr>\n      <th>Mass:</th>\n      <td>6.39 × 10^23 kg (0.11 Earths)</td>\n    </tr>\n    <tr>\n      <th>Moons:</th>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <th>Orbit Distance:</th>\n      <td>227,943,824 km (1.38 AU)</td>\n    </tr>\n    <tr>\n      <th>Orbit Period:</th>\n      <td>687 days (1.9 years)</td>\n    </tr>\n    <tr>\n      <th>Surface Temperature:</th>\n      <td>-87 to -5 °C</td>\n    </tr>\n    <tr>\n      <th>First Record:</th>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <th>Recorded By:</th>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>',
#  'hemi_dict': [{'title': 'Cerberus Hemisphere Enhanced',
#    'url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},
#   {'title': 'Schiaparelli Hemisphere Enhanced',
#    'url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},
#   {'title': 'Syrtis Major Hemisphere Enhanced',
#    'url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'},
#   {'title': 'Valles Marineris Hemisphere Enhanced',
#    'url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]}

 

    # url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # browser = Browser('chrome', **executable_path)
    # browser.visit(url)
    # time.sleep(5)
    # browser.click_link_by_id("full_image")
    # time.sleep(5)
    # soup = bs(browser.html,'html.parser')
    # data = soup.find("img", class_="fancybox-image")
    # image_link = data["src"] 
    # listings["image_link_url"] = f"https://www.jpl.nasa.gov/spaceimages{image_link}"   

    




