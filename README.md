# 1 Percent Better API

A GraphQL API that functions as the backend for the 1 Percent Better workout tracker for mobile.

Hosted here --> https://one-percent-better-api-7up3.onrender.com/api

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

A virtual environment is recommended so that we have an independent space to install required dependancies. You can set one up with the following terminal command:

```
python3 -m venv <environment-name-here>
```

It is recommended that you name your virtual environment 'venv' as this repo's .gitignore file is pre-tailored to ignore directories named venv.

Once created and visible in the root directory you can activate your environment with the following terminal command:

```
source <environment-name-here>/bin/activate
```

### Step 3: Installing Dependancies

To install the required dependancies for this project you can enter the following terminal command:

```
pip3 install -r requirements.txt
```

### Step 4: Setting Up a Environment File

To protect sensitive information, such as database credentials, create a file called '.env' in the root of the repository. Within this you will need to insert the following:

```
DB_NAME=<database-name>
DB_USER=<database-user>
DB_PASSWORD=<database-password>
DB_HOST=<database-host>
DB_PORT=<database-port>

SECRET_KEY=<django-secret-key>
DEBUG=<boolean-value>
```

Please note that the settings of this repository are pre-set to accommodate a MySQL database. If you wish to use a different db platform you will need to make relevent changes.

### Step 5: Making Migrations

Before running the server you will need to make sure your database is set-up and populated with the relevant tables and collums. You can do this by using the following commands in your terminal:

```
python3 manage.py makemigrations
python3 manage.py migrate
```

### Step 6: Running in Local

You can now run the application on your local machine using the following terminal command:

```
python3 manage.py runserver
```

Upon success your will be presented with a local host link (typically via port 8000) which you can navigate to by control clicking should it not open in your browser automatically.

### And Done! Happy Exploring
