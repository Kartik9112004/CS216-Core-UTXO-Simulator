import time
import random

def generate_tx_id():
    return f"tx_{int(time.time())}_{random.randint(1000, 9999)}"

class Transaction:
    @staticmethod
    def create_transaction(inputs, outputs):

        tx = {
            "tx_id": generate_tx_id(),
            "inputs": inputs,
            "outputs": outputs
        }
        return tx