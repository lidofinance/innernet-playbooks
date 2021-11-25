import pytest

testinfra_hosts = ['ansible://innernet_members?force_ansible=True']

@pytest.fixture()
def peers(host):
    ips = []
    inventory = host.backend.ansible_runner.inventory
    inventory_hostname = host.backend.get_hostname()
    other_hosts = set(inventory['innernet_members']['hosts']) - set([inventory_hostname])
    for other in other_hosts:
        ips.append(inventory['_meta']['hostvars'][other]['innernet_ip'])
    return ips
    

def test_ok(host, peers):
    for peer in peers:
        res = host.run(f'/usr/bin/ping -c 2 -w 2 -i 0.2 {peer}')
        if res.rc:
            pytest.fail(res.stdout)
