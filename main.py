#!/usr/bin/env python3
import requests, re, json, logging, uuid, os, random, yaml
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning, MaxRetryError, NewConnectionError

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

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


def update_uuid(cdns: list) -> list:
    try:
        for cdn in cdns:
          cdn['id'] = str(uuid.uuid4())

        if os.path.isfile(gdc["file"]):
            with open(gdc["file"], 'r') as f:
                file = json.load(f)

                for item in file['objects']:
                    for cdn in cdns:
                      if item['name'] == cdn['name']:
                          cdn['id'] = item['id']
    except Exception as e:
        raise e
    return cdns

def generate_genericdatacenter():
  return

def generate_networkfeed():
  return
  
def main():
    cdns = []
    try:
      with open('input.yaml', 'r') as f:
        cdns = update_uuid(yaml.safe_load(f))
    except Exception as e:
      raise e

    gdc_file = {
        "version": "1.0",
        "description": gdc["description"],
        "objects": []
    }
    for cdn in cdns:
      cdn_ips = get_cdn(cdn["url"], cdn["regex"], cdn["match_group"])
      gdc_file["objects"].append(
          gdc_create_object(name=cdn["name"],
                            uuid=cdn["id"],
                            description=cdn["description"],
                            ranges=cdn_ips))
    with open(gdc["file"], 'w') as f:
        json.dump(gdc_file, f, indent=2)
    return


if __name__ == "__main__":
    main()
