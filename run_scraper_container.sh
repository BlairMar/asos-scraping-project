#Run docker image on EC2 Ubuntu 20.04
#Check if Docker is already installed 

#If not, install Docker following the coommands bellow. For more details, follow https://docs.docker.com/engine/install/ubuntu/
$ sudo apt-get update
sudo apt-get install \
ca-certificates \
curl \
gnupg \
lsb-release

$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

$ echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
 
$ sudo apt-get update

$ sudo apt-get install docker-ce docker-ce-cli containerd.io

$ sudo docker --version 

#After Docker is installed, download seleniu/standalone-chrome 
$ sudo docker pull selenium/standalone-chrome 

sudo docker run -d -p 4444:4444 --shm-size="2g" selenium/standalone-chrome:4.1.0-20211123

#Run the asos_scraper image. To connect to the remote 4444 port, please use the following flags --no-CH --R and then as preffered. Do not forget --M or --W.
sudo docker run <container name> or <image name> --no-CH --R 


