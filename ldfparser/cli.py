"""Command Line Interface
"""
import argparse
import json
import os
import sys

from ldfparser import LDF, LinFrame, LinMaster, LinSignal, LinSlave, parseLDF

def auto_int(number):
    return int(number, 0)

def exit_with_error(code: int, message: str):
    print(message, file=sys.stderr)
    sys.exit(code)

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--ldf', required=True)
    parser.add_argument('-e', '--encoding', required=False, default='utf-8')
    subparser = parser.add_subparsers(dest="subparser_name")

    infoparser = subparser.add_parser('info')
    infoparser.add_argument('--details', action='store_true')

    exportparser = subparser.add_parser('export')
    exportparser.add_argument('--output', required=False, default=None)

    nodeparser = subparser.add_parser('node')
    nodearggroup = nodeparser.add_mutually_exclusive_group()
    nodearggroup.add_argument('--list', action="store_true")
    nodearggroup.add_argument('--master', action="store_true")
    nodearggroup.add_argument('--slave', type=str)

    frameparser = subparser.add_parser('frame')
    framearggroup = frameparser.add_mutually_exclusive_group()
    framearggroup.add_argument('--list', action="store_true")
    framearggroup.add_argument('--id', type=auto_int)
    framearggroup.add_argument('--name', type=str)

    signalparser = subparser.add_parser('signal')
    signalarggroup = signalparser.add_mutually_exclusive_group()
    signalarggroup.add_argument('--list', action="store_true")
    signalarggroup.add_argument('--name', type=str)

    return parser.parse_args(args)

def main():
    args = parse_args(sys.argv[1:])
    ldf = parseLDF(args.ldf, encoding=args.encoding)

    if args.subparser_name is None:
        print_ldf_info(ldf)
    elif args.subparser_name == 'info':
        print_ldf_info(ldf, args.details)
    elif args.subparser_name == 'export':
        export_ldf(ldf, args.output)
    elif args.subparser_name == 'node':
        handle_node_subcommand(args, ldf)
    elif args.subparser_name == 'frame':
        handle_frame_subcommand(args, ldf)
    elif args.subparser_name == 'signal':
        handle_signal_subcommand(args, ldf)
    else:
        exit_with_error(1, f"Unknown subcommand {args.subparser_name}")
    exit(0)

def handle_node_subcommand(args, ldf: LDF):
    if args.list:
        print(f"{ldf.master.name} (master)")
        for node in ldf.slaves:
            print(node.name)
    elif args.master:
        print_master_info(ldf.master)
    else:
        if not ldf.slave(args.slave):
            exit_with_error(1, f"Slave '{args.slave}' not found.")
        print_slave_info(ldf.slave(args.slave))

def handle_frame_subcommand(args, ldf: LDF):
    if args.list:
        for frame in ldf.frames:
            print(frame.name)
    elif args.id:
        if not ldf.frame(args.id):
            exit_with_error(1, f"Frame with id '{args.id}' not found.")
        print_frame_info(ldf.frame(args.id))
    else:
        if not ldf.frame(args.name):
            exit_with_error(1, f"Frame with name '{args.name}' not found")
        print_frame_info(ldf.frame(args.name))

def handle_signal_subcommand(args, ldf: LDF):
    if args.list:
        for signal in ldf.signals:
            print(signal.name)
    else:
        if not ldf.signal(args.name):
            exit_with_error(1, f"Signal with name '{args.name}' not found")
        print_signal_info(ldf.signal(args.name))

def export_ldf(ldf: LDF, output: str = None):
    if output is None:
        json.dump(ldf._source, sys.stdout, indent=4)
    else:
        os.makedirs(os.path.dirname(output), exist_ok=True)
        with open(output, 'w+') as file:
            json.dump(ldf._source, file, indent=4)

def print_ldf_info(ldf: LDF, extended: bool = False):
    print(f"Protocol Version: {ldf.protocol_version:.01f}")
    print(f"Language Version: {ldf.language_version:.01f}")
    print(f"Speed: {ldf.baudrate}")
    print(f"Channel: {ldf.channel if ldf.channel else '-'}")

    if extended:
        print("Nodes:")
        print(f"\t{ldf.master.name} (master)")
        for slave in ldf.slaves:
            print(f"\t{slave.name}")
    else:
        print(f"Node count: {len(ldf.slaves) + 1}")

    if extended:
        print("Frames (id, length, name):")
        for frame in ldf.frames:
            print(f"\t{frame.frame_id},{frame.length},{frame.name}")
    else:
        print(f"Frame count: {len(ldf.frames)}")

    if extended:
        print("Signals (width, name):")
        for signal in ldf.signals:
            print(f"\t{signal.width},{signal.name}")
    else:
        print(f"Signal count: {len(ldf.signals)}")

def print_slave_info(slave: LinSlave):
    print(f"Name: {slave.name}")
    print(f"Protocol: {slave.lin_protocol:.01f}")
    print(f"Configured NAD: 0x{slave.configured_nad:02x}")
    print(f"Initial NAD: 0x{slave.initial_nad:02x}")
    print("Product Id:")
    print(f"\tSupplier Id: 0x{slave.product_id.supplier_id:04x}")
    print(f"\tFunction Id: 0x{slave.product_id.function_id:04x}")
    print(f"\tVariant: {slave.product_id.variant}")

def print_master_info(master: LinMaster):
    print(f"Name: {master.name}")
    print(f"Timebase: {master.timebase * 1000:.02f} ms")
    print(f"Jitter: {master.jitter * 1000:.02f} ms")

def print_frame_info(frame: LinFrame):
    print(f"Id: {frame.frame_id}")
    print(f"Name: {frame.name}")
    print(f"Length: {frame.length} byte(s)")
    print(f"Publisher: {frame.publisher.name}")
    print("Signals (offset, width, name):")
    for signal in frame.signal_map:
        print(f"\t{signal[0]},{signal[1].width},{signal[1].name}")

def print_signal_info(signal: LinSignal):
    print(f"Name: {signal.name}")
    print(f"Width: {signal.width} bit(s)")
    print(f"Initial value: {signal.init_value}")
    print(f"Publisher: {signal.publisher.name}")
    print("Subscribers:")
    for subscriber in signal.subscribers:
        print(f"\t{subscriber.name}")
