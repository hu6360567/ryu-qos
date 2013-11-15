#!/usr/bin/python

"""
Script created by VND - Visual Network Description

Modified by LvLng@Future Network Lab of BUPT
"""
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
import os


def topology(remoteip, ofversion):
    "Create a network."
    net = Mininet(controller=RemoteController, link=TCLink, switch=OVSKernelSwitch)

    print "*** Creating nodes"
    client1 = net.addHost('client1', mac='00:00:00:00:00:01', ip='172.17.0.1/16')
    client2 = net.addHost('client2', mac='00:00:00:00:00:02', ip='172.17.0.2/16')
    server = net.addHost('server', mac='00:00:00:00:00:ff', ip='172.17.0.255/16')
    switch1 = net.addSwitch('switch1', protocols=ofversion)
    switch2 = net.addSwitch('switch2', protocols=ofversion)
    switch3 = net.addSwitch('switch3', protocols=ofversion)
    ryu = net.addController('ryu controller', controller=RemoteController, ip='10.108.144.150', port=6633)
    vm = net.addHost('vm', mac='00:00:00:00:00:10', ip='172.17.0.10/16')

    print "*** Creating links"
    switchLinkOpts = dict(bw=10, delay='1ms')
    hostLinkOpts = dict(bw=100)
    net.addLink(client1, switch1, 0, 0, **hostLinkOpts)
    net.addLink(client2, switch2, 0, 0, **hostLinkOpts)
    net.addLink(server, switch3, 0, 0, **hostLinkOpts)
    net.addLink(switch1, switch3, 1, 1, **switchLinkOpts)
    net.addLink(switch2, switch3, 1, 2, **switchLinkOpts)
    net.addLink(vm, switch1, 0, 2, **hostLinkOpts)

    print "*** Removing former QoS & Queue"
    os.popen("ovs-vsctl --all destroy qos")
    os.popen("ovs-vsctl --all destroy queue")

    print "*** Starting network"
    net.build()
    switch1.start([ryu])
    switch2.start([ryu])
    switch3.start([ryu])
    ryu.start()

    print "\n*** Stage 1: VM connected to switch1"
    CLI(net)
    print "***Migrating VM"
    switch1.detach('switch1-eth2')
    switch2.attach('switch1-eth2')
    print "\n*** Stage 2: VM connected to switch2"
    CLI(net)

    print "*** Stopping network"
    net.stop()


if __name__ == '__main__':
    print 'Please input controller ip (default 10.108.144.150) and OpenFlow Protocol Version (default OpenFlow13)'
    controller_ip = raw_input('controller ip:')
    of_version = raw_input('OpenFlow Protocol Version(OpenFlow10,OpenFlow13):')
    if controller_ip == '':
        controller_ip = '10.108.144.150'
    if of_version == '':
        of_version = 'OpenFlow13'
    elif (of_version != 'OpenFlow10') and (of_version != 'OpenFlow13'):
        of_version = 'OpenFlow13'
        print 'wrong OpenFlow Protocol Version, set it to Openflow13'
    setLogLevel('info')
    topology(controller_ip,of_version)

