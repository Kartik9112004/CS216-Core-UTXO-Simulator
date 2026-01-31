def mine_block(miner_address: str, mempool, utxo_manager, num_txs=5):
    raw_txs = mempool.transactions[:]
    if not raw_txs:
        print("No transactions to mempool.")
        return

    print("Mining block...")

    tx_map = {tx["tx_id"]: tx for tx in raw_txs}
    dependencies = {tx["tx_id"]: set() for tx in raw_txs}

    for tx in raw_txs:
        for inp in tx["inputs"]:
            parent_id = inp["prev_tx"]
            if parent_id in tx_map:
                dependencies[tx["tx_id"]].add(parent_id)

    selected_txs = []
    mined_ids = set()

    while len(selected_txs) < num_txs and raw_txs:
        candidates = []
        for tx in raw_txs:
            deps = dependencies[tx["tx_id"]]
            if deps.issubset(mined_ids):
                candidates.append(tx)

        if not candidates:
            break

        best_tx = candidates[0]
        selected_txs.append(best_tx)
        mined_ids.add(best_tx["tx_id"])
        raw_txs.remove(best_tx)

    txs_to_mine = selected_txs
    print(f"Selected {len(txs_to_mine)} transactions from mempool.")

    total_fee = 0.0

    for tx in txs_to_mine:
        input_sum = 0.0
        for inp in tx["inputs"]:
            if utxo_manager.exists(inp["prev_tx"], inp["index"]):
                utxo = utxo_manager.utxo_set[(inp["prev_tx"], inp["index"])]
                input_sum += utxo["amount"]
                utxo_manager.remove_utxo(inp["prev_tx"], inp["index"])
            else:
                for parent in txs_to_mine:
                    if parent["tx_id"] == inp["prev_tx"]:
                        input_sum += parent["outputs"][inp["index"]]["amount"]
                        break

        output_sum = 0.0
        for i, out in enumerate(tx["outputs"]):
            output_sum += out["amount"]
            utxo_manager.add_utxo(tx["tx_id"], i, out["amount"], out["address"])

        total_fee += (input_sum - output_sum)

    print(f"Total fees: {total_fee:.3f} BTC")

    if total_fee >= 0:
        coinbase_id = "coinbase_" + txs_to_mine[0]["tx_id"]
        utxo_manager.add_utxo(coinbase_id, 0, total_fee, miner_address)
        print(f"Miner {miner_address} receives {total_fee:.3f} BTC")

    print("Block mined successfully!")

    for tx in txs_to_mine:
        mempool.remove_transaction(tx["tx_id"])

    print(f"Removed {len(txs_to_mine)} transactions from mempool.")