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
* **UTXO Management:** Efficient tracking of unspent coins using unique identifiers.
* **Transaction Validation:** Strict enforcement of rules (input existence, signature checks, no double-spending).
* **Mempool Security:** Prevention of Race Attacks using "First-Seen" logic.
* **Mining Simulation:** Block creation, ledger updates, and miner fee collection.

---

## 2. Design Choices & Implementation
We implemented the simulation with a focus on efficiency and security logic as requested in the assignment.

### Data Structures
* **UTXO Set:** We used a **Python Dictionary** for the UTXO database.
    * *Key:* A tuple `(tx_id, index)` to uniquely identify every output.
    * *Value:* A dictionary `{'amount': float, 'owner': str}`.
    * *Reasoning:* This allows for **O(1)** time complexity when validating inputs, ensuring the simulation remains fast.

### Conflict Resolution (Double-Spending)
* **Internal Check:** The Validator ensures a single transaction does not reference the same UTXO twice in its own input list.
* **Mempool Locking (Race Attack Protection):** The `Mempool` class maintains a dictionary called `spent_utxos`. When a transaction enters the mempool, its inputs are mapped to the transaction ID. If a second transaction arrives trying to spend the same inputs, it is immediately rejected with a specific error identifying the conflicting transaction.

### Mining Logic
* The miner selects transactions from the mempool (FIFO basis), verifies them one last time, removes the spent inputs from the global UTXO set, and adds the new outputs.
* Miner fees are calculated dynamically (`Sum(Inputs) - Sum(Outputs)`) and awarded via a special Coinbase transaction.

---

## 3. How to Run the Program

### Prerequisites
* Python 3.8 or higher.
* No external libraries are required (uses standard `sys`, `time`, `random`, `os`).

### Steps
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/kartik9112004/CS216-Core-UTXO-Simulator.git](https://github.com/kartik9112004/CS216-Core-UTXO-Simulator.git)
    cd CS216-Core-UTXO-Simulator
    ```

2.  **Run the Main Simulator (CLI):**
    This starts the interactive menu where you can create transactions and mine blocks.
    ```bash
    python src/main.py
    ```

3.  **Run Test Scenarios:**
    You can run all tests or specific scenarios via the main menu (Option 5).
    Alternatively, run them directly from the terminal:
    ```bash
    # Run all 10 mandatory tests
    python -m tests.test_scenarios

    # Run specific double-spend test 
    python -m tests.test_scenarios double_spend
    ```

---

## 4. Bonus Status
* **Bonus Attempted:** **Yes**
* **Description:** We implemented **Unconfirmed Transaction Chaining (Test 10)**.
    1.  **Validator Update:** If an input is not found in the main UTXO set, the Validator searches the Mempool. If the parent transaction is found pending in the mempool, the input is accepted (simulating 0-conf chaining).
    2.  **Miner Update:** The mining function implements a **Topological Sort**. It builds a dependency graph of transactions in the block to ensure that a parent transaction is always mined *before* its child transaction, preventing invalid blocks.

---

## 5. Dependencies
* **Standard Libraries:** `time`, `random`, `sys`, `os`
* **External Packages:** None.