# cp_gdc_cdns
CHKP GenericDataCenter of CDNs - IPv4 and IPv6 addresses of various CDNs for GenericDataCenter object

## Purpose
Parse IPv4 and IPv6 addresses from various CDNs (`Cloudflare` and `Akamai`) into objects used as tags. The result of the objects within can be used as tags in Access Control policies. The created JSON file's objects will be used as a GenericDataCenter object. The JSON file is created automatically from GitHub Actions on a schedule and updated only on changes.

## Content
`main.py` - Python code that gets and parses data from `input.yaml` and generates `cdns.json` file

`cdns.json` - JSON file formated for Check Point's GenericDataCenter object. R81+ is required. See `sk167210`

`requirements.txt` - Python3 PIP requirements file

`.github/workflows/main.py` - GitHub Actions workflow of running Python code and create/update `cdns.json`

`.github/workflows/sourceguard.yml` - GitHub Actions workflow to run CHKP Sourceguard SAST CLI tool on `push` to comply to safe coding practices

## Prerequisites
Check Point R81+ for GenericDataCenter, R81.20+ for NetworkFeed

## Instructions
#### Direct Use as GenericDataCenter object (R81+)
Use the URL of the raw `cdns.json` file right in your `GenericDataCenter` object and use the resulting objects as `tags` in the Access Control policy.

**NOTE:** `GenericDataCenter` object will be downloaded by the management server, and pushed to the firewalls in question which use the resulting `tags` in their policies.
```
https://raw.githubusercontent.com/Senas23/cp_gdc_cdns/main/cdns.json
```

#### Direct Use as NetworkFeed object (R81.20+)
Use the URL of the raw `cdns.json` file right in your `NetworkFeed` object, add JQ filter for specific CDN, set feed format to `JSON`, set feed type `IP Address`, and use the object in the Access Control policy.

**NOTE:** `NetworkFeed` object will be downloaded by the firewall, not the management server.
```
https://raw.githubusercontent.com/Senas23/cp_gdc_cdns/main/cdns.json
```
Add JQ filter for `Cloudflare` object:
```
.objects[] | select(.name == "Cloudflare" ) | .ranges[]
```
Add JQ filter for `Akamai` object:
```
.objects[] | select(.name == "Akamai" ) | .ranges[]
```

#### Add GenericDataCenter object through API
API Documentation
```
https://sc1.checkpoint.com/documents/latest/APIs/#web/add-data-center-server~v1.7%20
```
MGMT_CLI
```
mgmt_cli add data-center-server name "CDNs" type "generic" url "https://raw.githubusercontent.com/Senas23/cp_gdc_cdns/main/cdns.json" interval 60 -f json
```

#### Add NetworkFeed object through API
API Documentation
```
https://sc1.checkpoint.com/documents/latest/APIs/#web/add-network-feed~v1.9%20
```
MGMT_CLI
```
mgmt_cli add network-feed name "nf_Cloudflare" feed-url "https://raw.githubusercontent.com/Senas23/cp_gdc_cdns/main/cdns.json" json-query ".objects[] | select(.name == "Cloudflare" ) | .ranges[]" feed-format "JSON" feed-type "IP Address" update-interval 60 -f json
```

#### Fork Repo
Fork repo and delete existing `cdns.json` file

#### Create Repo Secrets
Create repo secrets for the workflow under Settings -> Secrets -> Actions

`GH_USER` - Your GitHub account's username

`GH_MAIL` - Your GitHub account's email

#### Run
Nothing needs to be done, as the GitHub Actions workflow runs on a schedule of 15 minutes.
You can also clone the repo and run `python3 main.py` on your local system as a cronjob to generate `cdns.json` file.

## Local Use
Clone repo and delete existing `cdns.json` file
```
git clone https://github.com/Senas23/cp_gdc_cdns.git
```
Install Python requirements
```
pip install -r requirements.txt
```
Run code
```
python3 main.py
```

## Development Environment
Python 3.6.9; Ubuntu 18.04.5 LTS;
