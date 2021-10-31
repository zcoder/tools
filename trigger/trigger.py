#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import argparse
from time import sleep
import socket
import sys

hostname=socket.gethostname()

parser = argparse.ArgumentParser(description='trigger an action on condition')
parser.add_argument('--cmd', dest='cmd', default='echo "cmd"', help='bash cmd to run')
parser.add_argument('--condition', dest='condition', default='true; echo $?', help='condition for check')
parser.add_argument('--cresult', dest='cresult', default='0', help='condition result for trigger')
parser.add_argument('--ccounts', dest='ccounts', default=10, type=int, help='condition counts for trigger')
parser.add_argument('--duration', dest='duration', default=5, type=int, help='what duration (in seconds) for check condition')
parser.add_argument('--cmd_duration', dest='cmd_duration', default=120, type=int, help='what duration (in seconds) for rerun checks')
parser.add_argument('--allow_flap', dest='allow_flap', default=False, type=bool, help='allow flap of checks ?')
parser.add_argument('--debug', dest='debug', default=False, type=bool, help='debug ?')


debug_args = [
    '--cmd','echo "$(date) triggered link"',
    '--condition', "echo 'Link detected: yes' | grep 'Link detected:' | grep 'yesd' &>/dev/null || echo down",
    '--cresult', 'down',
]


args = parser.parse_args(None)

DEBUG=args.debug

if DEBUG: print(args)

def check_condition(condition, cresult):
    p = subprocess.Popen(f'bash -c "{condition}"', stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    if p_status != 0:
        print(f'Error exec [bash -c "{condition}"]: {err} ({output}). Exit code {p_status}')
        exit(p_status)
    output_result = output.decode().strip()
    if DEBUG: print(f'bash -c "{condition}"')
    if DEBUG: print(output_result)
    sys.stdout.flush()
    return cresult == output_result

def run_cmd(cmd):
    p = subprocess.Popen(f'{cmd}', stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    if p_status != 0:
        print(f'Error exec ["{cmd}"]: {err} ({output}). Exit code {p_status}')
        exit(p_status)
    output_result = output.decode().strip()
    if DEBUG: print(f'"{cmd}"')
    if DEBUG: print(output_result)
    return output_result


def main():
    curr_ccounts=0
    while True:
        while curr_ccounts<args.ccounts:
            if check_condition(args.condition, args.cresult):
                curr_ccounts+=1
                if DEBUG: print(f'+1 triggered condition')
                sys.stdout.flush()
            elif not args.allow_flap:
                curr_ccounts=0
            sleep(args.duration)

        curr_ccounts = 0
        run_cmd(args.cmd)
        sleep(args.cmd_duration)


if __name__ == '__main__':
    main()
