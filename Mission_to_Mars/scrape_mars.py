from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


#browser set up#
def init_browser():
    # executable_path = {'executable_path': 'chromedriver'}
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape_info():

    # scrapping news titles and paragraphs#
    browser = init_browser()
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    all_text = soup.find_all('div', class_='list_text')

    for item in all_text:
        news_title = item.find('div', class_='content_title').text
        news_p = item.find('div', class_='article_teaser_body').text

    #scrapping image#
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    image = soup.find('img', class_='headerimage')
    image_url = image['src']
    featured_image_url = url+image_url

    #scrapping table of Mars Facts#
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    df = tables[0]
    df.rename(columns={0: 'Mars - Earth Comparison',
                       1: 'Mars',
                       2: 'Earth'}, inplace=True)

    df = df.iloc[1:, :]
    df.set_index('Mars - Earth Comparison', inplace=True)
    html_table = df.to_html()
    html_table.replace('\n', '')

    #scrapping hemisphere image and title#
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    hemisphere_image_urls = []

    results = soup.find_all('div', class_='description')

    for result in results:
        try:
            link = result.find('a')
            title = link.text

            # setting up new page link for image"
            newpage_link = url+link['href']
            browser.visit(newpage_link)
            html = browser.html
            soup = bs(html, 'html.parser')

            # div=soup.find('div',id='wide-image')
            img = soup.find('img', class_='wide-image')
            src = img['src']
            img_url = url+src

            if (title and img_url):
                # printing results"
                print('-'*50)
                print(title)
                print(img_url)

            # creating dictionary"

                hem_dict = {'title': title,
                            'img_url': img_url}

                hemisphere_image_urls.append(hem_dict)

        except Exception as e:

            print(e)

    browser.quit()

    # Create dictionary for all info scraped from sources above
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": html_table,
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict
