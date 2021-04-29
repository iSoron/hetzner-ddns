#!/usr/bin/env python3
"""Hetzner Dynamic DNS Updater

This script finds this machine's hostname, public IPv4 and IPv6 addresses,
then updates the corresponding DNS records on Hetzner.

Usage:
  hetzner-ddns.py [options]

Options:
  -h --help             Show this screen
  --token=<str>         Hetzner API Token
  --zone=<str>          Name of the DNS zone
  --hostname=<std>      This machine's hostname
  --ttl=<n>             Time-to-live in seconds
  --v4-api=<url>        API that returns your public IPv4 address
  --v6-api=<url>        API that returns your public IPv6 address
  --retry-attempts=<n>  Retry N times if connection fails
  --retry-delay=<s>     Wait S seconds between attempts
  --config=<file>       Read options from configuration file
  --disable-v4          Do not update IPv4 address
  --disable-v6          Do not update IPv6 address
  --repeat=<s>          Update DNS again every S seconds
"""

from docopt import docopt
from time import sleep
import json
import os
import requests
import socket
import sys
import configparser
import time


args = docopt(__doc__)


def merge_config_file():
    global args
    basepath = os.path.dirname(os.path.abspath(__file__))
    candidate_config_files = [
        args["--config"],
        os.path.join(basepath, "hetzner-ddns.conf"),
        "/etc/hetzner-ddns.conf",
    ]

    for filename in candidate_config_files:
        if filename is None:
            continue
        if os.path.isfile(filename):
            print("Reading options from %s" % filename)
            config = configparser.ConfigParser()
            config.read(filename)

            section_name = config.sections()[0]
            print("    %-20s %s" % ("--zone", section_name))
            args["--zone"] = section_name

            section = config[section_name]
            for key in args.keys():
                if key[2:] in section:
                    value = section[key[2:]]
                    print("    %-20s %s" % (key, value))
                    args[key] = value

    return args


def merge_defaults():
    global args
    default_args = {
        "--ttl": 300,
        "--v4-api": "https://v4.ident.me/",
        "--v6-api": "https://v6.ident.me/",
        "--retry-attempts": 12,
        "--retry-delay": 5,
        "--hostname": socket.gethostname(),
        "--repeat": 3600,
    }

    print("Applying default options:")
    for (key, value) in default_args.items():
        if args[key] is None:
            print("    %-20s %s" % (key, value))
            args[key] = value


merge_config_file()

if args["--token"] is None:
    print("API token must be provided")
    sys.exit(1)

if args["--zone"] is None:
    print("DNS zone must be provided")
    sys.exit(1)

merge_defaults()


def get_addr(
    url, retry=int(args["--retry-attempts"]), delay=int(args["--retry-delay"])
):
    exception = None
    for i in range(retry):
        try:
            import urllib

            txt = urllib.request.urlopen(url).read()
            return txt.decode("utf-8")
        except Exception as e:
            exception = e
            print("    connection failed, retrying in %d seconds..." % delay)
            sleep(delay)
    raise (exception)


def get_all_records(zone):
    response = requests.get(
        url="https://dns.hetzner.com/api/v1/records",
        params={"zone_id": zone["id"]},
        headers={"Auth-API-Token": args["--token"]},
    )
    return response.json()["records"]


def get_all_zones():
    response = requests.get(
        url="https://dns.hetzner.com/api/v1/zones",
        headers={"Auth-API-Token": args["--token"]},
    )
    return response.json()["zones"]


def find_record(zone, name, kind="AAAA"):
    all_records = get_all_records(zone)
    for r in all_records:
        if r["type"] == kind and r["name"] == name:
            return r
    return None


def find_zone(name):
    all_zones = get_all_zones()
    for z in all_zones:
        if z["name"] == name:
            return z
    raise (Exception("Zone not found: %s" % name))


def update_record(record):
    response = requests.put(
        url="https://dns.hetzner.com/api/v1/records/%s" % record["id"],
        headers={
            "Content-Type": "application/json",
            "Auth-API-Token": args["--token"],
        },
        data=json.dumps(record),
    )
    response.raise_for_status()


def create_record(record):
    response = requests.post(
        url="https://dns.hetzner.com/api/v1/records",
        headers={
            "Content-Type": "application/json",
            "Auth-API-Token": args["--token"],
        },
        data=json.dumps(record),
    )
    response.raise_for_status()


def delete_record(rid):
    response = requests.delete(
        url=f"https://dns.hetzner.com/api/v1/records/{rid}",
        headers={
            "Content-Type": "application/json",
            "Auth-API-Token": args["--token"],
        }
    )
    response.raise_for_status()


def main():
    kinds = []
    delay = int(args["--repeat"])

    if not bool(args["--disable-v4"]):
        kinds += ["A"]

    if not bool(args["--disable-v6"]):
        kinds += ["AAAA"]

    print("Finding DNS zone...")
    zone = find_zone(args["--zone"])

    while True:
        for kind in kinds:
            if kind == "A":
                print("Finding public IPv4 address...")
                addr = get_addr(args["--v4-api"])
                print("    %s" % addr)
            else:
                print("Finding public IPv6 address...")
                addr = get_addr(args["--v6-api"])
                print("    %s" % addr)

            print("Finding existing %s record..." % kind)
            rec = find_record(zone=zone, kind=kind, name=args["--hostname"])

            if rec is not None:
                if rec["value"] == addr:
                    print("Existing record is up-to-date")
                    continue

                print("Deleting existing %s record..." % kind)
                delete_record(rec["id"])
                print("    done")

            print("Creating new %s record..." % kind)
            create_record(
                {
                    "value": addr,
                    "type": kind,
                    "name": args["--hostname"],
                    "zone_id": zone["id"],
                    "ttl": args["--ttl"],
                }
            )
            print("    done")

        print(f"Sleeping for {delay} seconds...")
        time.sleep(delay)

main()
