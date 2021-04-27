# Plan of action

My goal was to create the tool in **Python3**, with **SQLite database** and **web interface**, **dockerized**.

# Python3

Initially I was deciding between Python and Golang, but the laters syntax seemed way too hard to get into so I stuck with Python.

## HTTP Request

Firstly I learned how to use the Pythons request library. The 42 API lacks the examples in Python so I had to figure out how to send the params correctly, which took a bit of trial and error, but I managed to get it working. I made a couple of flexible functions to request data from the API using flexible parameters to make completely custom requests without making each end point it's own.

## JSON

I've had some experience with handing JSON data with Javascript before so I used JSON-files as a temporary database to read and save data. The API response is also in JSON so I used the new learned skills to navigate thru the values in the items.

# SQLite

Same as with JSON, I have had some previous experience with MySQL so some of the syntax wasn't all new to me.

## Tables

The table design was probably the hardest part of the database. I went with 4 tables: Campus, students, projects and evaluations. Their content should be self-descriptive. 

I designed the tool to be parse data on a particular campus and not as a whole.

## Functions

SQL databases have your common insert and select functions you would use for dealing with the data. I made a couple different variations of these basic tools with some custom variables to be more specific.

# Docker

I wanted to make this tool into a dockerized version so I could do the bonus part and use a web-based interface instead of the basic command line look.

# Web interface

I make the data visualization easier I wanted to create a web page for interacting with the data.

