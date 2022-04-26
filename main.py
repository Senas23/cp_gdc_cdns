#!/usr/bin/env python3
import requests, re, json, logging, uuid, os, random, yaml
from ipaddress import ip_network
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

def parse_results(reg: re, match_group: int, results: list) -> list:
  tmp_result = []
  for line in results:
    for match in re.finditer(reg, line, re.IGNORECASE):
      # Validate Network
      network = ip_network(match.group(match_group))
      tmp_result.append(str(network))
  return tmp_result


def get_cdn(url: list, reg: re, match_group: int) -> list:
    reg_result = []
    for item in url:
        try:
            logging.warning(f'[*] Request for: {item}')
            headers = {'User-Agent': random.choice(user_agent_list)}
            res = requests.get(item, verify=True, timeout=30, headers=headers)
            if res.status_code == 200:
                reg_result.extend(parse_results(reg, match_group, res.text.splitlines()))
            else:
                logging.warning(f"[*] Could not fetch from {item}")
        except (NewConnectionError, ConnectionError, MaxRetryError,
                RequestException):
            logging.error(f"[*] Connection exception in get_cdn() for {item}")
            exit(1)
        except (ValueError):
            logging.error(f"[*] Invalid network found in get_cdn() for {item}")
            exit(1)
        except Exception:
            logging.error(f"[*] General Error exception in get_cdn() for {item}")
            exit(1)
    return reg_result


def create_json_object(name: str, uuid: str, description: str,
                      ranges: list) -> dict:
    return {
        "name": name,
        "id": uuid,
        "description": description,
        "ranges": ranges
    }


def update_uuid(cdns: list):
    file = {}
    for cdn in cdns:
      cdn['id'] = str(uuid.uuid4())

    if os.path.isfile(gdc["file"]):
        with open(gdc["file"], 'r') as f:
            file = json.load(f)

            for item in file['objects']:
                for cdn in cdns:
                  if item['name'] == cdn['name']:
                      cdn['id'] = item['id']
    return cdns, file


def main():
    cdns = []
    with open('inputs.cdnql', 'r') as f:
      cdns, previous_cdns_output = update_uuid(yaml.safe_load(f))

    gdc_file = {
        "version": "1.0",
        "description": gdc["description"],
        "objects": []
    }
    for cdn in cdns:
      cdn_ips = get_cdn(cdn["url"], cdn["regex"], cdn["match_group"])
      gdc_file["objects"].append(
          create_json_object(name=cdn["name"],
                            uuid=cdn["id"],
                            description=cdn["description"],
                            ranges=cdn_ips))
    
    if gdc_file != previous_cdns_output:
      with open(gdc["file"], 'w') as f:
          json.dump(gdc_file, f, indent=2)


if __name__ == "__main__":
    main()
