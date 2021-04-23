# Google Cloud Vision over µD3TN

## Introduction
In this project Spatiam Coporation builds from the basic python programs in [µD3TN](https://gitlab.com/d3tn/ud3tn), to bring access to Google's Cloud Vision API as a DTN (Delay and Disruption Tolerant Network) application. The project is also based from Dr. Lara Suzuki's project, [Using Google Cloud Vision API over DTN](https://github.com/lasuzuki/dtn-gcp-vision-ai).

## Live Demo
See a live demo [here](https://youtu.be/BnHjMeGiE7Y).

## Prerequisites
This repo assumes that you have a running µD3TN environment in a POSIX-compliant OS, and are familiar with the basic set up of µD3TN nodes. This information can be found in the [µD3TN repo](https://gitlab.com/d3tn/ud3tn).
Additionally, µD3TN's `python-uD3TN-utils` must be installed in your environment. Follow [these instructions](https://gitlab.com/d3tn/ud3tn/-/tree/master/python-ud3tn-utils) for the installation steps.

## Project Set up
You may place `aap_receive_cv.py` and `aap_send_cv.py` in the `tools/aap/` directory (inside the µD3TN code base).

Install grpcio and google-cloud-vision

````
$ pip3 install grpcio google-cloud-vision
````

## Setting up our Google Cloud Project
In order to access Google's Cloud Vision API, you will need to create a Google Cloud Platform account from the [Google Cloud Console](https://console.cloud.google.com/).

Once this is done, go to the Google Cloud Console and select or create a project (option in top left corner).

We now need a way to authenticate to this project for our programs to access the Cloud Vision API. For this, follow Google's easy [authentication guide](https://cloud.google.com/docs/authentication/getting-started). 

At the end of this guide, you will have generated a JSON authentication key, copy this key into your µD3TN project, record its absolute path, and replace `<google_authentication_key_path>` in 'aap_receive_cv.py' with it.

Lastly, we will need to give our project permissions to the Cloud Vision API, so once again go to the Google Cloud Console and enter 'Cloud Vision API' into the search bar, then click on the first result and select 'ENABLE'.

## Using the programs
Once you have a set of nodes connected with each other, you may use the following commands to send and receive images and image labels from Google's Cloud Vision API.

### Receiving images and labels
`aap_receive_cv.py` sets up the receiver at the `/sink_cv` endpoint.

The `--send-reply` flag is optional if you wish for labels to be sent back to the /sink_cv endpoint of the original image sender.

````
$ python3 aap_receive_cv.py --socket <path_to_socket_file> --agentid sink_cv --send-reply
````

### Sending an image
`aap_send_cv.py` sends an image at the specified file path to a given endpoint.

````
$ python3 aap_send_cv.py --socket <path_to_socket_file> --agentid source_cv "dtn://<eid_to_send_to>/sink_cv" "<path_to_image>"
````
