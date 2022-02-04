# Butter - SSH Client
Lightweight SSH-Client. Build to manage IoT devices (like Raspberry Pis) VMs, Systems. It is agentless and relies on SSH Infrastructure. Fully capable of remotely executing commands on inventories and fetching you the consolidated outputs.

## Table of Contents
- [Requirments](#requirments)
- [Secure Shell Setup](#secure-shell-setup)
- [Installation](#installation)
- [Walk Through](#walk-through)
- [License](#license)

## Requirments
- Works with Unix-based systems (Linux, macOS)
- Python 3.7 or higher
- SSH passwordless login

## Secure Shell Setup
### Generate SSH Key Pair
The system running `Butter` should be able to login into each device through SSH without a password. So, generate SSH key pair and copy the public key to all other devices.
```bash
ssh-keygen
```
### Copy the Public Key
```bash
ssh-copy-id pi@192.168.0.XXX
```

## Installation
1. Clone the `butter` repository
```bash
git clone https://github.com/cloud-and-smart-labs/butter.git
```

2. Change directory
```bash
cd butter
```
3. Install the package
```bash
pip install .
```

## Walk Through
Butter has two types of commands:
1. `i`nventory: Creates inventory that contains the SSH details of hosts
2. E`x`ecute: Executes the commands on inventories

```bash
butter --help
```

### Inventory
1. Create inventory `demo`
```bash
butter i create demo
```
2. Add hosts into the inventory `demo`
```bash
butter i add demo root@172.17.0.3 root@172.17.0.4
```
3. Get list of inventories
```bash
butter i ls
```
4. Get list of Hosts inside inventory
```bash
butter i ls demo
```

<p align="center">
    <img src="docs/ls.png" width="500">
</p>

5. Remove host from inventory
```bash
butter i rm demo 172.17.0.3
```
OR
```bash
butter i rm demo root@172.17.0.3
```
6. Remove inventory `demo`
```bash
butter i clear demo 
```

### Execute
Execute commands
```bash
butter x sh demo 'docker image ls'
```
OR user short <br>
`bx` : `b`utter e`x`ecute
```bash
bx demo 'docker image ls'
```
<p align="center">
    <img src="docs/cmd.png" width="500">
</p>


## License
This tool is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).