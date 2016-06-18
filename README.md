# The ESCAPE code

This repository contains code for the ESCAPE counter scheme.

## Scripts for CAIDA traces

### Preprocessing

The scripts are intended to compute basic statistics for the ESCAPE counter scheme on CAIDA traces; they reproduce the figures shown in the CoNEXT 2016 submission on ESCAPE.

Before running the scripts, obtain CAIDA traces from 
http://www.caida.org/data/passive/passive_2016_dataset.xml.

For each CAIDA trace `trace.pcap.gz`, run the following preprocessing:
```
gunzip trace.pcap.gz
tcpdump -qn -r trace.pcap > trace.txt
'''

The directory conext2016_scripts contains the following scripts
 

