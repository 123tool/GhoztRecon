# 🛡️ GhoztRecon 
**GhoztRecon** is an advanced URL and endpoint discovery tool built for high-speed reconnaissance in bug bounty programs. It aggregates data from multiple OSINT sources and provides smart filtering for professional hunters.

## 🚀 Main Features
- **Multi-Source Mining:** Wayback Machine & AlienVault OTX.
- **Secret Detection:** Built-in regex to find exposed API keys, Firebase, and S3 buckets.
- **Live Status Validation:** Verify if the discovered endpoints are still active (`--live`).
- **Professional Filtering:** Narrow down to JavaScript files (`-x`) or query parameters (`--param`).
- **Terminal Optimization:** Works perfectly on Linux and **Termux**.

## 📥 Quick Installation
```bash
git clone [https://github.com/123tool/GhoztRecon.git]
cd GhoztRecon
pip install .
