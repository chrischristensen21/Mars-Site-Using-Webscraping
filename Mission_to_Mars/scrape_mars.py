from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    content_titles = soup.find_all('div', class_='content_title')
    news_title = content_titles[0].get_text()
    article_teaser_body = soup.find_all('div', class_='article_teaser_body')
    news_p = article_teaser_body[0].get_text()
  

    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    time.sleep(1)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_url = soup.find('img', class_='fancybox-image')['src']
    featured_image_url = url + "/" + img_url
    


    url = 'https://galaxyfacts-mars.com'
    mars_facts = pd.read_html(url)
    time.sleep(1)
    mars_facts_df = mars_facts[1]
    mars_facts_df = mars_facts_df.rename(columns={0: "Mars Facts Index", 1: "Mars Facts"})
    mars_html_table = mars_facts_df.to_html(index=False)
    mars_html_file =mars_facts_df.to_html("mars_facts.html", index=False)
    

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(1)
    hemisphere_image_urls = []
    hemi_link = 0

    for x in range(0, 4):
    
        browser.links.find_by_partial_text('Hemisphere Enhanced')[hemi_link].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h2', class_='title').get_text()
        img_find = soup.find('img', class_='wide-image')['src']
        img_url = url + img_find
        hemi_dict = {'title': title,'img_url': img_url}
        hemisphere_image_urls.append(hemi_dict)
        browser.back()
        hemi_link = hemi_link + 1

 # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_html_table": mars_html_table,
        "hemisphere_image_urls": hemisphere_image_urls}

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
