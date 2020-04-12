import argparse
import json
import matplotlib.pyplot as plt
import os
import sys

def sample_freq(data):
    times = [t['timestamp'] for t in data]
    last = None
    durations = []
    for t in times:
        if last is not None:
            durations.append(t - last)
        last = t
    if times:
        times.pop()
        plt.figure(1)
        plt.plot(times, durations)
        plt.xlabel('Time s')
        plt.ylabel('dt s')


def throttle_angle_trace(data): 
    times = [t['timestamp'] for t in data]
    throttle = [t['set_throttle']*10. for t in data]
    angle = [t['control_angle'] for t in data]
    plt.figure(2)
    plt.plot(times, throttle, times, angle)
    plt.xlabel('Time s')
    plt.legend(['Throttle(x10)', 'Angle degs'])


def make_plots(data):
    sample_freq(data)
    throttle_angle_trace(data)
    plt.show()
    

def process(filename):
    data = []
    with open(filename, 'r') as f:
        for l in f.readlines():
            if 'DEBUG:igor:Control Data:' in l:
                s = l.replace('DEBUG:igor:Control Data:', '')
                d = json.loads(s)
                data.append(d)
    make_plots(data)

def latest(directory):
    fl = os.listdir(directory)
    fl.sort()
    fl.reverse()
    for f in fl:
        if "igor" in f:
            return os.path.join(directory, f)

    return None

def main():
    parser = argparse.ArgumentParser(description='Process a log file created by Igor')
    parser.add_argument('-l',
                        '--log',
                        default=None,
                        help='Path to the log file to be processed')
    parser.add_argument('-d',
                        '--directory',
                        default=None,
                        help='Path to the log file to be processed')

    args = parser.parse_args()
    log = args.log if args.log is not None else latest(args.directory)
    process(log)

if __name__ == "__main__":
    sys.exit(main())
