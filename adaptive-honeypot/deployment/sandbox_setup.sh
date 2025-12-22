#!/usr/bin/env bash
# Basic sandbox setup (placeholder). Run with caution in a lab environment.
set -e

echo "[*] Applying basic firewall rules to limit outbound traffic..."
# Example: block outbound except loopback (adjust for your environment)
iptables -P OUTPUT DROP
iptables -A OUTPUT -d 127.0.0.1 -j ACCEPT

echo "[*] Sandbox setup complete (demo placeholder)."
