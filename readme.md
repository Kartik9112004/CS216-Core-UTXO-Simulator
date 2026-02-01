# CS216 Assignment 2: UTXO Simulator

### Team Details
**Team Name:** Core

| Name | Roll Number |
| :--- | :--- |
| Kartik Budhani | 240005022 |
| Rishan Bansi Gobse | 240008023 |
| Arjun Mahesh Dhamdhere | 240005011 |
| Krishnam Bhanwarlal Digga | 240003043 |

---

## 1. Project Description
This project is a simplified, local simulation of the Bitcoin **UTXO (Unspent Transaction Output)** model implemented in Python. It demonstrates the lifecycle of a transaction from creation to validation, mempool buffering, and final confirmation via mining.

Key features include:
* **UTXO Management:** Efficient tracking of unspent coins using unique identifiers `(tx_id, index)`.
* **Transaction Validation:** Strict enforcement of rules (input existence in confirmed set, signature checks, input >= output).
* **Mempool Security:** Prevention of Race Attacks using "First-Seen" logic.
* **Mining Simulation:** Block creation using FIFO selection and miner fee calculation.

---

## 2. Implementation Details
We implemented the simulation focusing on strict compliance with the Bitcoin protocol logic tailored for this assignment.

### Data Structures
* **UTXO Set:** A Python Dictionary `{(tx_id, index): {'amount': float, 'owner': str}}` for O(1) validation lookup.
* **Mempool:** A List for transactions and a Dictionary `spent_utxos` to track inputs used by pending transactions.

### Conflict Resolution
* **Double-Spending:** Addressed at two levels:
    1.  **Intra-Transaction:** A single transaction cannot reference the same input twice.
    2.  **Mempool (Race Attack):** If an input is already locked by a pending transaction, subsequent attempts to spend it are rejected immediately.

### Mining Logic
* The miner selects transactions from the mempool in **First-In-First-Out (FIFO)** order.
* It verifies inputs against the current UTXO set, removes spent inputs, adds new outputs, and awards the net fee to the miner via a Coinbase transaction.

---

## 3. How to Run the Program

### Prerequisites
* Python 3.8 or higher.
* No external libraries required.

### Steps
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/kartik9112004/CS216-Core-UTXO-Simulator.git](https://github.com/kartik9112004/CS216-Core-UTXO-Simulator.git)
    cd CS216-Core-UTXO-Simulator
    ```

2.  **Run the Main Simulator (CLI):**
    ```bash
    python src/main.py
    ```

3.  **Run Test Scenarios:**
    ```bash
    # Run all 10 mandatory tests
    python -m tests.test_scenarios

    # Run specific double-spend test (matches PDF output)
    python -m tests.test_scenarios 4
    ```

---

## 4. Bonus Status
* **Bonus Attempted:** **No**
* **Note on Test 10:** We implemented the "Standard Rule" for Test 10. Transactions spending unconfirmed outputs (chained transactions) are **rejected** until the parent transaction is mined.