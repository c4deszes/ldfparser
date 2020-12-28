from ldfparser.node import LinMaster, LinSlave
import sys
import argparse
import json

from .parser import parseLDF, LDF


def parse_args(args):
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--ldf', required=True)
	parser.add_argument('-e', '--encoding', required=False, default='utf-8')
	subparser = parser.add_subparsers(dest="subparser_name")

	infoparser = subparser.add_parser('info')
	infoparser.add_argument('--details', action='store_true')

	exportparser = subparser.add_parser('export')
	exportparser.add_argument('--output', required=False, type=str, default=None)

	nodeparser = subparser.add_parser('node')
	nodearggroup = nodeparser.add_mutually_exclusive_group()
	nodearggroup.add_argument('--list', action="store_true")
	nodearggroup.add_argument('--master', action="store_true")
	nodearggroup.add_argument('--slave', type=str)

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
		if args.list:
			# TODO: print list
			print("Printing node list..")
		elif args.master:
			print_master_info(ldf.master)
		else:
			if not ldf.slave(args.slave):
				print(f"Slave '{args.slave}' not found.")
				exit(1)
			print_slave_info(ldf.slave(args.slave))


def export_ldf(ldf: LDF, output: str = None):
	if output is None:
		json.dump(ldf._source, sys.stdout, indent=4)
	else:
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
		print("Frames:")
		for frame in ldf.frames:
			print(f"\tid={frame.frame_id},name={frame.name},length={frame.length}\t")
	else:
		print(f"Frame count: {len(ldf.frames)}")

	if extended:
		print("Signals:")
		for signal in ldf.signals:
			print(f"\tname={signal.name},width={signal.width}")
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
	print(f"\tVariant: {slave.product_id.variant if slave.product_id.variant else '-'}")


def print_master_info(master: LinMaster):
	print(f"Name: {master.name}")
	print(f"Timebase: {master.timebase * 1000:.02f} ms")
	print(f"Jitter: {master.jitter * 1000:.02f} ms")
