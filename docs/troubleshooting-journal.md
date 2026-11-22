# Troubleshooting Journal

*A practical record of the challenges, investigation and lessons learned while building a Cisco router monitoring and automation lab.*

## Why Document Troubleshooting?

Network engineering is not just about configuring devices when everything works. A significant part of the job involves identifying failures, investigating possible causes, testing solutions and validating the results.

This journal captures the challenges encountered while building the project, including the approaches that worked and the problems that still need attention.

---

## Challenge 01 — Lab Environment and File Persistence

### The problem

During earlier lab sessions, files created inside the virtual Linux environment were at risk of being lost when the lab restarted.

This created a practical concern: keeping the only copy of a Python script inside a temporary lab environment was not a reliable approach.

### Investigation and approach

We decided to maintain a separate project folder on the local Mac and use the virtual Linux environment for execution and testing.

However, transferring files directly from the Mac to the Linux node through SCP was unsuccessful because the virtual lab's internal network was not directly accessible from the host machine.

We eventually created the working Python script directly inside the Linux environment.

### What I learned

A working automation script is only one part of a project. Source-code backups, file persistence and report retrieval also need to be considered.

**Status:** Working script created and executed inside Linux. Direct file transfer and report retrieval remain unresolved.

---

## Challenge 02 — SSH Connection Refused

### The problem

The Linux node could reach the router, but the initial SSH connection attempt was refused.

This was an important distinction: successful IP connectivity did not automatically mean remote management was available.

### Investigation

We checked the router's SSH configuration and identified that SSH access needed to be enabled.

### Solution

The router was configured with:

- A hostname and domain name.
- A local administrative user.
- RSA keys.
- SSH version 2.
- Local authentication on the VTY lines.
- SSH as the permitted remote access protocol.

### Validation

SSH access from Linux to R1 was subsequently established successfully.

We also executed a remote Cisco IOS command from the Linux terminal.

**Status:** Resolved and verified.

---

## Challenge 03 — SSH Algorithm Compatibility

### The problem

The Linux SSH client and Cisco IOSv router did not initially negotiate a compatible connection using the default settings.

### Investigation

We examined the SSH key-exchange compatibility between the two systems.

### Solution

An additional SSH client option was used to permit the legacy Diffie-Hellman group14 SHA-1 key-exchange algorithm supported by the router.

The successful command used:

`-oKexAlgorithms=+diffie-hellman-group14-sha1`

### Validation

The Linux node successfully connected to R1 and executed remote monitoring commands.

### What I learned

SSH problems are not always caused by incorrect IP addresses, usernames or passwords. Differences in supported cryptographic algorithms can also prevent a connection.

**Status:** Resolved and verified in the lab.

---

## Challenge 04 — Python Environment Limitations

### The problem

The Linux environment did not provide the third-party Paramiko library, and installing additional packages was not a practical option in the available environment.

### Investigation

Instead of introducing an external dependency, we considered the tools already available in Linux.

### Solution

We used Python's standard library, particularly the `subprocess` module, to call the system SSH client.

This allowed Python to execute Cisco IOS commands remotely without requiring Paramiko.

### What I learned

Automation does not always require additional libraries. Understanding the tools already available in an environment can lead to simpler and more practical solutions.

**Status:** Implemented and verified.

---

## Challenge 05 — Python Script Creation and Execution

### The problem

An earlier script attempt encountered indentation and execution errors. Transferring the prepared script from the Mac also proved difficult.

### Investigation

We decided to create the working script directly inside the Linux environment using the Nano text editor.

The implementation was organised around a simple workflow:

1. Define router connection details.
2. Create report and log directories.
3. Check router reachability.
4. Execute the selected Cisco IOS commands over SSH.
5. Record execution results.
6. Generate a timestamped report.

### Validation

The script executed successfully in the Linux environment.

The terminal reported:

- Ping successful.
- `show version` successful.
- `show ip interface brief` successful.
- `show ip route` successful.
- `show clock` successful.
- Monitoring completed.

### What I learned

Building and testing automation in a restricted environment requires patience, careful command execution and a clear understanding of the dependencies involved.

**Status:** Core execution verified. The Mac-side script still needs to be aligned with the tested Linux version.

---

## Challenge 06 — Retrieving the Generated Monitoring Report

### The problem

The Python script completed its monitoring session and displayed the generated report filename.

However, the report was stored inside the virtual Linux environment, and retrieving it onto the Mac was unsuccessful.

### Investigation

We attempted to access the Linux node's report directory through a temporary HTTP server and also tried locating the generated file through terminal commands.

These attempts did not provide a reliable way to retrieve the report.

### What we learned

Generating a report successfully and making it accessible outside the execution environment are separate operational requirements.

Future improvements should include a reliable report export or file-transfer method.

**Status:** Report generation observed; retrieval onto the Mac remains pending.

---

## Final Lessons from the Lab

This project provided practical experience beyond basic router configuration.

Some of the most important lessons were:

- IP connectivity and SSH availability are separate things.
- SSH compatibility must be considered between different systems.
- Python can automate network tasks using existing Linux utilities.
- Troubleshooting should be performed one layer at a time.
- Temporary lab environments require careful file management.
- Automation results need to be preserved and documented, not just displayed in a terminal.

The most valuable part of this exercise was seeing how networking fundamentals, Linux and Python work together in a real virtual lab environment.

---

*This journal records actual observations and verified test outcomes. Unresolved issues are intentionally retained rather than presented as completed work.*