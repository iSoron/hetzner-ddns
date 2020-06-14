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

## License

MIT