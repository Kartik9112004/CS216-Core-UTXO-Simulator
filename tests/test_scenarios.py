import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utxo_manager import UTXOManager
from src.mempool import Mempool
from src.transaction import Transaction
from src.block import mine_block


def run_tests():
    target = "all"
    if len(sys.argv) > 1:
        target = sys.argv[1].lower()

    if target == "all":
        print("=== Running All 10 Mandatory Test Scenarios ===\n")
    else:
        print(f"=== Running Test Scenario: {target} ===\n")

    if target == "all" or target == "1":
        print("[Test 1] Basic Valid Transaction")
        utxo = UTXOManager()
        mempool = Mempool()
        utxo.add_utxo("genesis", 0, 50.0, "Alice")

        tx1 = Transaction.create_transaction(
            [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
            [{"amount": 10.0, "address": "Bob"}, {"amount": 39.999, "address": "Alice"}]
        )
        success, msg = mempool.add_transaction(tx1, utxo)
        print(f"Result: {success} ({msg}) - Expected: True")
        print("-" * 30)

    if target == "all" or target == "2":
        print("[Test 2] Multiple Inputs (50 + 20 -> 60)")
        utxo = UTXOManager()
        mempool = Mempool()
        utxo.add_utxo("genesis", 0, 50.0, "Alice")
        utxo.add_utxo("genesis", 1, 20.0, "Alice")

        tx2 = Transaction.create_transaction(
            [
                {"prev_tx": "genesis", "index": 0, "owner": "Alice"},
                {"prev_tx": "genesis", "index": 1, "owner": "Alice"}
            ],
            [{"amount": 69.999, "address": "Bob"}]
        )
        success, msg = mempool.add_transaction(tx2, utxo)
        print(f"Result: {success} ({msg}) - Expected: True")
        print("-" * 30)

    if target == "all" or target == "3":
        print("[Test 3] Double-Spend in Same Transaction")
        utxo = UTXOManager()
        mempool = Mempool()
        utxo.add_utxo("genesis", 0, 50.0, "Alice")

        tx3 = Transaction.create_transaction(
            [
                {"prev_tx": "genesis", "index": 0, "owner": "Alice"},
                {"prev_tx": "genesis", "index": 0, "owner": "Alice"}
            ],
            [{"amount": 100.0, "address": "Bob"}]
        )
        success, msg = mempool.add_transaction(tx3, utxo)
        print(f"Result: {success} ({msg}) - Expected: False")
        print("-" * 30)

    if target == "all" or target == "4" or target == "double_spend":
        print("[Test 4] Mempool Double-Spend (Race Attack)")
        print("Test: Alice tries to spend same UTXO twice")
        utxo = UTXOManager()
        mempool = Mempool()
        utxo.add_utxo("genesis", 0, 50.0, "Alice")

        tx1 = Transaction.create_transaction(
            [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
            [{"amount": 10.0, "address": "Bob"}, {"amount": 39.999, "address": "Alice"}]
        )
        tx1["tx_id"] = "tx_alice_bob_001"
        success1, msg1 = mempool.add_transaction(tx1, utxo)
        print(f"TX1: Alice -> Bob (10 BTC) - {'VALID' if success1 else 'REJECTED'}")

        tx2 = Transaction.create_transaction(
            [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
            [{"amount": 10.0, "address": "Charlie"}]
        )
        success2, msg2 = mempool.add_transaction(tx2, utxo)
        print(f"TX2: Alice -> Charlie (10 BTC) - {'VALID' if success2 else 'REJECTED'}")

        if not success2:
            print(f"{msg2}")
        print("-" * 30)

    if target == "all" or target == "5":
        print("[Test 5] Insufficient Funds")
        utxo = UTXOManager()
        mempool = Mempool()
        utxo.add_utxo("genesis", 1, 30.0, "Bob")

        tx5 = Transaction.create_transaction(
            [{"prev_tx": "genesis", "index": 1, "owner": "Bob"}],
            [{"amount": 35.0, "address": "Alice"}]
        )
        success, msg = mempool.add_transaction(tx5, utxo)
        print(f"Result: {success} ({msg}) - Expected: False")
        print("-" * 30)

    if target == "all" or target == "6":
        print("[Test 6] Negative Amount")
        utxo = UTXOManager()
        mempool = Mempool()
        utxo.add_utxo("genesis", 0, 50.0, "Alice")

        tx6 = Transaction.create_transaction(
            [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
            [{"amount": -5.0, "address": "Bob"}]
        )
        success, msg = mempool.add_transaction(tx6, utxo)
        print(f"Result: {success} ({msg}) - Expected: False")
        print("-" * 30)

    if target == "all" or target == "7":
        print("[Test 7] Zero Fee Transaction")
        utxo = UTXOManager()
        mempool = Mempool()
        utxo.add_utxo("genesis", 2, 50.0, "Alice")

        tx7 = Transaction.create_transaction(
            [{"prev_tx": "genesis", "index": 2, "owner": "Alice"}],
            [{"amount": 50.0, "address": "Bob"}]
        )
        success, msg = mempool.add_transaction(tx7, utxo)
        print(f"Result: {success} ({msg}) - Expected: True")
        print("-" * 30)

    if target == "all" or target == "8":
        print("[Test 8] Race Attack Simulation")
        utxo = UTXOManager()
        mempool = Mempool()
        utxo.add_utxo("genesis", 0, 50.0, "Alice")

        tx8a = Transaction.create_transaction(
            [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
            [{"amount": 50.0, "address": "Merchant"}]
        )
        mempool.add_transaction(tx8a, utxo)

        tx8b = Transaction.create_transaction(
            [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
            [{"amount": 49.0, "address": "Attacker"}]
        )
        success, msg = mempool.add_transaction(tx8b, utxo)
        print(f"Result: {success} ({msg}) - Expected: False")
        print("-" * 30)

    if target == "all" or target == "9":
        print("[Test 9] Complete Mining Flow")
        utxo = UTXOManager()
        mempool = Mempool()
        utxo.add_utxo("genesis", 0, 50.0, "Alice")

        tx9 = Transaction.create_transaction(
            [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
            [{"amount": 10.0, "address": "Bob"}, {"amount": 39.0, "address": "Alice"}]
        )
        mempool.add_transaction(tx9, utxo)

        mine_block("Miner1", mempool, utxo, num_txs=1)

        is_mempool_empty = len(mempool.transactions) == 0
        print(f"Result: {is_mempool_empty} - Expected: True")
        print("-" * 30)

    if target == "all" or target == "10":
        print("[Test 10] Unconfirmed Chain")
        utxo = UTXOManager()
        mempool = Mempool()
        utxo.add_utxo("genesis", 0, 50.0, "Alice")

        tx_a = Transaction.create_transaction(
            [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
            [{"amount": 50.0, "address": "Bob"}]
        )
        mempool.add_transaction(tx_a, utxo)

        tx_b = Transaction.create_transaction(
            [{"prev_tx": tx_a["tx_id"], "index": 0, "owner": "Bob"}],
            [{"amount": 50.0, "address": "Charlie"}]
        )

        success, msg = mempool.add_transaction(tx_b, utxo)
        print(f"Result: {success} ({msg}) - Expected: False")
        print("-" * 30)

    print("=== Tests Complete ===")


if __name__ == "__main__":
    run_tests()