# Algo Software
## INTRODUCTION
This is basically a software which is related to somewhere like algo trading software. But in this software, the user only has to enter the enter company name and then it displays all the technical analysis of that company's stock data. and also give notifications for buying and selling according to the software strategy.   
## PROBLEM FACING
1. While manual trading sometimes due to a lack of speed buying and selling will not be so accurate.
2. Time wasting in technical analysis.
## SOLUTIONS
1. By doing analysis with the help of code.
2. Algo trading.
## STEPS 
1. Getting live data from the website:
We use requests.get() for fetching data and there is a use of header because without these headers the request will just time out.
3. Converting data from one type to another type:
Convert the data in list
4. making a soup:
To parse a document, pass it into the BeautifulSoup constructor. You can pass in a string or an open filehandle:
6. Saving data in any server.
7. Showing all technical indicators.
8. Showing the result of the strategy
9. Performing tasks according to the strategy.
## LIBRARIES REQUIRED
1. BeautifulSoup
2. Selenium
3. third-party HTTP library for python-requests
4. Parser(which can create a nested/tree structure of the HTML data like html5lib.)
html5lib is very slow but python dependent.
lxml’s HTML parser & lxml’s XML parser both are very fast but external c dependent.
If you can, I recommend you install and use lxml for speed. If you’re using a version of Python 2 earlier than 2.7.3, or a version of Python 3 earlier than 3.2.2, it’s essential that you install lxml or html5lib–Python’s built-in HTML parser is just not very good in older versions.
## Web Scraping
Getting live data from a website.
### Different ways for web scraping
1. Off-the-shelf web scrapers (including low/no code web scrapers)
2. Cloud web scrapers
3. Browser extensions web scrapers
### Off-the-shelf web scrapers
1. Beautiful Soup.
2. Requests.
3. Scrapy.
4. Selenium.
5. Playwright.
6. Lxml.
7. Urllib3.
8. MechanicalSoup.
### Cloud web scrapers
1. Scrapestack
2. Bright Data
3. Oxylabs
4. Abstract API
5. ScraperAPI
6. ScrapingBee
7. Geekflare
8. Apify
9. Web Scraper
10. Mozenda
11. Octoparse
12. ParseHub
13. Diffbot
### Browser extensions web scrapers
1. Instant Data Scraper
2. Web Scraper
3. Data Miner
4. Scraper
5. Agenty
6. Simplescraper
### Best python libraries for web scraping
1. BeautifulSoup
#### Features:
a. It supports for encoding detection.
b. This is built of Ixml and html5lib. We can do work accordingly.
#### Cons:
a. Use of proxies is not  simple, We can't download large amount of data from same site without having IP blacklisted.
b. It requires some dependencies.
2. Scrapy
a. It can perform data monitoring, automated testing and data mining.
b. provides a Telnet console through which you can connect to a Python terminal inside your Scrapy process to monitor and debug your crawler.
c. built-in support for creating feed exports in various file types (JSON, CSV, and XML) and storing them in multiple backends (FTP, S3, local filesystem).
d. support for extensibility lets you add your features using signals and a simple API 
e. It does not work well with javaScript-based websites.
3. Selenium
a. Selenium is a free and open-source web driver
b.  It works efficiently on JavaScript-rendered web pages.
c. The most common approach to integrating Selenium with Python is through APIs.
d. Form submission, automatic login, data adding/deletion, and alert handling are some typical Selenium use cases for web scraping.
e. JavaScript-based traffic-tracking systems (like Google Analytics) will quickly identify you using Webdriver to browse many pages
f. security issue.
4. Requests
a. It supports the restful API and its functionalities (PUT, GET, DELETE, and POST) and offers extensive documentation.
b. It cannot handle dynamic websites that comprise mostly JavaScript code or parse HTML.
5. Urllib3
a. Developers can access and parse data from protocols like HTTP and FTP
6. Lxml
a. data manupulating is faster and more efficient
7. MechanicalSoup
a. JavaScript is not compatible with Mechanical Soup
## HARDWARE REQUIRED
## SOFTWARE REQUIRED
## PYTHON MODULE REQUIRED
## SOURCE CODE
## what required
1. header for NSE to respond
2. 

