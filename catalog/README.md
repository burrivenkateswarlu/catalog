# Item Catalog Web Application project
By Burri Venkateswarlu
This web app is a project for the Udacity [FSND Course](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## Overview
This project is a web application utilizing the Flask framework and Database. In this project the user who created this data(admin) can only edit or delete items in this site by login to the site through Gmail. normal user can only view the items in the site

## Skills Required
1. Python
2. HTML
3. CSS
4. OAuth
5. Flask Framework
6. DataBaseModels


## Dependencies for Installation and Running the project
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)



## How to Install and Run the Project
1. Install Vagrant & VirtualBox
2. Clone the Udacity Vagrantfile
3. Go to Vagrant directory and either clone this repo or download and place zip here
- Create Vagrant file `vagrant init ubuntu/xenial64`
- Connect to VirtualMachine `vagrant up`
- Login to VirtualMachine `vagrant ssh`
- Exit from current directory  `cd ..`
- Again exit directory `cd ..`
- Change directory path `cd vagrant`
- Change Project directory `cd catalog`
- To see list of files `ls -l`

### Here we need to install some modules and python

- Update `sudo apt-get update`
- Install Python `sudo apt-get install python`
- Install pip `sudo apt-get install python-pip`
- Import module `pip install flask`
- Import module`pip install sqlalchemy`
- Import module `pip install oauth2client`
- Import module `pip install httplib2`
- After installing modules we have to run `python Data_Setup.py` to create database models 
- Next run `python database_init.py` to insert sample data.
- Next run `python main.py` to execute project


## Google Login
To get the Google login working have to follow some steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'Rifle_Store'
7. Authorized JavaScript origins = 'http://localhost:8000'
8. Authorized redirect URIs = 'http://localhost:8000/login' && 'http://localhost:8000/gconnect'
9. Select Create
10. Copy the Client ID and use it into the `data-clientid` in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in rifle_store directory that you cloned from here
14. Run application using `python /rifle_store/main.py`

## JSON Endpoints

The following are to check JSON endpoints:

allRiflesJSON: `/RifleStore/JSON`
    - Displays the whole rifle models and rifle details

categoriesJSON: '/rifleStore/rifleCategories/JSON'
    - Displays the rifle models and its id
	
itemsJSON: '/rifleStore/rifles/JSON'
	- It displays all rifle details

categoryItemsJSON: '/rifleStore/<path:rifle_name>/rifles/JSON'
    - It displays the details of perticular rifle model

ItemJSON:
'/rifleStore/<path:rifle_name>/<path:edition_name>/JSON'
    - It displays the details of a given rifle and rifle model
	

The outputs to this project are in the images folder of this project folder.