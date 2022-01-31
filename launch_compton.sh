#!/bin/bash

# Terminate all running instances of compton
killall -q compton

# Launch compton
compton -b
