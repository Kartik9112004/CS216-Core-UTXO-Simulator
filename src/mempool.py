from src.validator import Validator


class Mempool:
    def __init__(self, max_size=50):
        self.transactions = []
        self.spent_utxos = {}
        self.max_size = max_size

    def add_transaction(self, tx, utxo_manager) -> (bool, str):
        if len(self.transactions) >= self.max_size:
            return False, "Mempool is full"

        is_valid, msg = Validator.validate_transaction(tx, utxo_manager, self)
        if not is_valid:
            return False, msg

        self.transactions.append(tx)

        for inp in tx["inputs"]:
            key = (inp["prev_tx"], inp["index"])
            self.spent_utxos[key] = tx["tx_id"]

        return True, "Transaction added to mempool"

    def remove_transaction(self, tx_id: str):
        tx_to_remove = None
        for tx in self.transactions:
            if tx["tx_id"] == tx_id:
                tx_to_remove = tx
                break

        if tx_to_remove:
            self.transactions.remove(tx_to_remove)
            for inp in tx_to_remove["inputs"]:
                key = (inp["prev_tx"], inp["index"])
                if key in self.spent_utxos:
                    del self.spent_utxos[key]

    def get_top_transactions(self, n: int) -> list:
        return self.transactions[:n]

    def clear(self):
        self.transactions = []
        self.spent_utxos = {}