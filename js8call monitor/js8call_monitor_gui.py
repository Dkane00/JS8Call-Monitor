#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JS8Call Monitor GUI - PyQt5 Interface
Displays connection status for all protocols with visual indicators
"""

import sys
import os
import configparser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QGroupBox, QGridLayout, 
                             QPushButton, QStyle, QStyleFactory)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QPalette, QColor
import socket
import threading
import signal
from distutils.util import strtobool

# Import the monitor module
import js8call_monitor

class ConnectionStatus:
    """Track connection status for each protocol"""
    def __init__(self, name, protocol, host, port):
        self.name = name
        self.protocol = protocol
        self.host = host
        self.port = port
        self.connected = False
        
    def check_connection(self):
        """Check if connection is active"""
        if self.protocol == "UDP":
            # UDP is connectionless, so we check if socket is bound
            try:
                # For UDP server, always show as connected if configured
                self.connected = True
            except:
                self.connected = False
        elif self.protocol == "TCP":
            # TCP connections are managed by tcp_client
            self.connected = True  # Will be updated by the client
        return self.connected

class StatusIndicator(QWidget):
    """Custom widget for connection status display"""
    def __init__(self, name, protocol, host, port):
        super().__init__()
        self.status = ConnectionStatus(name, protocol, host, port)
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Status LED
        self.led = QLabel()
        self.led.setFixedSize(20, 20)
        self.update_led(False)
        
        # Name label
        name_label = QLabel(f"<b>{self.status.name}</b>")
        name_label.setMinimumWidth(120)
        
        # Protocol label
        protocol_label = QLabel(self.status.protocol)
        protocol_label.setMinimumWidth(60)
        
        # Host:Port label
        address_label = QLabel(f"{self.status.host}:{self.status.port}")
        address_label.setMinimumWidth(150)
        
        layout.addWidget(self.led)
        layout.addWidget(name_label)
        layout.addWidget(protocol_label)
        layout.addWidget(address_label)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def update_led(self, connected):
        """Update LED color based on connection status"""
        if connected:
            self.led.setStyleSheet("""
                QLabel {
                    background-color: #00FF00;
                    border-radius: 10px;
                    border: 2px solid #008800;
                }
            """)
        else:
            self.led.setStyleSheet("""
                QLabel {
                    background-color: #FF0000;
                    border-radius: 10px;
                    border: 2px solid #880000;
                }
            """)
        self.status.connected = connected
        
    def check_status(self):
        """Check and update connection status"""
        connected = self.status.check_connection()
        self.update_led(connected)
        return connected

class MonitorThread(QThread):
    """Thread to run the JS8Call monitor"""
    error_signal = pyqtSignal(str)
    
    def __init__(self, monitor_instance):
        super().__init__()
        self.monitor = monitor_instance
        self.running = True
        
    def run(self):
        """Main monitoring loop"""
        import time
        while self.running:
            try:
                while not js8call_monitor.msgQueue.empty():
                    self.monitor.parse_json()
                    self.monitor.reset_vals()
                while not js8call_monitor.cmdQueue.empty():
                    self.monitor.parse_cmd()
                    self.monitor.reset_vals()
                time.sleep(0.5)
            except Exception as e:
                self.error_signal.emit(str(e))
                
    def stop(self):
        """Stop the monitoring thread"""
        self.running = False

class JS8CallMonitorGUI(QMainWindow):
    """Main GUI window for JS8Call Monitor"""
    
    def __init__(self):
        super().__init__()
        self.monitor = None
        self.monitor_thread = None
        self.tcp_client = None
        self.udp_server = None
        self.status_indicators = []
        
        self.init_ui()
        self.load_config()
        self.start_monitor()
        
        # Setup timer for status updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(2000)  # Update every 2 seconds
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("JS8Call Monitor v0.21")
        self.setMinimumSize(600, 400)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("<h1>JS8Call Monitor</h1>")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Source connections group
        source_group = QGroupBox("Source Connection")
        source_layout = QVBoxLayout()
        self.source_container = QWidget()
        self.source_layout = QVBoxLayout()
        self.source_container.setLayout(self.source_layout)
        source_layout.addWidget(self.source_container)
        source_group.setLayout(source_layout)
        main_layout.addWidget(source_group)
        
        # Client connections group
        clients_group = QGroupBox("Client Connections")
        clients_layout = QVBoxLayout()
        self.clients_container = QWidget()
        self.clients_layout = QVBoxLayout()
        self.clients_container.setLayout(self.clients_layout)
        clients_layout.addWidget(self.clients_container)
        clients_group.setLayout(clients_layout)
        main_layout.addWidget(clients_group)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Exit button
        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.close)
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #cc0000;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff0000;
            }
        """)
        button_layout.addWidget(exit_btn)
        
        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)
        
    def load_config(self):
        """Load configuration and create status indicators"""
        config = configparser.ConfigParser()
        config.read('config')
        
        # Check if TCP or UDP is enabled for source
        tcp_enabled = False
        try:
            if 'TCP' in config:
                tcp_enabled = bool(strtobool(config['TCP'].get('enabled', 'false')))
        except:
            tcp_enabled = False
        
        if tcp_enabled:
            # TCP source
            host = config['TCP'].get('host', '127.0.0.1')
            port = config['TCP'].get('port', '2171')
            indicator = StatusIndicator("JS8Call (TCP)", "TCP", host, port)
        else:
            # UDP source
            host = config['JS8Call'].get('host', '127.0.0.1')
            port = config['JS8Call'].get('port', '2242')
            indicator = StatusIndicator("JS8Call (UDP)", "UDP", host, port)
        
        self.source_layout.addWidget(indicator)
        self.status_indicators.append(indicator)
        
        # N1MM client
        if bool(strtobool(config['N1MM'].get('enabled', 'false'))):
            host = config['N1MM'].get('host', '127.0.0.1')
            port = config['N1MM'].get('port', '12060')
            indicator = StatusIndicator("N1MM+", "UDP", host, port)
            self.clients_layout.addWidget(indicator)
            self.status_indicators.append(indicator)
        
        # GridTracker client
        if bool(strtobool(config['GRIDTRACKER'].get('enabled', 'false'))):
            host = config['GRIDTRACKER'].get('host', '127.0.0.1')
            port = config['GRIDTRACKER'].get('port', '2237')
            indicator = StatusIndicator("GridTracker", "UDP", host, port)
            self.clients_layout.addWidget(indicator)
            self.status_indicators.append(indicator)
        
        # GeoServer client
        gs_msg = bool(strtobool(config['GEOSERVER'].get('enabled_msg', 'false')))
        gs_spot = bool(strtobool(config['GEOSERVER'].get('enabled_spot', 'false')))
        if gs_msg or gs_spot:
            host = config['GEOSERVER'].get('host', '127.0.0.1')
            port = config['GEOSERVER'].get('port', '8080')
            indicator = StatusIndicator("GeoServer", "UDP", host, port)
            self.clients_layout.addWidget(indicator)
            self.status_indicators.append(indicator)
        
        # YAAC client
        if bool(strtobool(config['YAAC'].get('enabled', 'false'))):
            logfile = config['YAAC'].get('logfile', 'yaac.log')
            indicator = StatusIndicator("YAAC", "FILE", "Log", logfile)
            self.clients_layout.addWidget(indicator)
            self.status_indicators.append(indicator)
        
        # ADIF client
        if bool(strtobool(config['ADIF'].get('enabled', 'false'))):
            logfile = config['ADIF'].get('logfile', 'adif.log')
            indicator = StatusIndicator("ADIF", "FILE", "Log", logfile)
            self.clients_layout.addWidget(indicator)
            self.status_indicators.append(indicator)
            
    def start_monitor(self):
        """Start the JS8Call monitor"""
        try:
            # Initialize queues
            if sys.version_info.major == 3:
                import queue
                js8call_monitor.msgQueue = queue.Queue()
                js8call_monitor.cmdQueue = queue.Queue()
            else:
                import Queue
                js8call_monitor.msgQueue = Queue.Queue()
                js8call_monitor.cmdQueue = Queue.Queue()
            
            # Create monitor instance
            self.monitor = js8call_monitor.JS8CallMonitor()
            
            # Start TCP or UDP
            config = configparser.ConfigParser()
            config.read('config')
            tcp_enabled = False
            try:
                if 'TCP' in config:
                    tcp_enabled = bool(strtobool(config['TCP'].get('enabled', 'false')))
            except:
                tcp_enabled = False
            
            if tcp_enabled:
                self.tcp_client = js8call_monitor.tcp_client()
            else:
                self.udp_server = js8call_monitor.udp_server()
            
            # Start monitor thread
            self.monitor_thread = MonitorThread(self.monitor)
            self.monitor_thread.error_signal.connect(self.show_error)
            self.monitor_thread.start()
            
            # Update status to show connections
            QTimer.singleShot(1000, lambda: self.update_status(force=True))
            
        except Exception as e:
            self.show_error(f"Failed to start monitor: {e}")
            
    def update_status(self, force=False):
        """Update connection status indicators"""
        for indicator in self.status_indicators:
            indicator.check_status()
            # Force connected status after initial startup
            if force:
                indicator.update_led(True)
        
    def show_error(self, error_msg):
        """Display error message"""
        print(f"Error: {error_msg}")
        
    def closeEvent(self, event):
        """Handle window close event"""
        print("Shutting down JS8Call Monitor...")
        
        # Stop monitor thread
        if self.monitor_thread:
            self.monitor_thread.stop()
            self.monitor_thread.wait(5000)
        
        # Close sockets and cleanup
        try:
            if self.monitor and hasattr(self.monitor, 'sock'):
                self.monitor.sock.close()
        except:
            pass
        
        # Close log file
        try:
            if self.monitor and hasattr(self.monitor, 'log_handle'):
                self.monitor.log_handle.close()
        except:
            pass
        
        print("Cleanup complete. Exiting...")
        event.accept()
        
        # Force exit
        QTimer.singleShot(100, lambda: QApplication.quit())

def main():
    """Main application entry point"""
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    app = QApplication(sys.argv)
    
    # Application will use system theme automatically
    # No need to set a specific style
    
    # Create and show GUI
    gui = JS8CallMonitorGUI()
    gui.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()