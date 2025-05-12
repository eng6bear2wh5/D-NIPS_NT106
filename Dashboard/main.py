########################################################################
## QT GUI BY SPINN TV(YOUTUBE)
########################################################################
import os
import sys
import threading # Added for running Flask API in a separate thread
########################################################################
# IMPORT GUI FILE
from src.ui_interface import *
########################################################################

########################################################################
# IMPORT Custom widgets
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
########################################################################
import requests # For fetching data from API
from PySide6.QtCore import QTimer # For periodic fetching
# IMPORT FUNCTIONS
from src.functions import *
from src.showPage import ShowPageMixin
from src.packetSniffer import LivePacketUpdater 

# Import the Flask app instance from dashboard_api.py
# Ensure dashboard_api.py is in the PYTHONPATH or same directory
from dashboard_api import app as flask_api_app

########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.server_url = "http://localhost:5001/api/get_packets" # API URL

        # Start Flask API in a separate thread
        self.start_flask_api()

        # Use this to specify your json file(s) path/name
        loadJsonStyle(self, self.ui, jsonFiles = {
            "json-styles/style.json"
            }) 

        ########################################################################

        #######################################################################
        # SHOW WINDOW
        #######################################################################
        self.show() 

        ########################################################################
        # self = QMainWindow class
        QAppSettings.updateAppSettings(self)

        ########################################################################
        # Application Functions
        #########################################################################
        self.app_functions = GuiFunctions(self)

        #Sidebar functions
        self.showPage = ShowPageMixin(self)

        # Chart and table managers are now instantiated within LivePacketUpdater.
        # MainWindow only needs to provide the container widgets from the UI.

        self.packet_updater = LivePacketUpdater(
            all_packets_table_widget=self.ui.packets,
            anomalous_packets_table_widget=self.ui.table,
            graph_widget=self.ui.graph
        )

        # Setup QTimer for MainWindow to fetch data periodically
        self.data_fetch_timer = QTimer(self)
        self.data_fetch_timer.timeout.connect(self.fetch_data_from_api)
        self.data_fetch_timer.start(1000) # Fetch every 1000 ms (1 second)

    def fetch_data_from_api(self):
        """Fetches data from the Flask API and passes it to LivePacketUpdater."""
        try:
            response = requests.get(self.server_url, timeout=0.5)
            response.raise_for_status()  # Raise an exception for HTTP errors
            new_packets_data = response.json()
            
            self.packet_updater.process_incoming_data(new_packets_data)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching packets in MainWindow: {e}")
        except Exception as e:
            print(f"An unexpected error occurred in MainWindow while fetching data: {e}")

    def start_flask_api(self):
        """Starts the Flask API in a daemon thread."""
        def run_api():
            # Running Flask with debug=False and use_reloader=False is recommended in threads
            # to prevent issues with the reloader and multiple initializations.
            flask_api_app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)

        # daemon=True ensures the thread will exit when the main application exits
        thread = threading.Thread(target=run_api, daemon=True)
        thread.start()
        print("Flask API thread started on port 5001.")

########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ########################################################################
    ## 
    ########################################################################
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
########################################################################
## END===>
########################################################################
