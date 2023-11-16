# 1 Percent Better API

A GraphQL API that functions as the backend for the 1 Percent Better workout tracker for mobile.

Hosted here --> https://one-percent-better-api-7up3.onrender.com/api/

If you would like to explore this repository and application on your local machine you can follow the steps outlined below.

## Getting Started

Before cloning this repository you will need to have an adequate version of Python installed on your machine.
This project was built using Python 3.10.12 and so we recommend this as a minimum requirement.

Instructions for installing Python can be found...

Here --> https://www.python.org/downloads/

### Step 1: Cloning

Clone this repository to your machine navigate to the root directory with the following terminal commands:

```
git clone https://github.com/aloan93/be-northcoders-news.git
cd be-1-percent-better
```

### Step 2: Setting up a Virtual Environment

A virtual environment is recommended so that we have an independent space to install required dependencies. You can set one up with the following terminal command:

```
python3 -m venv <environment-name-here>
```

It is recommended that you name your virtual environment 'venv' as this repo's .gitignore file is pre-tailored to ignore directories named venv.

Once created and visible in the root directory you can activate your environment with the following terminal command:

```
source <environment-name-here>/bin/activate
```

### Step 3: Installing Dependencies

To install the required dependencies for this project you can enter the following terminal command:

```
pip3 install -r requirements.txt
```

PLEASE NOTE - if you get any errors concerning 'pkg-config', you can run the following command as a fix:

```
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
```

### Step 4: Setting Up a Environment File

To protect sensitive information, such as database credentials, create a file called '.env' in the root of the repository. Within this you will need to insert the following (with your own values):

```
DB_NAME=my-bd
DB_USER=test-user
DB_PASSWORD=mysecurepassword
DB_HOST=127.0.0.1
DB_PORT=3306

SECRET_KEY=see-explanation-below
DEBUG=True
```

To generate your own secret key you can eneter the following command in your terminal:

```
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

PLEASE NOTE - the settings of this repository are pre-set to accommodate a MySQL database. If you wish to use a different db platform you will need to make relevant changes. Debug must be set to True (as above) for local development. DB_HOST must be set specifically to 127.0.0.1 if intending to locally host your database.

### Step 5: Making Migrations

Before running the server you will need to make sure your database is set-up and populated with the relevant tables and columns. You can do this by using the following commands in your terminal:

```
python3 manage.py makemigrations
python3 manage.py migrate
```

### Step 6: Running in Local

You can now run the application on your local machine using the following terminal command:

```
python3 manage.py runserver 0.0.0.0:8000
```

Upon success you will be presented with a local host link which you can navigate to by control clicking should it not open in your browser automatically. Once in your browser you will need to go to localhost:8000/api as the default landing page currently gives a 404 error.

PLEASE NOTE - due to default security settings, local host is recommended via port 8000 - hense the command above.

### And Done! Happy Exploring
