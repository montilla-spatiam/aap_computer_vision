#!/usr/bin/env python3
# encoding: utf-8

import argparse
import logging

import os
import base64

from ud3tn_utils.aap import AAPUnixClient, AAPTCPClient
from helpers import add_common_parser_arguments, logging_level

if __name__ == "__main__":
    import sys

    parser = argparse.ArgumentParser(
        description="send a bundle via uD3TN's AAP interface",
    )
    add_common_parser_arguments(parser)
    parser.add_argument(
        "dest_eid",
        help="the destination EID of the created bundle",
    )
    parser.add_argument(
        "image_path",
        nargs="?",
        default=None,
        help="the path to the image to be labeled, (default: read from STDIN)",
    )

    args = parser.parse_args()

    if not args.image_path:
        with sys.stdin as f:
            args.image_path = f.read()
    else:
        args.image_path = args.image_path

    if args.verbosity:
        logging.basicConfig(level=logging_level(args.verbosity))

    if args.tcp:
        addr = (args.tcp[0], int(args.tcp[1]))

        if os.path.exists(args.image_path):
            with open(args.image_path, 'rb') as file:
                raw_image = file.read()

            with AAPTCPClient(address=addr) as aap_client:
                aap_client.register(args.agentid)
                aap_client.send_str(args.dest_eid, raw_image)

        else:
            print("ERROR: Provided path '{}' does not exist".format(args.image_path))

    else:
        if os.path.exists(args.image_path):
            with open(args.image_path, 'rb') as file:

                filename = args.image_path.split('/')[-1]

                raw_image = file.read()
                encoded_img = base64.b64encode(raw_image)
                img_str = filename + '#image\n' + encoded_img.decode('utf-8')

            with AAPUnixClient(address=args.socket) as aap_client:
                aap_client.register(args.agentid)
                aap_client.send_str(args.dest_eid, img_str)

        else:
            print("ERROR: Provided path '{}' does not exist".format(args.image_path))
