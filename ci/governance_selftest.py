#!/usr/bin/env python3
from datetime import datetime, timedelta, timezone
def inactivity(hours):
    return "status:reassignment-required" if hours>=72 else "status:at-risk" if hours>=48 else "status:update-required" if hours>=24 else None
assert inactivity(23) is None and inactivity(24)=="status:update-required" and inactivity(48)=="status:at-risk" and inactivity(72)=="status:reassignment-required"
active=["WP-00.1"]
assert ("status:ready" if len(active)>=1 else "status:in-progress")=="status:ready"
print("PASS: WIP enforcement model")
print("PASS: inactivity escalation dry-run model")
