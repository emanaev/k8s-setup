#!/usr/bin/env python

from hetznercloud import *
import os, time, sys, json

client = HetznerCloudClient( HetznerCloudClientConfiguration().with_api_key(os.environ["HCLOUD_TOKEN"]).with_api_version(1) )

TYPE=SERVER_TYPE_2CPU_8GB
LOC='nbg1'

def delete_all():
  for server in client.servers().get_all():
    action = server.delete()
    client.actions().wait_until_empty()
#    action.wait_until_status_is(ACTION_STATUS_SUCCESS)
    print("Removed old server %s" % server.name)
  for volume in client.volumes().get_all():
    action = volume.delete()
    client.actions().wait_until_empty()
#    action.wait_until_status_is(ACTION_STATUS_SUCCESS)
    print("Removed old volume %s" % volume.name)

def create_server(name, type, volume_sizes):
  server, action = client.servers().create(name=name,
    server_type=type,
    image=IMAGE_UBUNTU_1604, # REQUIRED
#    datacenter=DATACENTER_NUREMBERG_1,
    location=LOC,
    start_after_create=True,
    ssh_keys=["emanaev@host"])
  server.wait_until_status_is(SERVER_STATUS_RUNNING)
  client.actions().wait_until_empty()
  print("Server %s created" % server.name)

  for i in range(len(volume_sizes)):
    volume, action = client.volumes().create(
        name="vol_%s_%d"%(name,i+1),
        size=volume_sizes[i],
        server=server.id,
        format='ext4',
        automount=True)
    volume.wait_until_status_is(VOLUME_STATUS_AVAILABLE)
    client.actions().wait_until_empty()
    print("Volume %s created" % volume.name)
#    action = volume.attach_to_server(server.id, True)
#    action.wait_until_status_is(ACTION_STATUS_SUCCESS)
#    print("Volume %s attached" % volume.name)

#  server.power_on()
#  server.wait_until_status_is(SERVER_STATUS_RUNNING)
#  print("Server %s started" % server.name)

#for dc in client.datacenters().get_all():
#  print(dc.name)

if len(sys.argv)>1:
    if sys.argv[1]=='create':
        for i in range(3):
            create_server('node'+str(i+1), TYPE, [50,10])
    elif sys.argv[1] in ['delete','remove']:
        delete_all()
    elif sys.argv[1]=='servers':
        for s in client.servers().get_all():
            print("%s %s" %(s.public_net_ipv4, s.name))
    elif sys.argv[1]=='--list':
        servers = list(client.servers().get_all())
        names = [s.name for s in servers]
        all = dict([(s.name, {'ansible_host': s.public_net_ipv4, 'ip': s.public_net_ipv4}) for s in servers])
        res = {
            "_meta": {"hostvars": all},
            "all": { "children": ["etcd","kubespray","ungrouped"] },
            "etcd": { "hosts": names[0:3] },
            "k8s-cluster": { "children": ["kube-master", "kube-node"] },
            "kube-master": { "hosts": names[0:2] },
            "kube-node": { "hosts": names },
            "kubespray": { "children": ["k8s-cluster"] },
            "ungrouped": {}
        }
        print(json.dumps(res))
