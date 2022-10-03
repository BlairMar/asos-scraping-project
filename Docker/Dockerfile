FROM python:3.9

COPY . . 

RUN apt-get update && apt-get install -y wget
RUN apt-get -y update &&\
    apt install -y wget &&\
    apt install -y gnupg &&\
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - &&\
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' &&\
    apt-get -y update &&\
    apt-get install -y google-chrome-stable &&\
    apt-get install -yqq unzip &&\
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip &&\
    apt-get install -yqq unzip &&\
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ 

ENV DISPLAY=:99

RUN  pip install -r ./requirements.txt 

ENTRYPOINT ["python", "ASOS_Scraper.py"]

CMD ["--CH", "--M", "--W", "--L", "--SJ" ]