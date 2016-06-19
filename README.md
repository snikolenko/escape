# The ESCAPE code

This repository contains code for the ESCAPE counter scheme.

## Scripts for CAIDA traces

### Preprocessing

The scripts are intended to compute basic statistics for the ESCAPE counter scheme on CAIDA traces; they reproduce the figures shown in the CoNEXT 2016 submission "Exact Scalable Per-flow Packet Counting".

Before running the scripts, obtain CAIDA traces from http://www.caida.org/data/passive/passive_2016_dataset.xml (registration needed).

For each CAIDA trace `trace.pcap.gz`, run the following preprocessing:
```
gunzip trace.pcap.gz
tcpdump -qn -r trace.pcap > trace.txt
python3 conext2016_scripts/find_last_flow_times.py trace.txt
```

The `find_last_flow_times.py` script finds the last timestamp for each flow in the trace and dumps them to the file `trace.lasttimes.txt`; subsequent scripts will use these timestamps as the time when a flow closes (since there are no explicit flow-ending commands in the scripts).

### Reproducing the figures

The directory conext2016_scripts contains Python scripts that recreate the graphs from the CoNEXT 2016 submission "Exact Scalable Per-flow Packet Counting". Each script expects a `trace.txt` file and a `trace.lasttimes.txt` file generated as above. All scripts output files in the form of `figurename.trace.csv` that contain X- and Y-axis values ready to input into pgfplots. The figures are grouped into a single script if they need the same processing (e.g., go over the trace once or re-run for all polling ratios).

#### Figure 5 ("Validation of the value-sharing phenomenon"), Figure 6a ("Counters and memory")

Run
```
python3 conext2016_scripts/conext_fig5_6a.py trace.txt
```
to produce Figs. 5a, 5b, 5c, and 6a for a given trace.

#### Figures 6b and 6c ("Counters and memory")

Run
```
python3 conext2016_scripts/conext_fig6b_6c.py trace.txt
```
to produce Figs. 6a and 6b for a given trace.

#### Figure 7a ("Polling configurations and ESCAPE processing complexity")

Run
```
python3 conext2016_scripts/conext_fig7a.py trace.txt
```
to produce Fig. 7a for a given trace.


#### Figure 7b ("Polling configurations and ESCAPE processing complexity")

Run
```
python3 conext2016_scripts/conext_fig7b.py trace.txt
```
to produce Fig. 7b for a given trace. Note that this will take longest to generate among all figures since it re-runs trace processing with different polling rates.

#### Figure 7c ("Polling configurations and ESCAPE processing complexity")

Run
```
python3 conext2016_scripts/conext_fig7c.py trace.txt
```
to produce Fig. 7c for a given trace. Note that this will take longer than the other figures (except 7b).

