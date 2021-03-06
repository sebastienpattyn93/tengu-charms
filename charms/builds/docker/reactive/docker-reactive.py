#!/usr/bin/env python3
# pylint:disable=c0111,c0103
from time import sleep
from subprocess import check_call, CalledProcessError

import docker
from charmhelpers.core import host
from charmhelpers.core.hookenv import (
    status_set,
    open_port,
    log,
    unit_private_ip,
)

from charms.reactive import remove_state, set_state, when, when_not


@when('apt.installed.docker.io')
@when_not('docker.ready')
def configure_docker():
    reload_system_daemons()
    check_call(['usermod', '-aG', 'docker', 'ubuntu'])
    set_state('docker.ready')
    # Make sure probe is installed
    if not _probe_runtime_availability():
        log("Error! Docker isn't available! This shouldn't happen!")
        exit(1)
    status_set('active', 'Ready')
    set_state('docker.available')


@when('dockerhost.available')
def run_images(relation):
    container_requests = relation.container_requests
    running_containers = {}
    log(container_requests)
    for (uuid, container_request) in container_requests.items():
        running_containers[uuid] = ensure_running(uuid, container_request)
    relation.send_running_containers(running_containers)


def _probe_runtime_availability():
    ''' Determine if the workload daemon is active and responding '''
    try:
        cmd = ['docker', 'info']
        check_call(cmd)
        return True
    except CalledProcessError:
        # Remove the availability state if we fail reachability
        remove_state('docker.available')
        return False


def ensure_running(uuid, container_request):
    '''When the provided image is not running, set it up and run it. '''
    client = docker.from_env()
    image = container_request['image']
    kwargs = {
        'name': uuid,
        'detach': True,
        'publish_all_ports': True,
    }
    # Only start container when it is not already running
    try:
        container = client.containers.get(uuid)
    except docker.errors.NotFound:
        print("Starting docker container. This might take a while.\n"
              "Image: {}\nkwargs: {}".format(image, kwargs))
        check_call([
            'docker', 'run',
            '--name', kwargs['name'],
            '-d',
            '-P',
            image])
        # Following code doesn't seem to work. no idea why..
        # container = client.containers.run(image, **kwargs)
        while True:
            # Refresh the python object to show the latest info
            container = client.containers.get(uuid)
            if container.status == "running":
                break
            sleep(1)
    # Expose ports
    ports = container.attrs['NetworkSettings']['Ports'] or {}
    open_ports = {}
    for exposed_port in ports.keys():
        print("exp_port: " + exposed_port)
        proto = exposed_port.split('/')[1]
        for host_portip in ports[exposed_port]:
            print("host_portip " + str(host_portip))
            open_port(host_portip['HostPort'], protocol=proto)
            open_ports[exposed_port.split('/')[0]] = host_portip['HostPort']
    return {
        'host': unit_private_ip(),
        'ports': open_ports,
    }


#
#     HELPER FUNCTIONS
#
def reload_system_daemons():
    ''' Reload the system daemons from on-disk configuration changes '''
    log('Reloading system daemons.')
    lsb = host.lsb_release()
    code = lsb['DISTRIB_CODENAME']
    if code != 'trusty':
        command = ['systemctl', 'daemon-reload']
        check_call(command)
    else:
        host.service_reload('docker')
