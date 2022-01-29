Innernet playbooks
==================
Innernet is a wireguard management software for creating private network system.

See https://github.com/tonarino/innernet

This repository contains playbooks to manage innernet with ansible.

## Security model.
In addition to own innernet security model, we introduce few more ideas:
### IPv6 only
To avoid messing with tiny pools of precious and non-unique private IPs
(192.168.0.0, 100.64.0.0, 172.16.0.0, 10.0.0.0, and ... well, that's all)
we have IPv6 as a single supported protocol of internals of innernet network.

Each innernet network recieve a proper Unique Local address (ULA) network
with prefix /48. Each use of playbook in each context (even between staging
and production) should have own network. There is a well-established procedure
for creating semi-unique networks, so chances of clash are very low.

###  User is cidr
Original innernet model included idea of 'peer' to represent user and/or
server. This is not enough, because user may have more than one device
(laptop, PC, may be a second laptop, etc).

To work with this we assign a whole /64 network to each user. Within
this cidr user may have 'machine to machine' connectivity (f.e. to
replicate data from working laptop to PC), and permissions are managed
on higher level cidr, which includes CIDRs for each user.

### Automated management of innernet-server
Outside of user management (see below) all other operations are
completely automated, inlcuding higher order cidr management,
servers invites and redeeming.

### Ansible is the source of truth
All CIDRs and associations are managed via ansible,
and Ansible variables (inventory, group vers, extra vars, etc) is
the single source of truth for them.

User peers are manually managed, server peers are managed by playbooks.

Address allocation is completely deterministic and done via ansible variables.

### No innernet administrator flags for anyone
All innernet administration is done via root access to innernet-auth
server (which run innernet-server application). Not a single user
or server has 'admin' flag set on. This helps to reduce administrative
scope and define permissions: if user can 'ssh/sudo' on innernet-auth,
it can manage users and association.

### Idempotence of playbooks
All playbooks are idempotent and should yield 0 changed if no
changes was done.

# Bugs
Said that, there are few issues in those implementations, mostly
coming from lack of some features of innernet-admin binary.

I hope they would be resolved soon.

# How to try

You need to run this from host with installed libvirt and qemu.
Whilst it's possible to run it on machine without hardware-accelerated
virtualization, it's going to be very slow (and it's required updating
VM templates), so, pratically, 'VT' is must.

VMs are created and destroyed by [Molecule](https://molecule.readthedocs.io/en/latest/).
Just run `molecule create` or `molecule converge`.

# How to use in production
You need to add groups `innernet-auth` and `innernet-servers` to
your inventory and provide with all required variables.

After configuring innernet, log in into innernet-auth server
(there should be only one innernet-auth server per network),
and issue oneself a new invite, and accept it for your own machine.

Assure you have access to all innernet-servers via innernet network.

Issue invites for your collegues.
