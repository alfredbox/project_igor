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
    d_angle = [t['control_d_angle'] for t in data]
    plt.figure(2)
    plt.plot(times, throttle, times, angle, times, d_angle)
    plt.xlabel('Time s')
    plt.legend(['Throttle(x10)', 'Angle degs', 'd_Angle/dt (deg/s)'])

def motor_speed_trace(data): 
    times = [t['timestamp'] for t in data]
    port_rpm = [t['port_rpm'] for t in data]
    sbrd_rpm = [t['sbrd_rpm'] for t in data]
    plt.figure(3)
    plt.plot(times, port_rpm, times, sbrd_rpm)
    plt.xlabel('Time s')
    plt.legend(['Port motor speed (RPM)', 'Starbord motor speed (RPM)'])

def angle_pid_trace(data):
    times = [t['timestamp'] for t in data]
    p = [t['p'] for t in data]
    i = [t['i'] for t in data]
    d = [t['d'] for t in data]
    pid = [t['pid'] for t in data]
    plt.figure(4)
    plt.plot(times, p, times, i, times, d, times, pid)
    plt.xlabel('Time s')
    plt.legend(['P', 'I', 'D', 'PID'])
    
def make_plots(control_data, motor_data, angle_pid_data):
    sample_freq(control_data)
    throttle_angle_trace(control_data)
    motor_speed_trace(motor_data)
    angle_pid_trace(angle_pid_data)
    plt.show()

def process(filename):
    control_data = []
    motor_data = []
    angle_pid_data = []
    with open(filename, 'r') as f:
        for l in f.readlines():
            if 'DEBUG:igor:Control Data:' in l:
                s = l.replace('DEBUG:igor:Control Data:', '')
                d = json.loads(s)
                control_data.append(d)
            elif 'DEBUG:igor:Motor Speed Data' in l:
                s = l.replace('DEBUG:igor:Motor Speed Data:', '')
                d = json.loads(s)
                motor_data.append(d)
            elif 'DEBUG:igor:pid data' in l:
                s = l.replace('DEBUG:igor:pid data:', '')
                d = json.loads(s)
                angle_pid_data.append(d)
                
    make_plots(control_data, motor_data, angle_pid_data)

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
