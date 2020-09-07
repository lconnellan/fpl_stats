# Database/website for Fantasy Premier League stats

A simple project to showcase some useful stats for evaluating players, namely deviation and points per million.

## Features

* Scrapes player information from the official website using Selenium and stores in mySQL database
* Calculates value in points per million, deviation and deviation by position
* Results from computations in R included
* Displays data on a website (using [DataTables](https://datatables.net/))

## Usage

To run website: `/run.py`
To update players: `python update.py`
To remake database: `mysql < rollback.sql && mysql < fpl.sql`
