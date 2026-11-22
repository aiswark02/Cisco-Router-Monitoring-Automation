
#!/usr/bin/env python3

"""
Cisco Router Monitoring and Automation
Project: Cisco Router Monitoring Using Python and SSH
"""

import subprocess
import logging
from datetime import datetime
from pathlib import Path

# -------------------------------
# Configuration
# -------------------------------

ROUTER_IP = "192.168.10.1"
USERNAME = input("Enter router SSH username: ").strip()
SSH_TIMEOUT = 30

PROJECT_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_DIR / "reports"
LOG_DIR = PROJECT_DIR / "logs"

REPORT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

REPORT_FILE = REPORT_DIR / f"monitoring_report_{timestamp}.txt"
LOG_FILE = LOG_DIR / "monitoring.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------
# SSH Configuration
# -------------------------------

SSH_OPTIONS = [
    "-oKexAlgorithms=+diffie-hellman-group14-sha1",
    "-oConnectTimeout=10"
]

# -------------------------------
# Router Command Execution
# -------------------------------

def run_router_command(command, report):

    report.write(f"\n\n{'=' * 60}\n")
    report.write(f"COMMAND: {command}\n")
    report.write(f"{'=' * 60}\n")
    report.flush()

    ssh_command = [
        "ssh"
    ] + SSH_OPTIONS + [
        f"{USERNAME}@{ROUTER_IP}",
        command
    ]

    try:
        result = subprocess.run(
            ssh_command,
            stdout=report,
            stderr=subprocess.STDOUT,
            timeout=SSH_TIMEOUT
        )

        if result.returncode == 0:
            logging.info("Command successful: %s", command)
            print(f"[SUCCESS] {command}")
        else:
            logging.error(
                "Command failed: %s (exit code %s)",
                command,
                result.returncode
            )
            print(f"[FAILED] {command}")

    except subprocess.TimeoutExpired:
        logging.error("Command timed out: %s", command)
        report.write("\nERROR: Command timed out.\n")
        print(f"[TIMEOUT] {command}")

    except Exception as error:
        logging.exception("Unexpected error: %s", command)
        report.write(f"\nERROR: {error}\n")
        print(f"[ERROR] {command}: {error}")


# -------------------------------
# Connectivity Test
# -------------------------------

def check_connectivity(report):

    report.write("\n\nCONNECTIVITY TEST\n")
    report.write("=" * 60 + "\n")

    try:
        result = subprocess.run(
            ["ping", "-c", "4", ROUTER_IP],
            stdout=report,
            stderr=subprocess.STDOUT,
            timeout=15
        )

        if result.returncode == 0:
            logging.info("Router ping successful")
            print("[SUCCESS] Router is reachable")
        else:
            logging.warning("Router ping failed")
            print("[FAILED] Router is unreachable")

    except subprocess.TimeoutExpired:
        logging.error("Ping test timed out")
        report.write("ERROR: Ping test timed out.\n")
        print("[TIMEOUT] Ping test")


# -------------------------------
# Main Monitoring Process
# -------------------------------

def main():

    commands = [
        "show version",
        "show ip interface brief",
        "show ip route",
        "show clock"
    ]

    print("\nCisco Router Monitoring Started")
    print(f"Router: {ROUTER_IP}")
    print(f"Report: {REPORT_FILE}")

    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as report:

            report.write("CISCO ROUTER MONITORING REPORT\n")
            report.write("=" * 60 + "\n")
            report.write(f"Router IP: {ROUTER_IP}\n")
            report.write(
                f"Generated: {datetime.now().isoformat()}\n"
            )

            check_connectivity(report)

            for command in commands:
                run_router_command(command, report)

            report.write("\n\nMONITORING SESSION COMPLETED\n")

        logging.info("Monitoring session completed")
        print("\nMonitoring session completed.")
        print(f"Report saved: {REPORT_FILE}")

    except OSError as error:
        logging.exception("Could not create monitoring report")
        print(f"File error: {error}")


if __name__ == "__main__":
    if not USERNAME:
        print("SSH username cannot be empty.")
    else:
        main()