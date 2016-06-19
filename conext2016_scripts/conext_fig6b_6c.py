from util import *

if len(sys.argv) < 2:
	print("Usage: python3 conext_fig6b_6c.py trace.txt")

## Values of the static counter 
STATIC_VALUES = [ 0, 64, 256, 1024, 2048, 4096 ]

in_trace, in_path, in_fname = parse_trace_filename(sys.argv[1])

my_print("Trace: %s" % in_trace)
my_print("Loading last flow times from %s.lasttimes.txt..." % in_fname)
lasttimes = load_lasttimes('%s.lasttimes.txt' % in_fname)

logM = 16
logL = 16
logN = 16

def memory_pfl(num_static, num_flows):
	return (num_static * logM + num_flows * logM) / 1024

def memory_escape(num_static, num_counters):
	return (num_static * logM + num_counters * ( logN + logM + 2 * logL )) / 1024


flow_counts = Counter()
max_len_counts = 0
max_len_counts_ts = 0.0
max_counts = Counter()
current_deleted = {}
# kk = ('177.186.72.37.7300', '202.205.213.145.13434:', 'UDP,')

for num_static in STATIC_VALUES:
	with open('fig6b.dyn.S%d.%s.csv' % (num_static, infname), 'w') as outf:
		pass
	with open('fig6b.pfl.S%d.%s.csv' % (num_static, infname), 'w') as outf:
		pass
	with open('fig6c.dyn.S%d.%s.csv' % (num_static, infname), 'w') as outf:
		pass
	with open('fig6c.pfl.S%d.%s.csv' % (num_static, infname), 'w') as outf:
		pass

my_print("Reading packets with period %f s..." % (GRAPH_RESOLUTION) )
with open(in_fname) as f:
	cur_packet = get_packet(f.readline())
	begin_time = 0.0
	first_packet_num = 0
	total_deleted = 0
	first_packet_ts = cur_packet[0]
	with open('fig6b.base.%s.csv' % (infname), 'a') as outf:
		outf.write( '%f %d\n' % (0.0, 0) )
	with open('fig6c.base.%s.csv' % (infname), 'a') as outf:
		outf.write( '%f %f\n' % (0.0, 0.0) )
	for num_static in STATIC_VALUES:
		num_extra_flows = len([x for x,v in flow_counts.items() if v > num_static])
		with open('fig6b.pfl.S%d.%s.csv' % (num_static, infname), 'a') as outf:
			outf.write( '%f %d\n' % (0.0, 0) )
		with open('fig6c.base.S%d.%s.csv' % (num_static, infname), 'a') as outf:
			outf.write( '%f %f\n' % (0.0, 0.0) )
		with open('fig6c.dyn.S%d.%s.csv' % (num_static, infname), 'a') as outf:
			outf.write( '%f %f\n' % (0.0, 0.0) )
		with open('fig6c.pfl.S%d.%s.csv' % (num_static, infname), 'a') as outf:
			outf.write( '%f %f\n' % (0.0, 0.0) )
	arr_packets = [cur_packet]
	total_packets = 0
	for line in f:
		cur_packet = get_packet(line)
		cur_ts = cur_packet[0] - first_packet_ts
		if cur_ts - begin_time > GRAPH_RESOLUTION:
			begin_time = arr_packets[-1][0] - first_packet_ts
			current_counts = Counter([ x[1] for x in arr_packets if not x[1] in current_deleted ])
			flow_counts.update(current_counts)
			all_counters = list(set(flow_counts.values()))
			my_print("\t[%f] packets %d -- %d, %d flows, %d total, with %d values [deleted %d]" % (begin_time, total_packets, total_packets + len(arr_packets), len(current_counts), len(flow_counts), len(all_counters), total_deleted) )
			total_packets += len(arr_packets)
			arr_packets = []
			current_deleted = {}
			with open('fig6b.base.%s.csv' % (infname), 'a') as outf:
				outf.write( '%f %d\n' % (begin_time, len(flow_counts)) )
			with open('fig6c.base.%s.csv' % (infname), 'a') as outf:
				outf.write( '%f %f\n' % (begin_time, len(flow_counts) * logM / 1024) )
			for num_static in STATIC_VALUES:
				num_extra_flows = len([x for x,v in flow_counts.items() if v > num_static])
				num_extra_counters = len([x for x in all_counters if x > num_static])
				with open('fig6b.dyn.S%d.%s.csv' % (num_static, infname), 'a') as outf:
					outf.write( '%f %d\n' % (begin_time, num_static + num_extra_counters) )
				with open('fig6b.pfl.S%d.%s.csv' % (num_static, infname), 'a') as outf:
					outf.write( '%f %d\n' % (begin_time, num_static + num_extra_flows) )
				with open('fig6c.dyn.S%d.%s.csv' % (num_static, infname), 'a') as outf:
					outf.write( '%f %f\n' % (begin_time, memory_escape(num_static, num_extra_counters) ) )
				with open('fig6c.pfl.S%d.%s.csv' % (num_static, infname), 'a') as outf:
					outf.write( '%f %f\n' % (begin_time, memory_pfl(num_static, num_extra_flows) ) )

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
	with open('fig6b.base.%s.csv' % (infname), 'a') as outf:
		outf.write( '%f %d\n' % (begin_time, len(flow_counts)) )
	with open('fig6c.base.%s.csv' % (infname), 'a') as outf:
		outf.write( '%f %f\n' % (begin_time, len(flow_counts) * logM / 1024) )
	for num_static in STATIC_VALUES:
		num_extra_flows = len([x for x,v in flow_counts.items() if v > num_static])
		num_extra_counters = len([x for x in all_counters if x > num_static])
		with open('fig6b.dyn.S%d.%s.csv' % (num_static, infname), 'a') as outf:
			outf.write( '%f %d\n' % (begin_time, num_static + num_extra_counters) )
		with open('fig6b.pfl.S%d.%s.csv' % (num_static, infname), 'a') as outf:
			outf.write( '%f %d\n' % (begin_time, num_static + num_extra_flows) )
		with open('fig6c.dyn.S%d.%s.csv' % (num_static, infname), 'a') as outf:
			outf.write( '%f %f\n' % (begin_time, memory_escape(num_static, num_extra_counters) ) )
		with open('fig6c.pfl.S%d.%s.csv' % (num_static, infname), 'a') as outf:
			outf.write( '%f %f\n' % (begin_time, memory_pfl(num_static, num_extra_flows) ) )

my_print("Done!")

