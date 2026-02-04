# Bitcoin Miner Mock

A simple, live-logging mock Bitcoin miner for demos, testing, and mockups.

## Quick Start

```bash
python "bitcoin miner.py"
```

The script will:
- Log mining activity to `miner.log` in real-time
- Print logs to the terminal
- Run until you press **Ctrl+C**

## Live Dashboard

Open `index.html` in a web browser to view a live dashboard of the mining logs. The dashboard updates every 500ms.

To serve locally:
```bash
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

## Files

- `bitcoin miner.py` — The mock miner script
- `index.html` — Live dashboard (real-time log viewer)
- `miner.log` — Log file (generated when the script runs)
- `README.md` — This file

## Features

- Real-time logging
- Simulated hashrate and share acceptance/rejection
- Clean terminal output
- Web dashboard with live updates

## Customization

Edit `bitcoin miner.py` to adjust:
- Pool address (`pool` variable)
- Worker name (`worker` variable)
- Accept rate and hashrate ranges
- Log update interval (`time.sleep()`)

---

**GitHub:** Ready to push! No external dependencies required (pure Python + HTML/JS).
