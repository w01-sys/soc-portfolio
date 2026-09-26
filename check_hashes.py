import os
import requests
import time

API_KEY = os.getenv("VT_API_KEY")

if not API_KEY:
    print("❌ VT_API_KEY environment variable is not set.")
    print('Run: export VT_API_KEY="your-api-key"')
    exit(1)

hashes = [
    "9f2b4c6d7e8a3f1c5b9d2e0f4a7c3b6e8d1f2a5c9b0d7e3f6a2c4b8e9d1f51c6", "3d8c9a2b6e7d1f0a5c3b9e8d7f6a2c9b4e3d1f5a7c6e0b9d2f4a3c1e8b7d62f5", "156335b95ba216456f1ac0894b7b9d6ad95404ac7df447941f21646ca0090673", "6d7e8a3f1c5b9d2e0f4a7c3b6e8d1f2a5c9b0d7e3f6a2c4b8e9d1f5a9f2b47e8", "0f4a7c3b6e8d1f2a5c9b0d7e3f6a2c4b8e9d1f5a9f2b4c6d7e8a3f1c5b9d26a4", "f837f1cd60e9941aa60f7be50a8f2aaaac380f560db8ee001408f35c1b7a97cb", "156335b95ba216456f1ac0894b7b9d6ad95404ac7df447946f21646ca0090673", "7e3f6a2c4b8e9d1f5a9f2b4c6d7e8a3f1c5b9d2e0f4a7c3b6e8d1f2a5c9b05d6", "5b9d2e0f4a7c3b6e8d1f2a5c9b0d7e3f6a2c4b8e9d1f5a9f2b4c6d7e8a3f13d7", "6a2c4b8e9d1f5a9f2b4c6d7e8a3f1c5b9d2e0f4a7c3b6e8d1f2a5c9b0d7e35f1", "156335b95ba216456f1ac0894b7b9d6ad95404ac7df447948f21646ca0090673", "d55f983c994caa160ec63a59f6b4250fe67fb3e8c43a388aec60a4a6978e9f1e", "1f5a9f2b4c6d7e8a3f1c5b9d2e0f4a7c3b6e8d1f2a5c9b0d7e3f6a2c4b8e97c5", "156335b95ba216456f1ac0894b7b9d6ad95404ac7df447943f21646ca0090673", "5c9b0d7e3f6a2c4b8e9d1f5a9f2b4c6d7e8a3f1c5b9d2e0f4a7c3b6e8d1f28a9", "156335b95ba216456f1ac0894b7b9d6ad95404ac7df447945f21646ca0090673", "01cd4320fa28bc47325ccbbce573ed5c5356008ab0dd1f450017e042cb631239", "0a9f2b4c6d7e8a3f1c5b9d2e0f4a7c3b6e8d1f2a5c9b0d7e3f6a2c4b8e9d12f6", "156335b95ba216456f1ac0894b7b9d6ad95404ac7df447940f21646ca0090673", "6c4b8e9d1f5a9f2b4c6d7e8a3f1c5b9d2e0f4a7c3b6e8d1f2a5c9b0d7e3f51b9", "156335b95ba216456f1ac0894b7b9d6ad95404ac7df447947f21646ca0090673", "156335b95ba216456f1ac0894b7b9d6ad95404ac7df447944f21646ca0090673", "feb3e6d30ba573ba23f3bd1291ca173b7879706d1fe039c34d53a4fdcdf33ede", "1d5a9f2b4c6d7e8a3f1c5b9d2e0f4a7c3b6e8d1f2a5c9b0d7e3f6a2c4b8e94a7", "5e8d1f2a5c9b0d7e3f6a2c4b8e9d1f5a9f2b4c6d7e8a3f1c5b9d2e0f4a7c34c8", "1f5a9f2b4c6d7e8a3f1c5b9d2e0f4a7c3b6e8d1f2a5c9b0d7e3f6a2c4b8e93a7", "156335b95ba216456f1ac0894b7b9d6ad95404ac7df447942f21646ca0090673", "9b2e0f4a7c3b6e8d1f2a5c9b0d7e3f6a2c4b8e9d1f5a9f2b4c6d7e8a3f1c58d3", "7e3f6a2c4b8e9d1f5a9f2b4c6d7e8a3f1c5b9d2e0f4a7c3b6e8d1f2a5c9b05d6", "6c6d7e8a3f1c5b9d2e0f4a7c3b6e8d1f2a5c9b0d7e3f6a2c4b8e9d1f5a9f20f4", "5b8d1f2a5c9b0d7e3f6a2c4b8e9d1f5a9f2b4c6d7e8a3f1c5b9d2e0f4a7c13e9"

]

url_base = "https://www.virustotal.com/api/v3/files"
headers = {
    "x-apikey": API_KEY
}

for index, file_hash in enumerate(hashes):

    print(f"\n🔍 Checking: {file_hash}")

    url = f"{url_base}/{file_hash}"

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 404:
            print(f"⏳ No VirusTotal record found for {file_hash}")
            continue

        if response.status_code == 429:
            print("⚠️ VirusTotal rate limit reached.")
            print("Waiting 60 seconds...")
            time.sleep(60)
            continue

        response.raise_for_status()

        data = response.json()

        attributes = data["data"]["attributes"]

        stats = attributes.get("last_analysis_stats", {})
        vendors = attributes.get("last_analysis_results", {})

        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)

        print(f"Malicious:  {malicious}")
        print(f"Suspicious: {suspicious}")

        if malicious > 0:

            print(f"\n⚠️ {file_hash} is flagged as malicious.")

            print("\nDetection results:")

            for vendor, result in vendors.items():

                if result.get("category") == "malicious":

                    detection = result.get("result", "Unknown")

                    print(f" - {vendor}: {detection}")

        elif suspicious > 0:

            print(f"\n⚠️ {file_hash} has suspicious detections.")

        else:

            print(f"\n✅ {file_hash} has no malicious detections.")

    except requests.exceptions.RequestException as error:

        print(f"❌ Request failed: {error}")

    except (KeyError, ValueError) as error:

        print(f"❌ Unexpected VirusTotal response: {error}")

    # Respect the public API rate limit
    if (index + 1) % 4 == 0 and index + 1 < len(hashes):

        print("\n⏳ Waiting 60 seconds to respect the API rate limit...")
        time.sleep(60)
