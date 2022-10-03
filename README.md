# **ASOS-webscraping-project**
## **What this project does**

This project was designed to scrape information and images from products on the asos.com website.
By deafault the scraper will scrape from the whole website, however there is a configurable yaml file and CLI flags to make the scraping targets more precise.
The scraped images and data will be in .jpg and .json formats respectively. <br /> <br />

## **Motivation**

ASOS do not provide an API for their website. Therefore the most time and labor efficient way to access large amounts of data on the website requires the use of a scraper. 
 <br /> <br />

## **How to use**
The default settings can be changed calling different flags in the CLI when running the docker image/conatiner of the scraper.

If running from a local or EC2 Ubuntu 20.04 terminal you can:
- Pull and run the docker image directly from Dockerhub. Instructions on how to run the docker image inside EC2 Ubuntu 20.04 are found in the *run_scraper_container.sh* file.<br />&nbsp;&nbsp;&nbsp;&nbsp;
    `docker pull wr95/asos_scraper` <br />&nbsp;&nbsp;&nbsp;&nbsp;
    `docker pull wr95/asos_scraper` 
 <br /> <br />
### **Configuration**
The following parameters require arguments within the config.yaml file:
 
Parameters |&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Arguments&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Usage |
--- | :---: | --- |
DRIVER |**Chrome** *or* **Remote**|- **Chrome** will run the scraper displaying the graphical interface<br />- **Remote** will run the scraper on  selenium standalone:<br />&nbsp;&nbsp;&nbsp;&nbsp;- This requires ```docker pull selenium/standalone-chrome``` to pull the selenium/standalone image from Dockerhub<br />&nbsp;&nbsp;&nbsp;&nbsp;- Then `docker run -d -p 4444:4444 --shm-size="2g" selenium/standalone-chrome:4.1.0-20211123`<br /><br />- Please see the selenium/standalone README here https://github.com/SeleniumHQ/docker-selenium for further help if requried!
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
S3_BUCKET: False
BUCKET_NAME: <Enter your bucket name here>
PRODUCTS_PER_CATEGORY: all
SAVE_IMAGES: False
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

### **CMD Flags** 
&nbsp;&nbsp;&nbsp;**Flag**| **Usage**
---|---
--CH | By default the driver runs on driver.Chrome() <br /> Use **--no-CH** to disable this option.
--R | By default the remote driver.Remote() is innactive. <br /> Use **--R** to enable this option.
--M | By default, the men option is false. <br /> Use **--M** to scrape men's section.
--W | By default, the women option is false. <br /> Use **--M** to scrape women's section.
--L | By default, the data is saved locally <br /> Use **--no-L** to disable this option.
--S3 | By default, this option is disabled. <br /> Use **--S3** to save data to your S3 bucket 
--SJ | By default, data is automatically saved to json. <br /> Use **--no-SJ** to disable this option.
--SI | By default, the product images are *not* downloaded automatically. <br /> Use **--SI** to disable this option.
-BN | The user's S3 bucket name. <br /> Use -BN <*Enter your bucket name here*>. <br /> Visit https://s3.console.aws.amazon.com/s3/ to create a bucket if not done already
-NUM | By default, -NUM = **all**. This will scrape every product from categories selected. <br /> Use **-NUM integer** to scrape required number of products from each category.<br />
-OM | By default, all **men**'s categories are scraped. <br /> Use **-OM integer** to choose a category.<br />(**1**)New in, (**2**)Clothing, (**3**)Shoes, (**4**)Accessories, (**5**)Topman, (**6**)Sportswear, (**7**)Face + Body"
-OW | By default, all **women**'s categories are scraped. <br /> Use **-OM integer** to choose a category.<br />(**1**)New in, (**2**)Clothing, (**3**)Shoes, (**4**)Accessories, (**5**)Topshop, (**6**)Sportswear, (**7**)Face + Body"



### E.g. These are the default flags the scraper is using:
Given the configuration file in the example above, *`python ASOS_Scraper.py --CH --M --L --SJ`* returns the same result as *`python ASOS_Scraper.py`*

```
$ python ASOS_Scraper.py --CH --M --L --SJ 
Namespace(CH=True, R=False, M=True, W=True, L=True, S3=False, SJ=True, SI=False, BUCKET_NAME=None,PRODUCTS_PER_CATEGORY='all', OPTIONS_MEN=[0], OPTIONS_WOMEN=[0])
```
### This is an example of how to customize your choices: <br /> 
```
$ python ASOS_Scraper.py --no-CH --R --M --W --no-L --S3 --SJ -BN mybucketname -NUM 100 -OM 57 -OW 46 
Namespace(CH=False, R=True, M=True, W=True, L=False, S3=True, SJ=True, SI=False, BUCKET_NAME='mybucketname', PRODUCTS_PER_CATEGORY='100', OPTIONS_MEN='57', OPTIONS_WOMEN='46')
```
This scraper will run remotely using selenium standalone, will scrape for both **M**en and **W**omen, will save the data to an **S3** bucket called `mybucketname`, scraping **100** products per each of the given categories: **M**en (**5**)Topshop and (**7**)Face + Body"; **W**omen (**4**)Accessories and (**6**)Sportswear.

## **Current Status**
The scraper has successfully collected alphanumeric and image data for over 1000 product samples from the website and saved these to our own S3 Bucket.
## **Roadmap**
- Add functionality to stop repeated data collection on subsequent reruns
- Connect data to PostgreSQL database using psycopg
- Use Grafana to monitor resource usage on CPU and/or EC2
<br >
