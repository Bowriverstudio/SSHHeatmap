# Author: Mees Altena, 24-04-2020
# Licence: MIT
import re
import os
import requests
import folium
from folium.plugins import HeatMap
import ipinfo
import sys
import time
from collections import Counter
import operator
import csv
import json


# read the file, split on newlines into array, return list of ips


def read_write_file_dates():

    # reading data from a csv file 'Data.csv'
    with open('ipinfo.csv', newline='') as file:

        reader = csv.reader(file, delimiter=',')

        # output list to store all rows
        ip_dict = {}
        for row in reader:
            # IP - 0, last 3
            country_index = len(row) - 3
            ip_dict[row[0]] = row[country_index]

    country_ip_count = {}
    for key in ip_dict:
        if ip_dict[key] in country_ip_count:
            country_ip_count[ip_dict[key]] = country_ip_count[ip_dict[key]] + 1
        else:
            country_ip_count[ip_dict[key]] = 1

    # reading data from a csv file 'Data.csv'
    with open('dates_ip.csv', newline='') as file:

        reader = csv.reader(file, delimiter=',')
        # store the headers in a separate variable,
        # move the reader object to point on the next row
        headings = next(reader)
        # output list to store all rows
        countries = {}
        for row in reader:
            country = ip_dict[row[1]]
            if country in countries:
                countries[country] = countries[country] + 1
            else:
                countries[country] = 1

        with open('countries_count.csv', 'w', encoding='UTF8') as f:
            # create the csv writer
            writer = csv.writer(f)
            writer.writerow(["Country,Count,IP Address"])
            for key in countries:
                writer.writerow([key, countries[key], country_ip_count[key]])

        print(countries)


# Returns a list with the items in the passed list that occur at least min_attempts times.


def main():
    # ips = read_file_get_ips(filename)
    read_write_file_dates()


main()
