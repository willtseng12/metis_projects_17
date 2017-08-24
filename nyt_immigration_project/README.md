## **Overview**

This is my fourth project at Metis data science bootcamp. This projects requires the use of unsupervsed learning and natural language processing technique on text data extacted either by scraping data from the web or APIs if available. It also requires us to familiarize ourselves with NoSql databases such as MongoDB. For this project, I decided to do my analysis on topic changes and evolution of New York Times articles related to immigration through time.

## **Data Source**

37 years of artciles data extract from the NYT articles api. Furthermore, I also web scraped the corresponding full articles 
from the NYT web page because the API only returned me a short abstract of the articles, which I thought was insuffficient for good topic modeling.

## **Goal**

To use NLP and unsupervised learning techniques on text data, clustering them into simialr subtopics and visualizing how their distributiton change through time.

## **Approach**

Please visit my [blog post](https://willtseng12.github.io/FourthBlog/) for more detailed information regarding this project's workflow and results.

## **File Descriptions**

`nyt_urls` contains the **first** set of urls where I used scrapy to pull the full articles from  
`nyt_urls_add` contains the **second** set of urls where I used scrapy to pull the full articles from
