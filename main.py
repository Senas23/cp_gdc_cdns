#!/usr/bin/env python3
import requests, re, json, logging, uuid, os
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning, MaxRetryError, NewConnectionError

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

cloudflare = {}
cloudflare['name'] = "Cloudflare"
cloudflare['description'] = "Cloudflare IPv4 and IPv6"
cloudflare['url'] = [
    "https://www.cloudflare.com/ips-v4", "https://www.cloudflare.com/ips-v6"
]
cloudflare['id'] = str(uuid.uuid4())
cloudflare['regex'] = "^(\d+.*\d+)$"

akamai = {}
akamai['name'] = "Akamai"
akamai['description'] = "Akamai IPv4 and IPv6"
akamai['url'] = [
    "https://learn.akamai.com/en-us/webhelp/origin-ip-acl/origin-ip-acl-guide/GUID-E5AD1B2B-BDA1-4C3F-87DE-B0CDBDD1E1B0.html"
]
akamai['id'] = str(uuid.uuid4())
akamai['regex'] = "^\s+<td[^>]+>(\d.*\d)<\/td>$"

gdc = {}
gdc['description'] = "CDNs"
gdc['file'] = "cdns.json"


def get_cdn(url: list, reg: re) -> list:
    reg_result = []
    for item in url:
        try:
            res = requests.get(item, verify=False)
            if res.status_code == 200:
                response = res.text.splitlines()
                for line in response:
                    if re.match(reg, line, re.IGNORECASE):
                        reg_result.append(
                            re.match(reg, line, re.IGNORECASE).group(1))
            else:
                logging.warning(f"[*] Could not fetch from {item}")
        except (NewConnectionError, ConnectionError, MaxRetryError,
                RequestException) as e:
            logging.error(f"[*] Connection exception in get_cdn() for {item}")
            exit(1)
        except Exception as e:
            logging.error(
                f"[*] General Error exception in get_cdn() for {item}")
            exit(1)
    return reg_result


def gdc_create_object(name: str, uuid: str, description: str,
                      ranges: list) -> dict:
    return {
        "name": name,
        "id": uuid,
        "description": description,
        "ranges": ranges
    }


def update_uuid():
    file = {}
    try:
        if os.path.isfile(gdc["file"]):
            with open(gdc["file"], 'r') as f:
                file = json.load(f)

            for item in file['objects']:
                if item['name'] == cloudflare['name']:
                    cloudflare['id'] = item['id']
                elif item['name'] == akamai['name']:
                    akamai['id'] = item['id']
    except Exception as e:
        raise e
        exit(1)
    return


def main():
    update_uuid()
    cloudflare_list = get_cdn(cloudflare["url"], cloudflare["regex"])
    akamai_list = get_cdn(akamai["url"], akamai['regex'])

    gdc_file = {
        "version": "1.0",
        "description": gdc["description"],
        "objects": []
    }
    gdc_file["objects"].append(
        gdc_create_object(name=cloudflare["name"],
                          uuid=cloudflare["id"],
                          description=cloudflare["description"],
                          ranges=cloudflare_list))
    gdc_file["objects"].append(
        gdc_create_object(name=akamai["name"],
                          uuid=akamai["id"],
                          description=akamai["description"],
                          ranges=akamai_list))
    with open(gdc["file"], 'w') as f:
        json.dump(gdc_file, f, indent=2)
    return


if __name__ == "__main__":
    main()
