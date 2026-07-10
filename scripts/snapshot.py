#!/usr/bin/env python3
"""Fetch current hero stats for a fixed set of base filter combos and append
a dated snapshot to snapshots/, so the frontend can show trend deltas
(current value vs. N days ago). Run daily by .github/workflows/snapshot.yml.

Only unfiltered combos (no rank/role/map) are snapshotted, on purpose: the
combinatorial space with rank/role/map included is too large to fetch daily
without hammering the API, and OverFast only exposes cumulative-since-patch
aggregates anyway, so trend deltas are an approximation already -- keeping
the snapshot scope small keeps that approximation honest and cheap to run.
"""
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

API = "https://overfast-api.tekrop.fr/heroes/stats"
REGIONS = ["europe", "americas", "asia"]
PLATFORMS = ["pc", "console"]
GAMEMODES = ["competitive", "quickplay"]

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_DIR = ROOT / "snapshots"
INDEX_FILE = SNAPSHOT_DIR / "index.json"
MAX_HISTORY_DAYS = 120


def fetch_combo(region, platform, gamemode, attempt=0):
    url = f"{API}?platform={platform}&gamemode={gamemode}&region={region}"
    try:
        with urllib.request.urlopen(url, timeout=15) as res:
            return json.loads(res.read())
    except urllib.error.HTTPError as e:
        if e.code == 429 and attempt < 4:
            time.sleep(1.5 * (attempt + 1))
            return fetch_combo(region, platform, gamemode, attempt + 1)
        raise


def main():
    SNAPSHOT_DIR.mkdir(exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    combos = {}
    for region in REGIONS:
        for platform in PLATFORMS:
            for gamemode in GAMEMODES:
                key = f"{region}|{platform}|{gamemode}"
                combos[key] = fetch_combo(region, platform, gamemode)
                time.sleep(0.3)

    snapshot = {
        "date": today,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "combos": combos,
    }
    (SNAPSHOT_DIR / f"{today}.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )

    if INDEX_FILE.exists():
        index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    else:
        index = {"dates": []}
    if today not in index["dates"]:
        index["dates"].append(today)
    index["dates"] = sorted(index["dates"])[-MAX_HISTORY_DAYS:]
    INDEX_FILE.write_text(json.dumps(index, indent=0), encoding="utf-8")

    print(f"Snapshot for {today} written ({len(combos)} combos).")


if __name__ == "__main__":
    main()
