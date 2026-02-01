import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utxo_manager import UTXOManager
from src.mempool import Mempool
from src.transaction import Transaction
from src.block import mine_block

if sys.platform == "win32":
    os.system('color')


class Colors:
    HEADER = '\033[95m'  # Magenta
    BLUE = '\033[94m'  # Blue
    CYAN = '\033[96m'  # Cyan
    GREEN = '\033[92m'  # Green
    RED = '\033[91m'  # Red
    GOLD = '\033[93m'  # Yellow/Gold
    BOLD = '\033[1m'  # Bold
    RESET = '\033[0m'  # Reset
    WHITE = '\033[97m'  # White


def main():
    utxo_manager = UTXOManager()
    mempool = Mempool()

    utxo_manager.add_utxo("genesis", 0, 50.0, "Alice")
    utxo_manager.add_utxo("genesis", 1, 30.0, "Bob")
    utxo_manager.add_utxo("genesis", 2, 20.0, "Charlie")
    utxo_manager.add_utxo("genesis", 3, 10.0, "David")
    utxo_manager.add_utxo("genesis", 4, 5.0, "Eve")

    while True:
        print(f"\n{Colors.BOLD}{Colors.GOLD}=== Bitcoin Transaction Simulator ==={Colors.RESET}")

        print(f"{Colors.HEADER}Initial UTXOs (Genesis Block):{Colors.RESET}")
        print(
            f"{Colors.CYAN}Alice:{Colors.RESET} {Colors.GOLD}50.0 BTC{Colors.RESET}\n{Colors.CYAN}Bob:{Colors.RESET} {Colors.GOLD}30.0 BTC{Colors.RESET}\n{Colors.CYAN}Charlie:{Colors.RESET} {Colors.GOLD}20.0 BTC{Colors.RESET}\n{Colors.CYAN}David:{Colors.RESET} {Colors.GOLD}10.0 BTC{Colors.RESET}\n{Colors.CYAN}Eve:{Colors.RESET} {Colors.GOLD}5.0 BTC{Colors.RESET}")

        print(f"{Colors.HEADER}Main Menu:{Colors.RESET}")
        print(f"{Colors.CYAN}1.{Colors.RESET} Create new transaction")
        print(f"{Colors.CYAN}2.{Colors.RESET} View UTXO set")
        print(f"{Colors.CYAN}3.{Colors.RESET} View mempool")
        print(f"{Colors.CYAN}4.{Colors.RESET} Mine block")
        print(f"{Colors.CYAN}5.{Colors.RESET} Run test scenarios")
        print(f"{Colors.CYAN}6.{Colors.RESET} Exit")

        choice = input(f"{Colors.GREEN}Enter choice: {Colors.RESET}")

        if choice == "1":
            sender = input(f"{Colors.WHITE}Enter sender: {Colors.RESET}")
            balance = utxo_manager.get_balance(sender)
            print(f"Available balance: {Colors.GOLD}{balance}{Colors.RESET}")

            if balance == 0:
                print(f"{Colors.RED}Error: Sender has no funds.{Colors.RESET}")
                continue

            recipient = input(f"{Colors.WHITE}Enter recipient: {Colors.RESET}")
            try:
                val = input(f"{Colors.WHITE}Enter amount: {Colors.RESET}").replace("BTC", "").strip()
                amount = float(val)
            except ValueError:
                print(f"{Colors.RED}Invalid amount.{Colors.RESET}")
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
                print(f"{Colors.RED}Error: Insufficient funds.{Colors.RESET}")
                continue

            fee = 0.001
            change = input_sum - amount - fee

            outputs = [{"amount": amount, "address": recipient}]
            if change > 0:
                outputs.append({"amount": change, "address": sender})

            print(f"{Colors.BLUE}Creating transaction...{Colors.RESET}")
            tx = Transaction.create_transaction(inputs, outputs)
            success, msg = mempool.add_transaction(tx, utxo_manager)

            if success:
                print(f"{Colors.GREEN}Transaction valid!{Colors.RESET} Fee: {Colors.GOLD}{fee:.3f} BTC{Colors.RESET}")
                print(f"Transaction ID: {Colors.CYAN}{tx['tx_id']}{Colors.RESET}")
                print(f"{Colors.GREEN}Transaction added to mempool.{Colors.RESET}")
                print(f"Mempool now has {Colors.BOLD}{len(mempool.transactions)}{Colors.RESET} transactions.")
            else:
                print(f"{Colors.RED}Transaction Rejected: {msg}{Colors.RESET}")

        elif choice == "2":
            print(f"\n{Colors.BLUE}--- Current UTXO Set ---{Colors.RESET}")
            for key, data in utxo_manager.utxo_set.items():
                print(
                    f"{Colors.CYAN}{key}{Colors.RESET}: {Colors.GOLD}{data['amount']} BTC{Colors.RESET} ({data['owner']})")

        elif choice == "3":
            print(f"\n{Colors.BLUE}--- Mempool ({len(mempool.transactions)} transactions) ---{Colors.RESET}")
            for tx in mempool.transactions:
                print(
                    f"TxID: {Colors.CYAN}{tx['tx_id']}{Colors.RESET} | Inputs: {len(tx['inputs'])} | Outputs: {len(tx['outputs'])}")

        elif choice == "4":
            miner = input(f"{Colors.WHITE}Enter miner name: {Colors.RESET}")
            mine_block(miner, mempool, utxo_manager)

        elif choice == "5":
            sub_choice = input(
                f"{Colors.WHITE}Select test scenario (1-10) or Press Enter for all: {Colors.RESET}").strip()
            if not sub_choice:
                sub_choice = "all"
            print(f"{Colors.BLUE}Running scenario: {sub_choice}...{Colors.RESET}")
            os.system(f"{sys.executable} -m tests.test_scenarios {sub_choice}")

        elif choice == "6":
            print(f"{Colors.GREEN}Exiting...{Colors.RESET}")
            break
        else:
            print(f"{Colors.RED}Invalid choice.{Colors.RESET}")


if __name__ == "__main__":
    main()