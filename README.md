# Web3 backend and smart contract development for Python developers: Musical NFTs part 1

In following set of posts I will be focused on `Python` based web3 backend development. This subject by itself is quite immense. It is `Python` web2 backend plus peculiarities of web3 world. This will include smart contract writing, testing and deployment to `Polygon` test-net `Mumbai` or similar with Brownie. Ones we have this in place we will move to `DjangoREST` backend and full integration with `Google cloud` platform services like `Firestore` (NoSQL database), `Firebase storage` and `Google authentication`. Also on the way we will integrate our web3 app with `Chainlink` VRF, `IPFS` (via `Pinata`) for NFT metadata, `Stripe` (for potential NFT credit card buyers) and few other services. Finally ones all this is done we will deploy our app to `Google App engine` from where our APIs will be available. 

General architecture should look something like this =>

<img src="./photos/general_architecure_intro.png" width=800 height=500>

### What we will build?

We will make API endpoints that can be consumed by client and through them provide interaction with smart contracts and normal backend functionalities like sign-up, login etc. Smart contracts will be coded in Solidity and main idea behind will be idea of musical NFTs. Imagine that musical company can issue certain number of trackpacks per batch. User then can buy one or more trackpacks with credit card or with crypto without knowing which songs are inside. Then we will provide to them opening functionality through which they will be able to initiate opening process (similar to opening of package of physical thumbnails). Ones he initiate opening process of his trackpack NFT we will use Chainlink VRF (verifiable random function) to randomly assign 5 NFT songs from musical company catalog to user address or to custodial wallet (in case of credit card buyers). In short something like blockchain version of musical NFT thumbnails. 


### But first things first: diving equipment!

Let's talk shortly about equipment we plan to use for this deep dive and environment in which we will build. I'm working on `Ubuntu 20.04.6` over `Windows WSL` and Im using `Python 3.8.10`. Then we will need to PIP install few packages and to create Python virtual environment. I'm using `venv` but you are free to use what ever you find most suitable for you. Then we will build our APIs with `Django REST` framework version 3.14.0 and develop smart contracts with `Brownie`. Backend interaction with deployed smart contract will be done through web3.py. For testing `Pytest` + few SDKs to manage our relation to Google cloud services and Stripe. As you can see  our tech stack is quite conventional. Maybe in context when we work over Google cloud with NoSql database and Google authentication Django REST can be seen as overkill (because we don't use his ORM layer at all in first phase of project). And maybe from this point of view is logical to opt for some more light Python framework like FastAPI. But we will stick to Django because at certain point we will develop also alternative version of our app that use SQL database and have Django native authentication mechanism in place. For version control we will use Git and then project code will be available over Github. 

And now let's do what our fellow Apes on Earth like to do for the centuries "Build that rocket and fly to motherfucking space..."      

<br/>
<br/>
<br/>
<br/>
<br/>

# Web3 backend and smart contract development for Python developers: Musical NFTs part 2


We will build few versions of this project: 
Pure Django + postgres db; 
Django REST, REACT for front-end + sql database; 
Django REST, React front-end and Google cloud (firestore noSql db, google storage and authentication). 

What means in third version we will avoid whole ORM layer of Django and substitute with Google services (a bit atypical combination).     


There will be two options here:

### Simple Git clone
In this option you can simple git clone project, run Django server locally and  play with functionalities and code. 

    # make dir and clone project github repo
    $md musical_nft_thumbnails && cd musical_nft_thumbnails 
    
    $git clone https://github.com/ilijapet/musical_nft_thumbnails.git .

    # you need to have env or similar enviroment manager
    $python -m venv env && source env/bin/activate
    
    # you need to have pip installed
    $pip install -r requirements.txt
    
    # run django server
    $python manage.py runserver

Now you can go to `http://127.0.0.1:8000/` and play with app. Or change source as you find most suitable. 

### Step by step guide

Second option is focused more on process for devs interested in how to put all this things together.

    $md musical_nft_thumbnails && cd musical_nft_thumbnails
    $git init
    # Create .gitignore with our future env folder
    $echo "env/" > .gitignore
    $git add -A
    $ git commit -m "First commit"
    $git branch -M main

Go go Github repo and create new repo:

![creating env file in secret manager](./photos/github_new_repo.png)

<br/>
<br/>

![creating env file in secret manager](./photos/github_new_repo_1.png)
        
<br/>
<br/>

    # add name of your branch
    $git remote add origin https://github.com/ilijapet/musical_nft_thumbnails.git
    $git push -u origin main

At this point we have local git repo, initial commit and code in your github repo. 


Lets create virtual environment and activate them: 

    $python -m venv env && source env/bin/activate

At this point we have local git, dedicated and with local git connected Github repo as well as local virtual environment created and activated. 

Now lets install Django and create our requirements.txt  
    # install django
    $pip install django

    # create requirements.txt
    $pip freeze > requirements.txt


Basically from this point we are ready to start writing the coding. But before that here is picture of overall architecture. 


<img src="./photos/overall_flow.png"  width="600" height="300">

<br/>

Client send some request to our backend server, routed through urls our app
views will handle the call. Read and write from sql database. Communicate with our smart contract when needed. Bake together all this processed data and return page to client. Fairly standard flow except web3 element and Chanilink and Polygon testnet Mumbai.   

<br/>
<br/>
<br/>
<br/>
<br/>

# Web3 backend and smart contract development for Python developers: Musical NFTs part 3

### Installing postgres database

This postgres installation procedure is written for WLS environment and it will presume that you already have WSL installed on your machine. If that's not the case go fist to WSL documentation and ones you successfully finish installation process you can continue from this point. 

(If you want to check if you have WSL already installed just can go to windows command line and type `wsl -l -v`)
```
$ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
 
$ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
 
$ sudo apt-get update
 
$ sudo apt-get -y install postgresql postgresql-contrib
 
$ psql --version
psql (PostgreSQL) 15.2 (Ubuntu 15.2-1.pgdg22.04+1)
 
$ sudo service postgresql status
15/main (port 5432): down
 
$ sudo service postgresql start
 * Starting PostgreSQL 15 database server
```

### Starting new Django project and adding postgres to our settings file

Let's first install Django

    $ pip install django
    # update requirments
    $ pip freeze > requirements.txt

This will install latest Django stabile version and add Django to our requirements.txt

To check if everything went well type

    $python -m django --version
    4.2.5

Now we will create new project in root directory `musical_nft_thumbnails`

    $django-admin startproject musical_nft .

Now project root folder should look something like this:

    ├── README.md
    ├── env
    ├── manage.py
    ├── musical_nft
    └── requirements.txt


In attempt to test django and everything worked as expected we should

    $python manage.py runserver

If everything goes well we should see something like

    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).

    You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
    Run 'python manage.py migrate' to apply them.
    September 21, 2023 - 20:03:07
    Django version 4.2.5, using settings 'musical_nft.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.



### Creatig user and new database 


    $sudo service postgresql start
    * Starting PostgreSQL 15 database server [ OK ] 
    * Starting PostgreSQL 9.1 database server 

    # create user
    $ sudo -u postgres denis

    # create database
    $sudo -u postgres createdb muscial_nft_db
    
    # now lets go to postgres command line and give password to user 
    $sudo -u postgres psql
    psql (15.4 (Ubuntu 15.4-1.pgdg20.04+1))
    Type "help" for help.
    postgres=# alter user denis with encrypted password 'testpassword';
    # grant all privileges to newly created database to user denis
    postgres=# grant all privileges on database muscial_nft_db to denis


Before we move to `settings.py` let's install `django-environ` library for
managing environment variables in our project.

    $pip install django-environ
    $pip freeze > requirements.txt

Create `.env` in our root directory and write

    DENIS_PASS=testpassword

Add `.env` file to our `.gitignore` 

    env/
    .env


Inside `musical_nft` you should be able to find and open `settings.py`
























