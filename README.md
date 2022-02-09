# cp_gdc_cdns
CHKP GenericDataCenter of CDNs - IPv4 and IPv6 addresses of various CDNs for GenericDataCenter object

## Purpose
Parse IPv4 and IPv6 address from various CDNs (`Cloudflare` and `Akamai`) into objects that can be used as tags. The JSON file that will be created, will be used as GenericDataCenter object. The result of the objects within, can be used as tags in Access Control policies. The JSON file is created automatically from GitHub Actions on a schedule and only if we have any changes to be made.

## Content
`main.py` - Python code that gets and parses data, and generates `cdns.json` file

`cdns.json` - JSON file in format for Check Point's GenericDataCenter object. R81+ is required. See `sk167210`

`.github/workflows/main.py` - GitHub Actions workflow of running Python code and create/update `cdns.json`

## Prerequisites
Check Point R81+

## Instructions
### Direct Use
Use raw `cdns.json` right into your GenericDataCenter object and use objects as `tags`
```
 export AWS_ACCESS_KEY='<API ACCESS KEY>'
 export AWS_SECRET_KEY='<API SECRET KEY>'
```

### Clone Repo
Clone repo without `cdns.json` file
```
git clone https://github.com/Senas23/cp_gdc_cdns.git
```

### Create Repo Secrets
Create repo secrets for the workflow under Settings -> Secrets -> Actions

`GH_USER` - Your GitHub account's username

`GH_MAIL` - Your GitHub account's email


## Run
Nothing needs to be done, as the GitHub Actions workflow runs on a schedule of 5 minutes.
You can also clone the repo and run on your local system as a cronjob for `cdns.json` file generation.

## Development Environment
Python 3.6.9; Ubuntu 18.04.5 LTS;
