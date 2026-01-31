import sys
import os

# Ensure src modules can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utxo_manager import UTXOManager
from src.mempool import Mempool
from src.transaction import Transaction
from src.block import mine_block


def main():
    utxo_manager = UTXOManager()
    mempool = Mempool()

    # Initialize Genesis Block
    utxo_manager.add_utxo("genesis", 0, 50.0, "Alice")
    utxo_manager.add_utxo("genesis", 1, 30.0, "Bob")
    utxo_manager.add_utxo("genesis", 2, 20.0, "Charlie")
    utxo_manager.add_utxo("genesis", 3, 10.0, "David")
    utxo_manager.add_utxo("genesis", 4, 5.0, "Eve")

    while True:
        print("\n=== Bitcoin Transaction Simulator ===")
        print("Initial UTXOs (Genesis Block):")
        print("Alice: 50.0 BTC\nBob: 30.0 BTC\nCharlie: 20.0 BTC\nDavid: 10.0 BTC\nEve: 5.0 BTC")
        print("Main Menu:")
        print("1. Create new transaction")
        print("2. View UTXO set")
        print("3. View mempool")
        print("4. Mine block")
        print("5. Run test scenarios")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            sender = input("Enter sender: ")
            balance = utxo_manager.get_balance(sender)
            print(f"Available balance: {balance}")

            if balance == 0:
                print("Error: Sender has no funds.")
                continue

            recipient = input("Enter recipient: ")
            try:
                val = input("Enter amount: ").replace("BTC", "").strip()
                amount = float(val)
            except ValueError:
                print("Invalid amount.")
                continue

            user_utxos = utxo_manager.get_utxos_for_owner(sender)
            inputs = []
            input_sum = 0.0

            for utxo in user_utxos:
                inputs.append({
                    "prev_tx": utxo["tx_id"],
                    "index": utxo["index"],
                    "owner": sender
                })
                input_sum += utxo["amount"]
                if input_sum >= amount + 0.001:
                    break

            if input_sum < amount:
                print("Error: Insufficient funds.")
                continue

            fee = 0.001
            change = input_sum - amount - fee

            outputs = [{"amount": amount, "address": recipient}]
            if change > 0:
                outputs.append({"amount": change, "address": sender})

            print("Creating transaction...")
            tx = Transaction.create_transaction(inputs, outputs)
            success, msg = mempool.add_transaction(tx, utxo_manager)

            if success:
                print(f"Transaction valid! Fee: {fee:.3f} BTC")
                print(f"Transaction ID: {tx['tx_id']}")
                print("Transaction added to mempool.")
                print(f"Mempool now has {len(mempool.transactions)} transactions.")
            else:
                print(f"Transaction Rejected: {msg}")

        elif choice == "2":
            print("\n--- Current UTXO Set ---")
            for key, data in utxo_manager.utxo_set.items():
                print(f"{key}: {data['amount']} BTC ({data['owner']})")

        elif choice == "3":
            print(f"\n--- Mempool ({len(mempool.transactions)} transactions) ---")
            for tx in mempool.transactions:
                print(f"TxID: {tx['tx_id']} | Inputs: {len(tx['inputs'])} | Outputs: {len(tx['outputs'])}")

        elif choice == "4":
            miner = input("Enter miner name: ")
            mine_block(miner, mempool, utxo_manager)

        elif choice == "5":
            # --- FIXED: Now passes the specific number to the script ---
            sub_choice = input("Select test scenario (1-10) or Press Enter for all: ").strip()
            if not sub_choice:
                sub_choice = "all"
            print(f"Running scenario: {sub_choice}...")
            os.system(f"{sys.executable} -m tests.test_scenarios {sub_choice}")

        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()