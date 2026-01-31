class Validator:
    @staticmethod
    def validate_transaction(tx, utxo_manager, mempool):
        inputs = tx.get("inputs", [])
        outputs = tx.get("outputs", [])

        total_in = 0.0
        input_keys = []

        for inp in inputs:
            prev_tx = inp["prev_tx"]
            idx = inp["index"]

            if utxo_manager.exists(prev_tx, idx):
                utxo = utxo_manager.utxo_set.get((prev_tx, idx))
            else:
                found_in_mempool = False
                for pending_tx in mempool.transactions:
                    if pending_tx["tx_id"] == prev_tx:
                        if idx < len(pending_tx["outputs"]):
                            utxo_data = pending_tx["outputs"][idx]
                            utxo = {"amount": utxo_data["amount"], "owner": utxo_data["address"]}
                            found_in_mempool = True
                            break

                if not found_in_mempool:
                    return False, f"Input {prev_tx}:{idx} does not exist"

            if utxo["owner"] != inp["owner"]:
                return False, f"Signature mismatch for input {prev_tx}:{idx}"

            total_in += utxo["amount"]
            input_keys.append((prev_tx, idx))

        if len(input_keys) != len(set(input_keys)):
            return False, "Double-spending detected within transaction inputs."

        total_out = sum(out["amount"] for out in outputs)
        for out in outputs:
            if out["amount"] < 0: return False, "Negative output."

        if total_in < total_out:
            return False, f"Insufficient funds"

        for key in input_keys:
            if key in mempool.spent_utxos:
                spender_id = mempool.spent_utxos[key]
                return False, f"Error: UTXO {key[0]}:{key[1]} already spent by {spender_id}"

        return True, "Transaction valid"