from __future__ import annotations

import time

from .incidents import STATE

# IT Helpdesk knowledge base
CORPUS = {
    "password": [
        "To reset your password: go to https://sso.internal/reset, enter your employee email, and follow the link sent to your registered email. Passwords must be at least 12 characters with uppercase, number, and symbol.",
    ],
    "vpn": [
        "Install the VPN client from https://it.internal/vpn. Use your SSO credentials to connect. If connection fails, check that your device certificate is up to date. Contact helpdesk if the issue persists.",
    ],
    "laptop": [
        "For hardware issues (screen, keyboard, battery), submit a ticket at https://helpdesk.internal. Bring your laptop to IT room 3B for same-day diagnosis. Loaner devices are available for critical cases.",
    ],
    "email": [
        "Email is hosted on Microsoft 365. If you cannot access Outlook, try https://outlook.office.com. For quota issues, archive old emails or request a quota increase via the helpdesk portal.",
    ],
    "incident": [
        "To report a system incident: call the on-call hotline at ext. 9999 or page via PagerDuty. Severity P1 (full outage) requires immediate escalation to the on-call engineer. Include affected service, symptoms, and start time.",
    ],
    "access": [
        "Access requests must be approved by your manager and submitted via https://access.internal. Standard provisioning takes 1 business day. Emergency access for production systems requires CISO approval.",
    ],
    "server": [
        "Server health dashboards are at https://grafana.internal. For unresponsive servers, check the runbook at docs/runbooks/server-down.md. Do not reboot production servers without change management approval.",
    ],
    "network": [
        "For network issues (slow connection, no internet), first restart your network adapter. If the issue persists, check the status page at https://status.internal. Report outages to netops@internal.",
    ],
    "software": [
        "Software installation requests must go through the IT portal at https://it.internal/software. Approved software list is available there. Unlicensed software installation is a policy violation.",
    ],
    "backup": [
        "All workstations are backed up nightly via the backup agent. To restore a file, right-click and select 'Restore previous versions'. For full system restores, contact helpdesk with your device serial number.",
    ],
}


def retrieve(message: str) -> list[str]:
    if STATE["tool_fail"]:
        raise RuntimeError("Helpdesk knowledge base timeout")
    if STATE["rag_slow"]:
        time.sleep(2.5)
    lowered = message.lower()
    for key, docs in CORPUS.items():
        if key in lowered:
            return docs
    return ["No matching IT helpdesk article found. Please contact helpdesk at ext. 9999 or helpdesk@internal."]
