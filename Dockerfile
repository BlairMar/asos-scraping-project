FROM python:3.8

COPY . .
# installing the necessary functions
RUN apt-get update && apt-get install -y wget
RUN apt-get -y update &&\
    apt install -y wget &&\
    apt install -y gnupg &&\
    # adding trusting keys to get apps for repositories
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - &&\
    # Adding Google Chrome 
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' &&\
    apt-get -y update &&\
    # installing Google Chrome 
    apt-get install -y google-chrome-stable &&\
    # installing unzip 
    apt-get install -yqq unzip &&\
    # install the latest release of ChromeDriver
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip &&\
    # installing unzip and using it to unzip temporary directory for Chromedriver
    apt-get install -yqq unzip &&\
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ 


ENV DISPLAY=:99

RUN  pip install -r ./requirements.txt 

CMD ["python", "ASOS_Scraper.py"]