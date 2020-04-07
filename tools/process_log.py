import argparse
import json
import matplotlib.pyplot as plt
import sys

def sample_freq(data):
    times = [t['timestamp'] for t in data]
    last = None
    durations = []
    for t in times:
        if last is not None:
            durations.append(t - last)
        last = t
    times.pop()
    plt.plot(times, durations)
    plt.show()

def throttle_angle_trace(data): 
    times = [t['timestamp'] for t in data]
    throttle = [t['set_throttle'] for t in data]
    angle = [t['control_angle'] for t in data]
    plt.plot(times, throttle, times, angle)
    plt.show()


def make_plots(data):
    sample_freq(data)
    throttle_angle_trace(data)
    

def process(filename):
    data = []
    with open(filename, 'r') as f:
        for l in f.readlines():
            if 'DEBUG:Igor:Control Data:' in l:
                s = l.replace('DEBUG:Igor:Control Data:', '')
                d = json.loads(s)
                data.append(d)
    make_plots(data)


def main():
    parser = argparse.ArgumentParser(description='Process a log file created by Igor')
    parser.add_argument('-l',
                        '--log',
                        required=True,
                        help='Path to the log file to be processed')
    args = parser.parse_args()
    process(args.log)

if __name__ == "__main__":
    sys.exit(main())
