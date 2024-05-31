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


