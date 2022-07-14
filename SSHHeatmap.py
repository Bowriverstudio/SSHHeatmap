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


# Set a default api key here if you're not using sys arguments.
api_key = ""

# Filename of the txt with the output of: grep "authentication failure\| Failed password" /var/log/auth.log > failed_attempts.txt
try:
    filename = sys.argv[1]
except IndexError:
    if(api_key == ""):
        print("Usage: SSHHeatmap.py <source_filename> <api key> <attempts_threshold> <heatmap_filename>")
        print("To run SSHHeatmap without arguments, manually set an api key.")
        quit()
    filename = "failed_attempts.txt"
    pass

# ipinfo.io api key
try:
    api_key = sys.argv[2]
except IndexError:
    if(api_key == ""):
        raise IndexError(
            "API key not found. Please pass your ipinfo.io api key as the second argument, or set it manually.")

# minimum login attempts per ip required to include it in the heatmap
try:
    min_attempts = int(sys.argv[3])
except IndexError:
    min_attempts = 30
    pass

# what filename the heatmap should be saved as.
try:
    heatmap_filename = sys.argv[4]
except IndexError:
    heatmap_filename = 'heatmap.html'
    pass

# create handler to interface with API
ip_handler = ipinfo.getHandler(api_key)

# read the file, split on newlines into array, return list of ips


def read_file_get_ips(filename):
    with open(filename) as f:
        f_a = f.read().split('\n')

        # get array with only the ips
        # Use a regex to match and extract ips
        p = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        ips = []
        for x in f_a:
            match = p.search(x)
            if match:
                ip = match.group(0)
                ips.append(ip)

        print('Read file ' + filename + ' and got ' +
              str(len(ips)) + ' login attempts.')
        return ips


def save_dates_from_ips(filename):
    with open(filename) as f:
        f_a = f.read().split('\n')
        # get array with only the ips
        # Use a regex to match and extract ips
        p = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

        ips = []
        dates_ip = []
        for x in f_a:
            theDate = ""
            if(x):
                split = x.split()
                theDate = (split[0] + ' ' + split[1] + " " + split[2])
            match = p.search(x)
            if match:
                ip = match.group(0)
                ips.append(ip)
                dates_ip.append([theDate, ip])

        print('Read file ' + filename + ' and got ' +
              str(len(ips)) + ' login attempts.')

        # open the file in the write mode
        header = ['date', 'IP Address']

        with open('dates_ip.csv', 'w', encoding='UTF8') as f:
            # create the csv writer
            writer = csv.writer(f)
            writer.writerow(header)
            # write a row to the csv file
            writer.writerows(dates_ip)

        return ips
# Returns a list with the items in the passed list that occur at least min_attempts times.


def get_applicable_ips(ips):
    counts = Counter(ips).most_common()
    min_attempts = 0
    meet_minimum = [x[0] for x in counts if x[1] > min_attempts]
    print('No. of ips with at least ' + str(min_attempts) +
          ' login attempts: ' + str(len(meet_minimum)))
    return meet_minimum

# Call ipinfo api per api to get coordinates.


def get_ip_coordinates(ips):

    print('Fetching coordinates...')
    if(len(ips) > 500):
        print("Fetching coordinates for > 500 IP's. Please consider using your own (free) ipinfo API key if you are not already.")
    print(ips)
    # split the list of ips into batches of 100 (or less, if the list is smaller)
    batches = [ips[x:x+100] for x in range(0, len(ips), 100)]
    coords = []
    ipinfo = []
    start = time.process_time()
    for batch in batches:

        # send the request to the api and get the values as a list
        v = list(ip_handler.getBatchDetails(batch).values())

        # split the coords into a list with lat and lon if type is not dict, because the type of an error response is a dict
        c = [x['loc'].split(',') for x in v]
        coords.extend(c)
        ipinfo.extend(v)
        print("Fetched " + str(len(coords)) + "/" + str(len(ips)) +
              " coordinates in " + str(round(time.process_time() - start, 3)) + " seconds.")

    with open('ipinfo.csv', 'w', encoding='UTF8') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file

        for row in ipinfo:
            writer.writerow(row.values())
        # writer.writerows(ipinfo.values())

    return coords


def generate_and_save_heatmap(coords):
    # generate and save heatmap
    m = folium.Map(tiles="OpenStreetMap", location=[20, 10], zoom_start=2)
    # mess around with these values to change how the heatmap looks
    HeatMap(data=coords, radius=15, blur=20, max_zoom=2, max_val=2).add_to(m)
    m.save(heatmap_filename)
    print('Done. heatmap saved as ' + heatmap_filename)
    return


def main():
    # ips = read_file_get_ips(filename)
    ips = save_dates_from_ips(filename)
    ips_count = get_applicable_ips(ips)
    # print(ips_count)
    coords = get_ip_coordinates(ips_count)
    generate_and_save_heatmap(coords)


main()
