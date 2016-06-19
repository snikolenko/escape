from util import *

if len(sys.argv) < 2:
	print("Usage: python3 conext_fig7b.py trace.txt")

## Values of the polling rate for plotting
POLLING_RATES = [ 50, 100, 200, 300, 400, 500, 750, 1000, 2000, 3000, 4000, 5000, 10000 ]

in_trace, in_path, in_fname = parse_trace_filename(sys.argv[1])

my_print("Trace: %s" % in_trace)
my_print("Loading last flow times from %s.lasttimes.txt..." % in_fname)
lasttimes = load_lasttimes('%s.lasttimes.txt' % in_fname)


with open('fig7b.%s.csv' % in_trace, 'w') as outf:
	for polling_rate in POLLING_RATES:
		my_print("Starting polling rate %d!" % polling_rate)
		with open(in_fname) as f:
			flow_counts = Counter()
			flows = {}
			max_len_counts = 0
			max_len_counts_ts = 0.0
			current_deleted = {}
			cur_packet = get_packet(f.readline())
			begin_time = 0.0
			first_packet_num = 0
			total_deleted = 0
			first_packet_ts = cur_packet[0]
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
					my_print("\t[%f] packets %d -- %d, %d flows, %d total, with %d values [deleted %d]" % (begin_time, total_packets, total_packets + len(arr_packets), len(current_counts), len(flow_counts), res_total_counters, total_deleted) )

					# polling
					flows_to_delete = sorted(flows.items(), key=itemgetter(1))[:int(polling_rate * GRAPH_RESOLUTION)]
					for flow in flows_to_delete:
						del flows[flow[0]]
						del flow_counts[flow[0]]

					total_packets += len(arr_packets)
					arr_packets = []
					current_deleted = {}
				if cur_ts - lasttimes[cur_packet[1]] > -0.000005:
					del flow_counts[cur_packet[1]]
					current_deleted[cur_packet[1]] = True
					total_deleted += 1
				else:
					if not cur_packet[1] in flows:
						flows[cur_packet[1]] = cur_packet[0]
					arr_packets.append(cur_packet)
			current_counts = Counter([ x[1] for x in arr_packets if not x[1] in current_deleted ])
			flow_counts.update(current_counts)
			res_total_counters = len(set(flow_counts.values()))
			outf.write( '%d %d\n' % (polling_rate, max_len_counts) )
			outf.flush()

my_print("Done!")



