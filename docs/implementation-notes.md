# Implementation Notes

*Technical record of the configuration, implementation and validation of the Cisco Router Monitoring and Automation project.*

## 1. Lab Architecture

The project uses a simple management environment consisting of:

- One Linux monitoring node.
- One Cisco vIOS router (R1).
- One management network connecting the two devices.
- PNETLab as the virtual lab environment.

The Linux node acts as the monitoring system. It uses Python and the Linux SSH client to communicate with the Cisco router.

## 2. IP Addressing Plan

The following addressing was configured and verified during the lab session.

| Device | Interface | IP Address |
|---|---|---|
| Linux | eth0 | 192.168.10.2/24 |
| Cisco R1 | GigabitEthernet0/0 | 192.168.10.1/24 |

The router's management interface was verified as operational (`up/up`).

The Linux node was assigned its IPv4 address manually during the lab session.

## 3. Router Configuration

Cisco vIOS router R1 was configured to support remote SSH monitoring.

The configuration included:

- Hostname: R1
- Domain name: lab.local
- Management IP: 192.168.10.1/24
- Local administrative user authentication
- RSA key generation
- SSH version 2
- Local authentication on VTY lines
- SSH permitted for remote access

The router configuration was verified using:

```cisco
show ip interface brief
show ip ssh
show running-config
show logging
```

Sensitive configuration details, including password hashes and key material, are intentionally excluded from this document.

## 4. Linux Configuration

The Linux node was used to establish connectivity and execute the monitoring program.

The following commands were used during verification:

```bash
ip -br addr
ip route
ping -c 4 192.168.10.1
```

The Linux node was configured with `192.168.10.2/24` on `eth0`.

### Connectivity result

The ping test to R1 completed successfully:

- Packets transmitted: 4
- Packets received: 4
- Packet loss: 0%

This confirmed IP connectivity between the monitoring node and the router during the lab session.

## 5. SSH Configuration and Verification

The initial SSH connection attempt was refused because remote SSH access had not yet been configured on the router.

After configuring SSH on R1, the connection was established successfully.

The following command was used to execute a remote router command:

```bash
ssh -oKexAlgorithms=+diffie-hellman-group14-sha1 admin@192.168.10.1 "show ip interface brief"
```

The additional key-exchange option was required for compatibility with the virtual router's supported SSH algorithms.

SSH version 2 was verified on the router.

## 6. Python Monitoring Implementation

The monitoring program was created inside the Linux environment using Python 3.8.2.

It uses Python's standard-library `subprocess` module to execute Linux commands and connect to the router through the system SSH client.

No third-party Python SSH library was required.

### Monitoring operations

The script performs the following tasks:

1. Creates report and log directories.
2. Generates a timestamp for the monitoring report.
3. Checks router reachability using ping.
4. Connects to R1 through SSH.
5. Executes selected Cisco IOS commands.
6. Records execution results in the monitoring log.
7. Writes collected output into a timestamped report.

### Commands collected

| Cisco IOS command | Purpose |
|---|---|
| `show version` | Collect device and IOS information |
| `show ip interface brief` | Check interface addresses and status |
| `show ip route` | Collect routing information |
| `show clock` | Record router date and time |

## 7. Python Execution and Test Results

The monitoring script was executed successfully inside the Linux node.

The terminal reported:

| Test | Observed result |
|---|---|
| Router ping | Successful |
| `show version` | Successful |
| `show ip interface brief` | Successful |
| `show ip route` | Successful |
| `show clock` | Successful |
| Monitoring process | Completed |

The script displayed the generated report filename after execution.

**Important:** Report generation was observed, but the report and log files have not yet been retrieved to the local Mac and independently inspected.

## 8. Expected Project Output Structure

The intended local project structure is:

```text
Cisco-Router-Monitoring-Automation/
│
├── README.md
│
├── docs/
│   ├── implementation-notes.md
│   ├── troubleshooting-journal.md
│   └── router-command-outputs.txt
│
├── scripts/
│   └── router_monitor.py
│
├── reports/
│
├── logs/
│
└── screenshots/
```

The report and log directories are part of the intended output structure. The generated files from the Linux lab have not yet been archived in the local project.

## 9. Validation Summary

The following parts of the core workflow were successfully exercised:

1. Linux management IP configuration.
2. Router management interface configuration.
3. Linux-to-router IP connectivity.
4. SSH configuration and remote access.
5. Remote execution of four Cisco IOS commands.
6. Python monitoring script execution.
7. Timestamped report generation.

Report retrieval, inspection and preservation remain pending.

## 10. Implementation Considerations

A few practical considerations emerged during the lab:

- The Linux management IP was assigned manually and may need to be configured again if the lab environment resets.
- The SSH compatibility option should only be used when required by the router.
- The monitoring script depends on the Linux SSH client being available.
- Report and log files should be backed up outside the temporary lab environment.
- The local Mac copy of the Python script still needs to be aligned with the version successfully executed in Linux.

---

*These notes distinguish between verified lab results and remaining work. They will be updated as the project moves towards final documentation and publication.*