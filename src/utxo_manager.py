class UTXOManager:
    def __init__(self):

        self.utxo_set = {}


    def add_utxo(self, tx_id: str, index: int, amount: float, owner: str):
        self.utxo_set[(tx_id, index)] = {"amount": amount, "owner": owner}



    def remove_utxo(self, tx_id: str, index: int):

        if (tx_id, index) in self.utxo_set:
            del self.utxo_set[(tx_id, index)]



    def get_balance(self, owner: str) -> float:

        balance = 0.0
        for data in self.utxo_set.values():
            if data["owner"] == owner:
                balance += data["amount"]
        return balance

    def exists(self, tx_id: str, index: int) -> bool:
        return (tx_id, index) in self.utxo_set

    def get_utxos_for_owner(self, owner: str) -> list:
        """Get all UTXOs owned by an address."""
        owned_utxos = []
        for key, data in self.utxo_set.items():
            if data["owner"] == owner:
                owned_utxos.append({
                    "tx_id": key[0],
                    "index": key[1],
                    "amount": data["amount"]
                })
        return owned_utxos