# Hotel Booking System

## App description

This is a web application for booking hotel rooms. 

The website is available on the Internet: [https://hotel-booking-system-project.herokuapp.com/](https://hotel-booking-system-project.herokuapp.com/)

The application consists of two modules. The first is a publicly visible website, which is available on `/` endpoint. It contains information about the hotel and has a booking form. The second module is for administrator and is available on `/admin` endpoint. You have to log in to see the details - admin panel is not available for unlogged user.

## Run the application locally

1. To run the application locally you need to have `Python 3` installed.

2. Moreover, you have to set environment variables or create a file named `.env` in main directory with variables:

    `EMAIL_ADDRESS=name@gmail.com`

    `EMAIL_PASSWORD=password`

    `ADMIN_LOGIN=admin`

    `ADMIN_PASSWORD=admin`

    Variables `EMAIL_ADDRESS` and `EMAIL_PASSWORD` contains access data to your Gmail account, from which conformation emails will be sent. Variables `ADMIN_LOGIN` and `ADMIN_PASSWORD` defines login and password for admin access.

3. Next, you have to create a virtual environment and install required packages. All you have to do is to run a script: `./create_project`

4. (optional) You can also create a database ind fill it with example data by running a script:  `./create_database` However, one is already created, so you don't have to do it once more.

5. To start an app you have to run a script: `./start_app`. You will see then the address on which the website is available.

## Additional configuration

By default, a server is started with 2 workers, but you can change it by editing `--workers` parameter in the script `./start_app`.

## Additional files

In the repository, there are two files, which are nedded by heroku for deployment. 

These two files are: `Procfile` and `runtime.txt`.

## Technologies and libraries

The following technologies and libraries were used in the project:

* HTML + CSS
    * Bootstrap 4
    * Font Awesome - icons
    * Gijgo - datepicker
    * MDBootstrap - admin table
    * DataTables - admin table
* JavaScript
    * jQuery
    * Gijgo - datepicker
    * DataTables - admin table
    * JSCharting - admin charts
    * moment
* Python
    * FastAPI, fastapi_login, uvicorn
    * asyncio
    * pandas, SQLite3
    * smtplib, email
    * datetime, os, dotenv
    * starlette, pydantic
    * inspect, typing - for form decorator
* Database
    * SQLite3

The photos are mostly shared on Creative Commons licence on the Internet; the details are in the following file: `./html/items/README.md`. The logo and favicon were created in `GIMP`.


## Project purpose

It is the final project created during Web Application course at Data Science studies at MiNI, Warsaw University of Technology. 
