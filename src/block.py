import heapq


def mine_block(miner_address, mempool, utxo_manager, num_txs=5):
    pending_txs = mempool.transactions[:]
    if not pending_txs:
        return

    tx_lookup = {tx["tx_id"]: tx for tx in pending_txs}
    dependency_count = {tx["tx_id"]: 0 for tx in pending_txs}
    dependency_graph = {tx["tx_id"]: [] for tx in pending_txs}

    for tx in pending_txs:
        for inp in tx["inputs"]:
            parent_id = inp["prev_tx"]
            if parent_id in tx_lookup:
                dependency_graph[parent_id].append(tx["tx_id"])
                dependency_count[tx["tx_id"]] += 1

    candidate_queue = []

    for tx in pending_txs:
        if dependency_count[tx["tx_id"]] == 0:
            fee = tx.get("fee", 0)
            heapq.heappush(candidate_queue, (-fee, tx["tx_id"], tx))

    final_block_txs = []

    while len(final_block_txs) < num_txs and candidate_queue:
        neg_fee, tx_id, current_tx = heapq.heappop(candidate_queue)
        final_block_txs.append(current_tx)

        if tx_id in dependency_graph:
            for child_id in dependency_graph[tx_id]:
                dependency_count[child_id] -= 1
                if dependency_count[child_id] == 0:
                    child_tx = tx_lookup[child_id]
                    child_fee = child_tx.get("fee", 0)
                    heapq.heappush(candidate_queue, (-child_fee, child_id, child_tx))

    local_utxo_lookup = {}
    total_block_reward = 0.0

    for tx in final_block_txs:
        input_total = 0.0

        for inp in tx["inputs"]:
            utxo_key = (inp["prev_tx"], inp["index"])

            if utxo_manager.exists(*utxo_key):
                utxo_data = utxo_manager.utxo_set[utxo_key]
                input_total += utxo_data["amount"]
                utxo_manager.remove_utxo(*utxo_key)

            elif utxo_key in local_utxo_lookup:
                input_total += local_utxo_lookup[utxo_key]

        output_total = 0.0
        for index, out in enumerate(tx["outputs"]):
            amount = out["amount"]
            output_total += amount
            utxo_manager.add_utxo(tx["tx_id"], index, amount, out["address"])
            local_utxo_lookup[(tx["tx_id"], index)] = amount

        total_block_reward += (input_total - output_total)

    if total_block_reward >= 0:
        coinbase_tx_id = f"coinbase_{final_block_txs[0]['tx_id']}"
        utxo_manager.add_utxo(coinbase_tx_id, 0, total_block_reward, miner_address)

    for tx in final_block_txs:
        mempool.remove_transaction(tx["tx_id"])