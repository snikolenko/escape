from util import *

## Values of the static counter 
STATIC_VALUES = [ 0, 8, 16, 24, 32, 48, 64, 72, 96, 102, 128, 192, 256, 256+128, 512, 756, 1024, 1536, 2048, 3072, 4096 ]

if len(sys.argv) < 2:
	print("Usage: python3 conext_fig5_6a.py trace.txt")

in_trace, in_path, in_fname = parse_trace_filename(sys.argv[1])

my_print("Trace: %s" % in_trace)
my_print("Loading last flow times from %s.lasttimes.txt..." % in_fname)
lasttimes = load_lasttimes('%s.lasttimes.txt' % in_fname)
my_print("Reading packets with period %f s..." % (GRAPH_RESOLUTION) )

flow_counts = Counter()
max_len_counts = 0
max_len_counts_ts = 0.0
max_counts = Counter()
current_deleted = {}
# kk = ('177.186.72.37.7300', '202.205.213.145.13434:', 'UDP,')

with open(in_fname) as f:
	with open('fig5a.%s.csv' % in_trace, 'w') as outf:
		cur_packet = get_packet(f.readline())
		begin_time = 0.0
		first_packet_num = 0
		total_deleted = 0
		first_packet_ts = cur_packet[0]
		outf.write('%f %f\n' % ( 0.0, 0.0 ))
		arr_packets = [cur_packet]
		total_packets = 0
		for line in f:
			cur_packet = get_packet(line)
			cur_ts = cur_packet[0] - first_packet_ts
			if cur_ts - begin_time > GRAPH_RESOLUTION:
				begin_time = arr_packets[-1][0] - first_packet_ts
				current_counts = Counter([ x[1] for x in arr_packets if not x[1] in current_deleted ])
				flow_counts.update(current_counts)
				res_total_counters = len(set(flow_counts.values()))
				if res_total_counters > max_len_counts:
					max_len_counts = res_total_counters
					max_len_counts_ts = cur_ts
					max_counts = copy.deepcopy(flow_counts)
				my_print("\t[%f] packets %d -- %d, %d flows, %d total, with %d values [deleted %d]" % (begin_time, total_packets, total_packets + len(arr_packets), len(current_counts), len(flow_counts), res_total_counters, total_deleted) )
				total_packets += len(arr_packets)
				arr_packets = []
				current_deleted = {}
				outf.write( '%f %f\n' % (begin_time, float(0.001 + len(flow_counts)) / float(0.001 + res_total_counters) ) )
			if cur_ts - lasttimes[cur_packet[1]] > -0.000005:
				del flow_counts[cur_packet[1]]
				current_deleted[cur_packet[1]] = True
				total_deleted += 1
			else:
				arr_packets.append(cur_packet)
		current_counts = Counter([ x[1] for x in arr_packets if not x[1] in current_deleted ])
		flow_counts.update(current_counts)
		res_total_counters = len(set(flow_counts.values()))
		my_print("\t[%f] packets %d -- %d, %d flows, %d total, with %d values [deleted %d]" % (begin_time, total_packets, total_packets + len(arr_packets), len(current_counts), len(flow_counts), res_total_counters, total_deleted) )
		outf.write( '%f %f\n' % (begin_time, float(0.001 + len(flow_counts)) / float(0.001 + res_total_counters) ) )


my_print("Preparing Figures 5b and 5c at time %f" % max_len_counts_ts)
counts_reverse = {}
for k, v in max_counts.items():
    counts_reverse[v] = counts_reverse.get(v, 0) + 1
counts_reverse_plot = [ counts_reverse.get(i, 0) for i in range(1, max(counts_reverse.keys())+1) ]
counts_reverse_plot = [ x for i,x in enumerate(counts_reverse_plot) if i==0 or i==len(counts_reverse_plot)-1 or counts_reverse_plot[i-1] > 0 or counts_reverse_plot[i] > 0 or counts_reverse_plot[i+1] > 0 ]

with open('fig5b.%s.csv' % in_trace, 'w') as outf:
	outf.write("\n".join([ "%d %d" % (i+1, v) for i,v in enumerate(counts_reverse_plot) ]))

cntrc = np.cumsum(counts_reverse_plot)
cntrc_plot = [ (i, cntrc[i]) for i in range(100) ] + [ (i, cntrc[i]) for i in np.arange(100,min(1000, len(cntrc)-1),10) ] + [ (i, cntrc[i]) for i in np.arange(1000,len(cntrc)-1,100) ]

with open('fig5c.%s.csv' % in_trace, 'w') as outf:
	outf.write("\n".join([ "%d %d" % (i[0]+1, i[1]) for i in cntrc_plot ]))

my_print("Preparing Figure 6a at time %f" % max_len_counts_ts)

counts_reverse = {}
for k, v in max_counts.items():
    counts_reverse[v] = counts_reverse.get(v, 0) + 1

with open('fig6a.%s.csv' % in_trace, 'w') as outf:
	outf.write("\n".join([ "%d %.4f" % (s, float(0.001 + len([ k for k,v in max_counts.items() if v > s ])) / float(0.001 + len([ k for k in counts_reverse if k > s ])) ) for s in STATIC_VALUES ]))

my_print("All done!")



