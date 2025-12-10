#!/bin/bash
set -e

source /opt/ros/jazzy/setup.bash
if [ -f "/root/openvins_ws/install/setup.bash" ]; then
    source "/root/openvins_ws/install/setup.bash"
fi

exec "$@"
