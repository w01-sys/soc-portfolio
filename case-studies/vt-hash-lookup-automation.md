# VirusTotal Hash Lookup Automation

## Objective

Manually checking file hashes against threat intelligence sources during
triage is slow and doesn't scale past a handful of indicators. This project
automates that step: a Python script takes a list of file hashes and checks
each one against the VirusTotal v3 API, reporting whether it's known
malicious, clean, or unseen — without an analyst having to paste hashes into
a browser one at a time.

## Tools Used

- Python 3
- `requests` library
- VirusTotal API v3 (`/files/{hash}` endpoint)
- macOS Terminal, virtual environment (`venv`)

## Workflow

```
Alert / File
     │
     ▼
Extract Hash
     │
     ▼
Python Script
     │
     ▼
VirusTotal API
     │
     ├── Malicious / Suspicious detections
     │        │
     │        ▼
     │   Investigate / Escalate
     │
     └── No detections / No record
              │
              ▼
        Continue investigation
```

The script reads each hash from a list, queries VirusTotal, and prints a
summary of vendor detections when a hash is flagged. It respects the public
API's rate limit (4 requests/minute) by pausing between batches, and handles
missing records, rate-limit responses, and malformed hashes without crashing
the run.

The API key is never hardcoded — it's read from an environment variable at
runtime:

```python
API_KEY = os.getenv("VT_API_KEY")
```

## Sample Output

Running the script against a batch of hashes correctly identified two known
ransomware families and one that had already been added to VirusTotal from
earlier submissions, alongside several hashes with no matching record:

```
🔍 Checking: f837f1cd60e9941aa60f7be50a8f2aaaac380f560db8ee001408f35c1b7a97cb
Malicious:  62
Suspicious: 0

⚠️ f837f1cd60e9941aa60f7be50a8f2aaaac380f560db8ee001408f35c1b7a97cb is flagged as malicious.

Detection results:
 - CrowdStrike: win/malicious_confidence_100% (W)
 - ESET-NOD32: Win32/Filecoder.BlackCat.A trojan
 - Symantec: Ransom.Noberus
 - Kaspersky: HEUR:Trojan-Ransom.Win32.Generic
 ...
```

This particular hash was identified as **BlackCat/ALPHV ransomware** by 62 of
the vendors queried. A second hash in the same batch was identified as
**REvil/Sodinokibi**, and a third as **DearCry**. Several other hashes in the
test batch returned no VirusTotal record, which the script reports clearly
rather than treating as an error.

*(See `/screenshots` for full terminal captures of each run.)*

## Skills Demonstrated

- API integration and authentication (environment-variable-based secrets,
  never hardcoded)
- Rate-limit handling and retry logic
- Error handling for network failures, missing records, and malformed input
- Reading and interpreting multi-vendor threat intelligence output
- Basic IOC triage workflow (hash → lookup → detection → decision)

## Lessons Learned

While testing this script, I initially exported my VirusTotal API key
directly in a terminal session that was later shared for troubleshooting.
This meant the key was briefly exposed outside my local environment.

Once I recognised the exposure, I:

- Regenerated the API key via VirusTotal's account settings, immediately
  invalidating the old one
- Reviewed the script to confirm it never hardcodes the key, and instead
  reads it from an environment variable (`os.getenv("VT_API_KEY")`)
- Added `.gitignore` rules to keep the virtual environment and result files
  out of version control
- Adopted the habit of referring to secrets as "set" rather than pasting
  their values when sharing terminal output for debugging

This reinforced a core operational security principle: credentials should be
treated as compromised the moment they're exposed outside their intended
context, regardless of intent, and rotated immediately rather than assessed
for risk first.
