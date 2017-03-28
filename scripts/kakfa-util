#!/usr/bin/env python

import sys
import json
import argparse
from kafka import KafkaConsumer, KafkaProducer


def action_dump(args):
    consumer = KafkaConsumer(args.channel,
        auto_offset_reset='earliest',
        bootstrap_servers=args.server,
        consumer_timeout_ms=3000,
        group_id=args.group)

    for msg in consumer:
        print msg.value

def action_load(args):
    consumer = KafkaConsumer(args.channel, 
        auto_offset_reset='earliest',
        bootstrap_servers=args.server,
        consumer_timeout_ms=3000,
        group_id=args.group)
        
    for msg in consumer:
        print msg.value
        

def action_list(args):
    consumer = KafkaConsumer(bootstrap_servers=args.server)

    for msg in consumer.topics():
        print msg

def action_load(args):
    producer = KafkaProducer(bootstrap_servers=args.server)

    with open(args.file) as handle:
        for line in handle:
            data = json.loads(line)
            producer.send(args.channel, json.dumps(data))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    subparsers = parser.add_subparsers(title="subcommand")

    parser_dump = subparsers.add_parser('dump')
    parser_dump.add_argument("server")
    parser_dump.add_argument("channel")
    parser_dump.add_argument("--group", default=None)
    parser_dump.set_defaults(func=action_dump)

    parser_load = subparsers.add_parser('load')
    parser_load.add_argument("server")
    parser_load.add_argument("channel")
    parser_load.add_argument("file")
    parser_load.set_defaults(func=action_load)

    parser_list = subparsers.add_parser('list')
    parser_list.add_argument("server")
    parser_list.set_defaults(func=action_list)

    args = parser.parse_args()
    func = args.func

    e = func(args)
    sys.exit(e)
