from util import *

if len(sys.argv) < 2:
    print("Usage: python3 find_last_flow_times.py trace.txt")

in_trace, in_path, in_fname = parse_trace_filename(sys.argv[1])

i = 0
flows = {}

my_print("Reading %s..." % sys.argv[1])
with open(sys.argv[1]) as f:
    for line in f:
        if i == 0:
            start_time = float(line.strip().split()[0][6:])
        i += 1
        arr = line.strip().split()
        if len(arr) < 6:
            continue

        ts = float(arr[0][6:]) - start_time
        flow = (arr[2], arr[4], arr[5])
        flows[flow] = (ts, 1 if flows.get(flow, (0,0))[0] != ts else flows.get(flow, (0,0))[1]+1)

my_print('Writing to %s.lasttimes.txt' % in_trace)
with open('%s.lasttimes.txt' % in_trace, 'w') as outf:
    for f,res in flows.items():
        outf.write("%.6f %d %s %s %s\n" % (res[0], res[1], f[0], f[1], f[2]))

my_print("Done!")
exit(0)

