#!/usr/bin/env python3
# encoding: utf-8

import argparse
import logging
import sys

import base64
import os

from google.cloud import vision
from ud3tn_utils.aap import AAPUnixClient, AAPTCPClient
from helpers import add_common_parser_arguments, logging_level


def run_aap_recv(aap_client, max_count=None):

    print("Waiting for bundles...")

    # Set up client for Google Cloud Vision API
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '<google_authentication_key_path>'
    client = vision.ImageAnnotatorClient()

    counter = 0
    while True:
        msg = aap_client.receive()
        if not msg:
            return

        msg_payload = msg.payload.decode('utf-8')

        
        # Message payload has one of two formats
        #   1) <img_filename>#image\n<base64_encoded_image>
        #   2) <img_filename>#labels\n<image_labels>
        
        img_filename = msg_payload.split('\n', 1)[0]
        msg_content = msg_payload.split('\n', 1)[1]
    
        img_bytes = base64.b64decode(msg_content)

        print("\nReceived '{}' from '{}'".format(
            img_filename, msg.eid,
        ))

        # Load and send image to Google Cloud Vision API to get labels back
        image = vision.Image(content=img_bytes)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        x = len(labels)

        label_descriptions = []
        for label in labels:
            label_descriptions.append(str(label.description))

        label_desc_str = ', '.join(label_descriptions,)
        print("Identified '{}' Labels in the image: {}".format(x, label_desc_str))

        print("Forwarding labels to '{}', see logs for more details".format(msg.eid))

        aap_client.send_str(msg.eid, label_desc_str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="register an agent with uD3TN and wait for bundles",
    )

    add_common_parser_arguments(parser)

    parser.add_argument(
        "-c", "--count",
        type=int,
        default=None,
        help="amount of bundles to be received before terminating",
    )

    args = parser.parse_args()

    if args.verbosity:
        logging.basicConfig(level=logging_level(args.verbosity))

    if args.tcp:
        addr = (args.tcp[0], int(args.tcp[1]))
        with AAPTCPClient(address=addr) as aap_client:
            aap_client.register(args.agentid)
            run_aap_recv(aap_client, args.count)
    else:
        with AAPUnixClient(address=args.socket) as aap_client:
            aap_client.register(args.agentid)
            run_aap_recv(aap_client, args.count)
