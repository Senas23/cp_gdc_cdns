# cp_gdc_cdns
CHKP GenericDataCenter of CDNs - IPv4 and IPv6 addresses of various CDNs for GenericDataCenter object

## Purpose
Parse IPv4 and IPv6 addresses from various CDNs (`Cloudflare` and `Akamai`) into objects used as tags. The result of the objects within can be used as tags in Access Control policies. The created JSON file's objects will be used as a GenericDataCenter object. The JSON file is created automatically from GitHub Actions on a schedule and updated only on changes.

## Content
`main.py` - Python code that gets and parses data and generates `cdns.json` file

`cdns.json` - JSON file formated for Check Point's GenericDataCenter object. R81+ is required. See `sk167210`

`.github/workflows/main.py` - GitHub Actions workflow of running Python code and create/update `cdns.json`

## Prerequisites
Check Point R81+

## Instructions
#### Direct Use
Use the URL of the raw `cdns.json` file right in your GenericDataCenter object and use the resulting objects as `tags` in the Access Control policy.
```
https://raw.githubusercontent.com/Senas23/cp_gdc_cdns/main/cdns.json
```

##### Add GenericDataCenter through API
API Documentation
```
https://sc1.checkpoint.com/documents/latest/APIs/#web/add-data-center-server~v1.7%20
```
MGMT_CLI
```
mgmt_cli add data-center-server name "CDNs" type "generic" url "https://raw.githubusercontent.com/Senas23/cp_gdc_cdns/main/cdns.json" interval 60 -f json
```

#### Clone Repo
Clone repo and delete existing `cdns.json` file
```
git clone https://github.com/Senas23/cp_gdc_cdns.git
```

#### Create Repo Secrets
Create repo secrets for the workflow under Settings -> Secrets -> Actions

`GH_USER` - Your GitHub account's username

`GH_MAIL` - Your GitHub account's email

## Run
Nothing needs to be done, as the GitHub Actions workflow runs on a schedule of 15 minutes.
You can also clone the repo and run `python3 main.py` on your local system as a cronjob to generate `cdns.json` file.

## Development Environment
Python 3.6.9; Ubuntu 18.04.5 LTS;
