"""
Dust Sniffer — находит пылевые выходы (dust outputs) в Bitcoin-транзакциях.
"""

import requests
import sys

DUST_THRESHOLD_SATS = 546  # минимальный размер выхода (в сатоши), принятый за "dust"

def fetch_transaction(txid):
    url = f"https://blockstream.info/api/tx/{txid}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def analyze_tx(txid):
    print(f"🔍 Анализируем транзакцию {txid} на наличие dust-выходов...")
    tx = fetch_transaction(txid)

    dust_outputs = []
    for vout in tx.get("vout", []):
        value = vout.get("value", 0)
        if value <= DUST_THRESHOLD_SATS:
            dust_outputs.append({
                "value": value,
                "address": vout.get("scriptpubkey_address", "unknown")
            })

    if dust_outputs:
        print(f"⚠️ Найдено {len(dust_outputs)} пылевых выходов:")
        for d in dust_outputs:
            print(f" - {d['value']} sats → {d['address']}")
    else:
        print("✅ Пылевых выходов не обнаружено.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python dust_sniffer.py <txid>")
        sys.exit(1)

    txid = sys.argv[1]
    try:
        analyze_tx(txid)
    except Exception as e:
        print("Ошибка:", e)
