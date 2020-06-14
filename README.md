# Hetzner Dynamic DNS Updater

This script finds this machine's hostname, public IPv4 and IPv6 addresses,
then updates the corresponding DNS records on Hetzner.

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

1. Install `python3` and `pip`:

    apt install python3

2. Install package dependencies:

    pip install docopt

3. Clone the repository somewhere:

    cd /opt
    git clone https://github.com/iSoron/hetzner-ddns.git

4. Install the script system-wide:

    cd hetzner-ddns
    sudo make install

5. Create a configuration file in `/etc/hetzner-ddns.conf` with you API token. See `/etc/hetzner-ddns.conf.example` for an example.

6. Run script and enable it during boot:

    sudo systemctl start hetzner-ddns
    sudo systemctl enable hetzner-ddns

## License

MIT
