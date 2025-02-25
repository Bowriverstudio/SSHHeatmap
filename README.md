# SSHHeatmap

This is a Fork of https://github.com/meesaltena/SSHHeatmap

The difference is this fork saves the metadata into files. Which we use to generate some tables as well.

## Roadmap

Convert the heatmap to this:
http://datamaps.github.io/

Generates a heatmap of IPs that made failed SSH login attempts on linux systems, using /var/log/auth.log to get failed attempts. Uses the ipinfo.io library to fetch the IP address coordinates, and folium to generate the heatmap.

<img src="https://i.imgur.com/ZNoACD0.png"></img>

## Dependencies

- Python >3.5
- venv
- folium
- ipinfo
- requests

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install folium requests ipinfo

```

## Installation & Usage

Use wget (or curl, or git clone) to download the script.

```bash
wget https://raw.githubusercontent.com/meesaltena/SSHHeatmap/master/SSHHeatmap.py
```

Use grep to generate a text file that contains the logging entries of failed ssh connection attempts. Pattern matches login attempts with a password as well as an ssh key.

```bash
grep "authentication failure\| Failed password" /var/log/auth.log > failed_attempts.txt
```

Or use /var/log/secure if /var/log/auth.log doesn't exist

```bash
grep "authentication failure\| Failed password" /var/log/secure > failed_attempts.txt
```

Get a free [ipinfo](https://ipinfo.io/) api key.

Run the script, passing the required arguments.

```bash
python3 SSHHeatmap.py failed_attempts.txt <ipinfo_api_key>
```

You can pass additional arguments to set the minimum number of login attempts required for the IP address to be included in the heatmap, and the file name to use for the heatmap.

```bash
python3 SSHHeatmap.py <sourcefile> <api key> <min_attempts> <heatmap_filename>
```

Open the generated heatmap HTML file in a browser.

## License

[MIT](https://choosealicense.com/licenses/mit/)
