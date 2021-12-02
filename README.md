# **ASOS-webscraping-project**
## **What our project does**

This project was designed to scrape information and images from products on the asos.com website.
By deafault the scraper will scrape from the whole website, however there is a configurable yaml file to make the scraping targets more precise.
The scraped images and data will be in .jpg and .json formats respectively. <br /> <br />

## **Motivation**

ASOS do not provide an API for their website. Therefore the most time and labor efficient way to access large amounts of data on the website requires the use of a scraper.
 <br /> <br />

## **How to use it**
If running the ASOS_Scraper.py file in a code editor you can edit the config.yaml beforehand to run the scraper in the desired way.
If running from a local or AWS EC2 instance terminal you can either:<br />
    - Run `nano config.yaml` to edit the configuration before running `ASOS_Scraper.py`.<br />
    - Pull and then run the docker image directly from Dockerhub<br />&nbsp;&nbsp;&nbsp;&nbsp;
        `docker pull asos_scraper` <br />&nbsp;&nbsp;&nbsp;&nbsp;
        `docker run -it asos_scraper` 
 <br /> <br />
### **Configuration**
The following parameters require arguments within the config.yaml file:
 


Parameters |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Arguments&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Usage |
--- | :---: | --- |
DRIVER |**Chrome** *or* **Remote**|  - **Chrome** will run the scraper displaying the graphical interface<br />- **Remote** will run the scraper on  selenium standalone:<br />&nbsp;&nbsp;&nbsp;&nbsp;- This requires ```docker pull selenium/standalone-chrome``` to pull the selenium/standalone image from Dockerhub<br />&nbsp;&nbsp;&nbsp;&nbsp;- Then `docker run -d -p 4444:4444 --shm-size="2g" selenium/standalone-chrome:4.1.0-20211123`<br /><br />- Please see the selenium/standalone README here https://github.com/SeleniumHQ/docker-selenium for further help if requried!
MEN |**True** *or* **False** |If you want to scrape from the Men's categories
WOMEN |**True** *or* **False**|If you want to scrape from the Women's categories
LOCAL |**True** *or* **False**|If you want save the data on the local machine
S3_BUCKET |**True** *or* **False**| If you want save the data on AWS S3 Bucket cloud storage
BUCKET_NAME |<*Enter your bucket name here*> |Visit https://s3.console.aws.amazon.com/s3/ to create a bucket if not done already
PRODUCTS_PER_CATEGORY |**all** *or* **integer**|**all** will scrape every product from categories selected <br />**integer** will scrape required number of products from each category<br />The ASOS website displays 72 products per page<br />For **all** or if the **integer** given is greater than 72 the scraper will visit the required number of pages to get specified number of products
SAVE_IMAGES |**True** *or* **False** |If you want to scrape images from the website
SAVE_JSON |**True** *or* **False** |If you want to scrape alphanumeric data from the website
OPTIONS_MEN |**New in<br />Clothing<br />Shoes<br />Accessories<br />Topman<br />Sportswear<br />Face + Body**|Requires a list of categories, delete or comment out lines to select the options
OPTIONS_WOMEN |**New in<br />Clothing<br />Shoes<br />Accessories<br />Topshop<br />Sportswear<br />Face + Body**|Requires a list of categories, delete or comment out lines to select the options



### config.yaml
```
DRIVER: Chrome or Remote
MEN: True 
WOMEN: True
LOCAL: True
S3_BUCKET: True
BUCKET_NAME: <Enter your bucket name here>
PRODUCTS_PER_CATEGORY: integer or all
SAVE_IMAGES: True
SAVE_JSON: True 
OPTIONS_MEN:
        - New in
        - Clothing
        - Shoes
        - Accessories
        - Topman
        - Sportswear
        - Face + Body
OPTIONS_WOMEN:
        - New in
        - Clothing
        - Shoes
        - Accessories
        - Topshop
        - Sportswear
        - Face + Body
```
 <br /> 

## **Current Status**
The scraper has successfully collected alphanumeric and image data for over 1000 product samples from the website and saved these to our own S3 Bucket
## **Roadmap**
-Add functionality to stop repeated data collection on subsequent reruns
<br >-Connect data to PostgreSQL database using psycopg
<br >-Use CLI tags to make choosing configuration options more user friendly
<br >-Use Grafana to monitor resource usage on CPU and/or EC2
<br >
