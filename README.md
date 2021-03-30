# Vaccinator
Find some Covid relief in NYC

# Running (at a Bash prompt)
`while true; do [path-to-application]/Vaccinator/main.py ;now="$(date)"; printf "Latest run at $now\n------------------------------------------------------------------------------------------------\n\n"; sleep 30; done`

Make sure to edit `config.yaml` to reflect keywords for vaccine sites you wish to display in purple or green. I've been using purple for sites I don't care about and green for those of particular interest.

This script requires Python 3.x as well as the `colorama`, `yaml`, `json`, and `requests` packages. Install with `pip`.
