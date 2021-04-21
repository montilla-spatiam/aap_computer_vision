# Google Cloud Vision over µD3TN

## Introduction
In this project Spatiam Coporation builds from the basic python programs in [µD3TN](https://gitlab.com/d3tn/ud3tn), to bring access to Google's Cloud Vision API as a DTN (Delay and Disruption Tolerant) application.

## Prerequisites
This repo assumes that you have a running µD3TN environment in a POSIX-compliant OS, and are familiar with the basic set up of µD3TN nodes. This information can be found in the [µD3TN repo](https://gitlab.com/d3tn/ud3tn).
Additionally, python-uD3TN-utils must be installed in your environment. Follow [these instructions](https://gitlab.com/d3tn/ud3tn/-/tree/master/python-ud3tn-utils) for the installation steps.

## Project Set up
You may place aap_receive_cv.py and aap_send_cv.py in tools/aap/ (directories inside the µD3TN code base).

Install grpcio and google-cloud-vision

`
pip3 install grpcio google-cloud-vision
`

## Setting up our Google Cloud Project
In order to access Google's Cloud Vision API, you will need to create a Google Cloud Platform account from the [Google Cloud Console](https://console.cloud.google.com/).

Once this is done, go to the Google Cloud Console and select or create a project (option in top left corner).

We now need a way to authenticate to this project, for our programs to access the Cloud Vision API through it. For this, follow Google's easy [authentication guide](https://cloud.google.com/docs/authentication/getting-started). 

At the end of this guide, you will have generated a JSON authentication key, copy this key into your µD3TN project, record its absolute path, and replace <google_authentication_key_path> in 'aap_receive_cv.py' with it.

Lastly, we will need to give our project permissions to the Cloud Vision API, so once again go to the Google Cloud Console and enter 'Cloud Vision API' into the search bar, then click on the first result and click 'ENABLE'.

Everything is now set up to start using the programs.
