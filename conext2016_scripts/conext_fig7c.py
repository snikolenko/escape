from util import *

if len(sys.argv) < 2:
	print("Usage: python3 conext_fig7c.py trace.txt")

## Values of the number of static counters S for plotting
STATIC_VALUES = [ 0, 64, 128, 256, 256+128, 512, 756, 1024, 1536, 2048, 2048+128, 2048+2*128, 2048+512, 2048+2*128+512, 3072, 3072+256, 3072+512, 4096, 4096+256, 4096+512,4096+512+256,4096+1024 ]

in_trace, in_path, in_fname = parse_trace_filename(sys.argv[1])

my_print("Trace: %s" % in_trace)
my_print("Loading last flow times from %s.lasttimes.txt..." % in_fname)
lasttimes = load_lasttimes('%s.lasttimes.txt' % in_fname)

flow_counts = {}
inv_counts = {}
max_len_counts = 0
max_len_counts_ts = 0.0
max_counts = Counter()

total_access_times = { s : 0 for s in STATIC_VALUES }
max_memory = { s : 0 for s in STATIC_VALUES }

def access_times(num_static, num, cur, cur_prev, cur_next):
	if num < num_static:
		return 1
	elif num == num_static:
		if cur_next > 0:
			return 3
		else:
			return 4
	else:
		if (cur == 1 and cur_next == 0) or (cur > 1 and cur_next > 0):
			return 3
		else:
			return 5

def dec_inv(num):
	if num == 0:
		return
	cur = inv_counts[num]
	if cur == 1:
		del inv_counts[num]
	else:
		inv_counts[num] = cur - 1	

def poll_flow(flow):
	num = flow_counts[flow]
	dec_inv(num)
	del flow_counts[flow]

with open(sys.argv[1]) as f:
	cur_packet = get_packet(f.readline())
	begin_time = 0.0
	first_packet_num = 0
	total_deleted = 0
	first_packet_ts = cur_packet[0]
	total_packets = 0
	for line in f:
		cur_packet = get_packet(line)
		cur_ts = cur_packet[0] - first_packet_ts
		total_packets += 1

		### counting memory accesses
		num = flow_counts.get(cur_packet[1], 0)
		cur, cur_prev, cur_next = inv_counts.get(num, 0), inv_counts.get(num-1, 0), inv_counts.get(num+1, 0)
		for s in STATIC_VALUES:
			total_access_times[s] = total_access_times[s] + access_times(s, num, cur, cur_prev, cur_next)

		### updating
		flow_counts[cur_packet[1]] = num+1
		dec_inv(num)
		inv_counts[num+1] = inv_counts.get(num+1, 0) + 1

		if cur_ts - lasttimes[cur_packet[1]] > -0.000005:
			poll_flow(cur_packet[1])
			total_deleted += 1

		### progress
		if cur_ts - begin_time > GRAPH_RESOLUTION:
			begin_time = cur_ts
			my_print("\t[%f] packet %d" % (begin_time, total_packets) )


with open('fig7c.%s.csv' % in_trace, 'w') as outf:
	outf.write("\n".join([ "%d %.4f" % (s, float(total_access_times[s]) / float(total_packets) ) for s in STATIC_VALUES ]))

my_print("All done!")



