install:
	cp hetzner-ddns.py /usr/local/bin
	cp etc/hetzner-ddns.conf.example /etc
	cp etc/systemd/hetzner-ddns.service /etc/systemd/system/

uninstall:
	rm /usr/local/bin/hetzner-ddns.py
	rm /etc/hetzner-ddns.conf.example
	rm /etc/systemd/system/hetzner-ddns.service

enable:
	systemctl enable hetzner-ddns

disable:
	systemctl disable hetzner-ddns

start:
	systemctl start hetzner-ddns

