from qrlib.QRBot import QRBot
from CIBDeltaProcess import CIBDeltaProcess

class Bot(QRBot):

    def __init__(self):
        super().__init__()
        self.process = CIBDeltaProcess()

    def start(self):
        self.setup_platform_components()
        self.process.before_run()
        self.process.execute_run()

    def teardown(self):
        self.process.after_run()
