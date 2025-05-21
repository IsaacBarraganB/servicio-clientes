from project.adapters.receipt.ReceiptAdapter import ReceiptAdapter

class ReceiptsStatusContext:
    def __init__(self, receipt: ReceiptAdapter):
        self.receipt = receipt
    
    def execute_receipt(self, id, schema, config=None, compose=None):
        return self.receipt.change_status(id=id, schema=schema, config=config, compose=compose)