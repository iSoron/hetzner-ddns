# Hetzner Dynamic DNS Updater

This script finds this machine's hostname, public IPv4 and IPv6 addresses,
then updates the corresponding DNS records on Hetzner.

**Note:** *This script is not developed, maintained or supported by Hetzner.*

## Usage

```text
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
```

## Running during boot

The instructions below were tested on Ubuntu Linux 20.04 LTS. 

1. Install Python and pip:

```
sudo apt install python3 python3-pip
```

2. Install package dependencies:

```
sudo pip3 install docopt
```

3. Clone the repository somewhere:

```
git clone https://github.com/iSoron/hetzner-ddns.git
```

4. Install the script system-wide:

```
cd hetzner-ddns
sudo make install
```

5. Create a configuration file in `/etc/hetzner-ddns.conf` with you API token. See `/etc/hetzner-ddns.conf.example` for an example.

6. Run script and enable it during boot:

```
sudo make start
sudo make enable
```

## License

MIT
