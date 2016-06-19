# The ESCAPE code

This repository contains code for the ESCAPE counter scheme.

## Scripts for CAIDA traces

### Preprocessing

The scripts are intended to compute basic statistics for the ESCAPE counter scheme on CAIDA traces; they reproduce the figures shown in the CoNEXT 2016 submission "Exact Scalable Per-flow Packet Counting".

Before running the scripts, obtain CAIDA traces from 
http://www.caida.org/data/passive/passive_2016_dataset.xml.

For each CAIDA trace `trace.pcap.gz`, run the following preprocessing:
```
gunzip trace.pcap.gz
tcpdump -qn -r trace.pcap > trace.txt
python3 conext2016_scripts/find_last_flow_times.py trace.txt
```

The `find_last_flow_times.py` script finds the last timestamp for each flow in the trace and sets them; later scripts will use these timestamps as the time when a flow closes (since there are no explicit trace-ending commands in the scripts).

### Reproducing the figures in the submission

The directory conext2016_scripts contains Python scripts that recreate the graphs from the CoNEXT 2016 submission "Exact Scalable Per-flow Packet Counting". Each script expects a `trace.txt` file and a `trace.lasttimes.txt` file generated as above. All scripts output files in the form of `figurename.trace.csv` that contain X- and Y-axis values ready to input into pgfplots.

#### Figure 5: Validation of the value-sharing phenomenon




