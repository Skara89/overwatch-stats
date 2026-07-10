# Overwatch Tier List

**Live:** https://skara89.github.io/overwatch-stats/

Personal tool for browsing Overwatch hero win/pick rates, pulled live from the [OverFast API](https://overfast-api.tekrop.fr). Auto-deploys via GitHub Pages on every push to `master`.

## Trend filter

The `Trend` dropdown (1/7/30/90 days) compares current stats to a daily snapshot, collected automatically by `.github/workflows/snapshot.yml` into `snapshots/`. Only available with no rank/role/map filter, since that's the only scope we snapshot. It shows the *change* since a past snapshot, not an exact "last N days" win rate — Blizzard only exposes cumulative-since-patch numbers, so a true rolling window isn't derivable.
