import json, psutil, os, subprocess, random, string

print("Checking if Ledger Live is running...\n")

for proc in psutil.process_iter():
    if proc.name() == "Ledger Live.exe":
        print(f"Terminating pid: {proc.pid}")
        try:
            proc.terminate()
        except:
            continue

print("Complete\n")

chains = {
    "ETH": {"name": "ethereum", "derivation": "44'/60'/0'/0/0"},
    "SOL": {"name": "solana", "derivation": "m/44'/501'/0'"},
}

option = input("Choice (ETH/SOL): ").upper()

while option not in ["ETH", "SOL"]:
    option = input("Choice (ETH/SOL): ").upper()

address = input("Address to add: ")
accName = input("Name for wallet (empty for random): ")

seedIdentifier = json.load(open("./seedIdentifier.json", "r"))["identifier"]

currency = chains[option]["name"]

if accName == "":
    accName = "".join(random.choice(string.ascii_letters) for _ in range(14))

accData = {
    "data": {
        "id": f"js:2:{currency}:{address}:",
        "name": accName,
        "seedIdentifier": seedIdentifier,
        "starred": False,
        "used": True,
        "derivationMode": "",
        "index": 1,
        "freshAddress": address,
        "freshAddressPath": chains[option]["derivation"],
        "freshAddresses": [
            {"address": address, "derivationPath": chains[option]["derivation"]}
        ],
        "blockHeight": 19019988,
        "syncHash": "0x9595c94",
        "creationDate": "2022-05-06T18:36:10.000Z",
        "operationsCount": 0,
        "operations": [],
        "pendingOperations": [],
        "currencyId": currency,
        "unitMagnitude": 18,
        "lastSyncDate": "2024-01-16T14:16:40.422Z",
        "balance": "0",
        "spendableBalance": "0",
        "nfts": [],
        "balanceHistoryCache": {},
        "subAccounts": [],
        "swapHistory": [],
    },
    "version": 1,
}

with open(f"{os.getenv('APPDATA')}\\Ledger Live\\app.json", "r+", encoding="utf8") as f:
    appJson = json.load(f)

    if not appJson["data"]["settings"]["lastSeenDevice"]:
        appJson["data"]["settings"] = json.load(
            open("baseSettings.json", "r", encoding="utf8")
        )

    if "accounts" not in appJson["data"]:
        appJson["data"]["accounts"] = []

    appJson["data"]["accounts"].append(accData)

    f.seek(0)
    f.truncate(0)

    f.write(json.dumps(appJson))

    f.close()

print(
    f"\nAccount added\nWallet Name: {accName}\nSeed Identifier: {seedIdentifier}\nLarp complete"
)
print("Attempting to open Ledger Live")

try:
    subprocess.Popen(["C:\\Program Files\\Ledger Live\\Ledger Live.exe"])
    print("\nSuccessfully ran Ledger Live.exe")
except:
    print("\nCouldn't open Ledger Live.")
