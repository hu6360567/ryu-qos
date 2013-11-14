ryu-qos
=======

*Provide simple switch with QoS by using ryu-controller in both openflow 1.0 and openflow 1.3*

###Requirements

This project is a very simple implementation by using OVS queue and Openflow protocols.

These codes are tesed by:

Ryu 3.3

Mininet 2.1.0 (should also work in 2.0.0, but `node.py` we offered is modified from 2.1.0)

OpenVSwitch 1.11.0 (any version >=1.10.0 which supports Openflow 1.3 protocol should work)

###Thanks

We use the same way that [floodlight-qos-betta](https://github.com/wallnerryan/floodlight-qos-beta)
implements in Floodlight.

