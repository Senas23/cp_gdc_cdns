#!/usr/bin/env python3
import requests, re, json, logging, uuid, os, random
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
cloudflare['match_group'] = 1

akamai = {}
akamai['name'] = "Akamai"
akamai['description'] = "Akamai IPv4 and IPv6"
akamai['url'] = [
    "https://techdocs.akamai.com/property-mgr/docs/origin-ip-access-control"
]
akamai['id'] = str(uuid.uuid4())
akamai['regex'] = "(^|\>)(\d.*?\/\d{1,2})\<"
akamai['match_group'] = 2

gdc = {}
gdc['description'] = "CDNs"
gdc['file'] = "cdns.json"

user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

def get_cdn(url: list, reg: re, match_group: int) -> list:
    reg_result = []
    for item in url:
        try:
            logging.warning(f'[*] Request for: {item}')
            headers = {'User-Agent': random.choice(user_agent_list)}
            res = requests.get(item, verify=False, timeout=30, headers=headers)
            if res.status_code == 200:
                for line in res.text.splitlines():
                  for match in re.finditer(reg, line, re.IGNORECASE):
                    reg_result.append(match.group(match_group))
            else:
                logging.warning(f"[*] Could not fetch from {item}")
        except (NewConnectionError, ConnectionError, MaxRetryError,
                RequestException) as e:
            logging.error(f"[*] Connection exception in get_cdn() for {item}")
            exit(1)
        except Exception as e:
            logging.error(f"[*] General Error exception in get_cdn() for {item}")
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
    cloudflare_list = get_cdn(cloudflare["url"], cloudflare["regex"], cloudflare["match_group"])
    akamai_list = get_cdn(akamai["url"], akamai['regex'], akamai["match_group"])

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
