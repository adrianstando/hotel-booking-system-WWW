# Hotel Booking System

## App description

This is a web application for booking hotel rooms. 

The website is available online: [https://hotel-booking-system-project.herokuapp.com/](https://hotel-booking-system-project.herokuapp.com/)

## Run the application locally

1. To run the application locally you need to have `Python 3` installed.

2. Next, you have to create a virtual environment and install required packages. All you have to do is to run a script: `./create_project`

3. (optional) You can also create a database ind fill it with example data by running a script:  `./create_database` However, one is already created, so you don't have to do it once more.

4. To run an app run a script: `./start_app`. You will see then the address on which the website is available.

## Additional configuration

By default, a server is started with 2 workers, but you can change it by editing `--workers` parameter in the script `./start_app`.

## Additional files

In the repository, there are two files, which are nedded by heroku for deployment. 

These two files are: `Procfile` and `runtime.txt`.

## Technologies

The following technologies were used in the project (the most important):

* HTML
    * Bootstrap 4
* JavaScript
    * jQuery
* Python
    * FastAPI
    * uvicorn
    * asyncio
    * pandas
    * SQLite3
* Database
    * SQLite3

The photos are mostly shared on Creative Commons licence in the Internet; the details are in the following file: `./html/items/README.md`. The logo and favicon were created in `GIMP`.


## Project purpose

It is the final project created during Web Application course at Data Science studies at MiNI, Warsaw University of Technology. 
