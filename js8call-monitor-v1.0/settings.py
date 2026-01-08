#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Settings Dialog for JS8Call Monitor
Configuration editor module
"""

import sys
import configparser
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QGroupBox, QPushButton, QTabWidget, QLineEdit,
                             QCheckBox, QSpinBox, QFileDialog, QMessageBox,
                             QFormLayout, QScrollArea, QWidget)
from PyQt5.QtCore import Qt
from distutils.util import strtobool

class SettingsDialog(QDialog):
    """Configuration editor dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = configparser.ConfigParser()
        self.config.read('config')
        self.setWindowTitle("Settings - JS8Call Monitor")
        self.setMinimumSize(700, 600)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the settings UI"""
        layout = QVBoxLayout()
        
        # Create tab widget
        tabs = QTabWidget()
        
        # Add tabs
        tabs.addTab(self.create_station_tab(), "Station Info")
        tabs.addTab(self.create_source_tab(), "Source Connection")
        tabs.addTab(self.create_clients_tab(), "Client Connections")
        tabs.addTab(self.create_databases_tab(), "Databases")
        tabs.addTab(self.create_logging_tab(), "Logging")
        tabs.addTab(self.create_grids_tab(), "Grid Settings")
        tabs.addTab(self.create_advanced_tab(), "Advanced")
        
        layout.addWidget(tabs)
        
        # Button row
        button_layout = QHBoxLayout()
        
        restore_btn = QPushButton("Restore Defaults")
        restore_btn.clicked.connect(self.restore_defaults)
        button_layout.addWidget(restore_btn)
        
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save && Apply")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0066cc;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0077dd;
            }
        """)
        save_btn.clicked.connect(self.save_config)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def create_station_tab(self):
        """Create station information tab"""
        widget = QScrollArea()
        widget.setWidgetResizable(True)
        scroll_widget = QWidget()
        layout = QFormLayout()
        
        # Operator callsign
        self.operator_edit = QLineEdit(self.config.get('STATION', 'operator', fallback=''))
        self.operator_edit.setToolTip("Your callsign")
        layout.addRow("Operator Callsign:", self.operator_edit)
        
        # Station class
        self.class_edit = QLineEdit(self.config.get('STATION', 'class', fallback=''))
        self.class_edit.setToolTip("Station class (e.g., 2A)")
        layout.addRow("Class:", self.class_edit)
        
        # My gridsquare
        self.my_grid_edit = QLineEdit(self.config.get('STATION', 'my_gridsquare', fallback=''))
        self.my_grid_edit.setToolTip("Your Maidenhead grid square (e.g., FN31pr)")
        layout.addRow("My Gridsquare:", self.my_grid_edit)
        
        # My name
        self.my_name_edit = QLineEdit(self.config.get('STATION', 'my_name', fallback=''))
        self.my_name_edit.setToolTip("Your name")
        layout.addRow("My Name:", self.my_name_edit)
        
        # My county
        self.my_county_edit = QLineEdit(self.config.get('STATION', 'my_county', fallback=''))
        self.my_county_edit.setToolTip("Your county (for county hunters)")
        layout.addRow("My County:", self.my_county_edit)
        
        layout.addRow(QLabel(""))  # Spacer
        info_label = QLabel("<i>These settings identify your station in logs and QSOs</i>")
        layout.addRow(info_label)
        
        scroll_widget.setLayout(layout)
        widget.setWidget(scroll_widget)
        return widget
        
    def create_source_tab(self):
        """Create source connection tab"""
        widget = QScrollArea()
        widget.setWidgetResizable(True)
        scroll_widget = QWidget()
        layout = QVBoxLayout()
        
        # TCP Settings Group
        tcp_group = QGroupBox("TCP Connection (JS8Call)")
        tcp_layout = QFormLayout()
        
        self.tcp_enabled = QCheckBox()
        tcp_enabled_val = self.config.get('TCP', 'enabled', fallback='false')
        self.tcp_enabled.setChecked(bool(strtobool(tcp_enabled_val)))
        self.tcp_enabled.setToolTip("Enable TCP connection to JS8Call")
        tcp_layout.addRow("Enabled:", self.tcp_enabled)
        
        self.tcp_host_edit = QLineEdit(self.config.get('TCP', 'host', fallback='127.0.0.1'))
        self.tcp_host_edit.setToolTip("JS8Call TCP host address")
        tcp_layout.addRow("Host:", self.tcp_host_edit)
        
        self.tcp_port_edit = QSpinBox()
        self.tcp_port_edit.setRange(1, 65535)
        self.tcp_port_edit.setValue(int(self.config.get('TCP', 'port', fallback='2171')))
        self.tcp_port_edit.setToolTip("JS8Call TCP port")
        tcp_layout.addRow("Port:", self.tcp_port_edit)
        
        self.tcp_poll_edit = QSpinBox()
        self.tcp_poll_edit.setRange(1, 60)
        self.tcp_poll_edit.setValue(int(self.config.get('TCP', 'poll_status_interval', fallback='5')))
        self.tcp_poll_edit.setToolTip("Seconds between status polls")
        tcp_layout.addRow("Poll Interval (sec):", self.tcp_poll_edit)
        
        tcp_group.setLayout(tcp_layout)
        layout.addWidget(tcp_group)
        
        # UDP Settings Group
        udp_group = QGroupBox("UDP Connection (JS8Call)")
        udp_layout = QFormLayout()
        
        info = QLabel("<i>UDP is used if TCP is disabled</i>")
        udp_layout.addRow(info)
        
        self.udp_host_edit = QLineEdit(self.config.get('JS8Call', 'host', fallback='127.0.0.1'))
        self.udp_host_edit.setToolTip("JS8Call UDP host address")
        udp_layout.addRow("Host:", self.udp_host_edit)
        
        self.udp_port_edit = QSpinBox()
        self.udp_port_edit.setRange(1, 65535)
        self.udp_port_edit.setValue(int(self.config.get('JS8Call', 'port', fallback='2242')))
        self.udp_port_edit.setToolTip("JS8Call UDP port")
        udp_layout.addRow("Port:", self.udp_port_edit)
        
        udp_group.setLayout(udp_layout)
        layout.addWidget(udp_group)
        
        layout.addStretch()
        scroll_widget.setLayout(layout)
        widget.setWidget(scroll_widget)
        return widget
        
    def create_clients_tab(self):
        """Create client connections tab"""
        widget = QScrollArea()
        widget.setWidgetResizable(True)
        scroll_widget = QWidget()
        layout = QVBoxLayout()
        
        # N1MM Group
        n1mm_group = QGroupBox("N1MM+ Logger")
        n1mm_layout = QFormLayout()
        
        self.n1mm_enabled = QCheckBox()
        n1mm_enabled_val = self.config.get('N1MM', 'enabled', fallback='false')
        self.n1mm_enabled.setChecked(bool(strtobool(n1mm_enabled_val)))
        n1mm_layout.addRow("Enabled:", self.n1mm_enabled)
        
        self.n1mm_host_edit = QLineEdit(self.config.get('N1MM', 'host', fallback='127.0.0.1'))
        n1mm_layout.addRow("Host:", self.n1mm_host_edit)
        
        self.n1mm_port_edit = QSpinBox()
        self.n1mm_port_edit.setRange(1, 65535)
        self.n1mm_port_edit.setValue(int(self.config.get('N1MM', 'port', fallback='12060')))
        n1mm_layout.addRow("Port:", self.n1mm_port_edit)
        
        n1mm_group.setLayout(n1mm_layout)
        layout.addWidget(n1mm_group)
        
        # GridTracker Group
        gt_group = QGroupBox("GridTracker")
        gt_layout = QFormLayout()
        
        self.gt_enabled = QCheckBox()
        gt_enabled_val = self.config.get('GRIDTRACKER', 'enabled', fallback='false')
        self.gt_enabled.setChecked(bool(strtobool(gt_enabled_val)))
        gt_layout.addRow("Enabled:", self.gt_enabled)
        
        self.gt_host_edit = QLineEdit(self.config.get('GRIDTRACKER', 'host', fallback='127.0.0.1'))
        gt_layout.addRow("Host:", self.gt_host_edit)
        
        self.gt_port_edit = QSpinBox()
        self.gt_port_edit.setRange(1, 65535)
        self.gt_port_edit.setValue(int(self.config.get('GRIDTRACKER', 'port', fallback='2237')))
        gt_layout.addRow("Port:", self.gt_port_edit)
        
        gt_group.setLayout(gt_layout)
        layout.addWidget(gt_group)
        
        # GeoServer Group
        gs_group = QGroupBox("GeoServer")
        gs_layout = QFormLayout()
        
        self.gs_msg_enabled = QCheckBox()
        gs_msg_val = self.config.get('GEOSERVER', 'enabled_msg', fallback='false')
        self.gs_msg_enabled.setChecked(bool(strtobool(gs_msg_val)))
        gs_layout.addRow("Enable Messages:", self.gs_msg_enabled)
        
        self.gs_spot_enabled = QCheckBox()
        gs_spot_val = self.config.get('GEOSERVER', 'enabled_spot', fallback='false')
        self.gs_spot_enabled.setChecked(bool(strtobool(gs_spot_val)))
        gs_layout.addRow("Enable Spots:", self.gs_spot_enabled)
        
        self.gs_host_edit = QLineEdit(self.config.get('GEOSERVER', 'host', fallback='127.0.0.1'))
        gs_layout.addRow("Host:", self.gs_host_edit)
        
        self.gs_port_edit = QSpinBox()
        self.gs_port_edit.setRange(1, 65535)
        self.gs_port_edit.setValue(int(self.config.get('GEOSERVER', 'port', fallback='8080')))
        gs_layout.addRow("Port:", self.gs_port_edit)
        
        self.gs_token_edit = QLineEdit(self.config.get('GEOSERVER', 'token', fallback=''))
        self.gs_token_edit.setEchoMode(QLineEdit.Password)
        gs_layout.addRow("Auth Token:", self.gs_token_edit)
        
        gs_group.setLayout(gs_layout)
        layout.addWidget(gs_group)
        
        # YAAC Group
        yaac_group = QGroupBox("YAAC APRS")
        yaac_layout = QFormLayout()
        
        self.yaac_enabled = QCheckBox()
        yaac_enabled_val = self.config.get('YAAC', 'enabled', fallback='false')
        self.yaac_enabled.setChecked(bool(strtobool(yaac_enabled_val)))
        yaac_layout.addRow("Enabled:", self.yaac_enabled)
        
        yaac_file_layout = QHBoxLayout()
        self.yaac_logfile_edit = QLineEdit(self.config.get('YAAC', 'logfile', fallback='yaac.log'))
        yaac_file_layout.addWidget(self.yaac_logfile_edit)
        yaac_browse = QPushButton("Browse...")
        yaac_browse.clicked.connect(lambda: self.browse_file(self.yaac_logfile_edit))
        yaac_file_layout.addWidget(yaac_browse)
        yaac_layout.addRow("Log File:", yaac_file_layout)
        
        yaac_group.setLayout(yaac_layout)
        layout.addWidget(yaac_group)
        
        # ADIF Group
        adif_group = QGroupBox("ADIF Logger")
        adif_layout = QFormLayout()
        
        self.adif_enabled = QCheckBox()
        adif_enabled_val = self.config.get('ADIF', 'enabled', fallback='false')
        self.adif_enabled.setChecked(bool(strtobool(adif_enabled_val)))
        adif_layout.addRow("Enabled:", self.adif_enabled)
        
        adif_file_layout = QHBoxLayout()
        self.adif_logfile_edit = QLineEdit(self.config.get('ADIF', 'logfile', fallback='adif.log'))
        adif_file_layout.addWidget(self.adif_logfile_edit)
        adif_browse = QPushButton("Browse...")
        adif_browse.clicked.connect(lambda: self.browse_file(self.adif_logfile_edit))
        adif_file_layout.addWidget(adif_browse)
        adif_layout.addRow("Log File:", adif_file_layout)
        
        adif_group.setLayout(adif_layout)
        layout.addWidget(adif_group)
        
        layout.addStretch()
        scroll_widget.setLayout(layout)
        widget.setWidget(scroll_widget)
        return widget
        
    def create_databases_tab(self):
        """Create databases tab"""
        widget = QScrollArea()
        widget.setWidgetResizable(True)
        scroll_widget = QWidget()
        layout = QVBoxLayout()
        
        # Database location
        loc_layout = QHBoxLayout()
        loc_label = QLabel("Database Location:")
        loc_layout.addWidget(loc_label)
        self.db_location_edit = QLineEdit(self.config.get('DATABASES', 'location', fallback='./'))
        loc_layout.addWidget(self.db_location_edit)
        db_browse = QPushButton("Browse...")
        db_browse.clicked.connect(lambda: self.browse_directory(self.db_location_edit))
        loc_layout.addWidget(db_browse)
        layout.addLayout(loc_layout)
        
        # Database options
        db_group = QGroupBox("Offline Databases")
        db_layout = QFormLayout()
        
        self.fcc_enabled = QCheckBox()
        fcc_val = self.config.get('DATABASES', 'FccData', fallback='false')
        self.fcc_enabled.setChecked(bool(strtobool(fcc_val)))
        self.fcc_enabled.setToolTip("Enable FCC database lookups")
        db_layout.addRow("FCC Database:", self.fcc_enabled)
        
        self.hamcallcd_enabled = QCheckBox()
        hccd_val = self.config.get('DATABASES', 'HamCallCD', fallback='false')
        self.hamcallcd_enabled.setChecked(bool(strtobool(hccd_val)))
        self.hamcallcd_enabled.setToolTip("Enable HamCall CD database")
        db_layout.addRow("HamCall CD:", self.hamcallcd_enabled)
        
        self.raccd_enabled = QCheckBox()
        rac_val = self.config.get('DATABASES', 'RacCD', fallback='false')
        self.raccd_enabled.setChecked(bool(strtobool(rac_val)))
        self.raccd_enabled.setToolTip("Enable RAC CD database")
        db_layout.addRow("RAC CD:", self.raccd_enabled)
        
        self.local_enabled = QCheckBox()
        local_val = self.config.get('DATABASES', 'LocalDB', fallback='false')
        self.local_enabled.setChecked(bool(strtobool(local_val)))
        self.local_enabled.setToolTip("Enable local database lookups")
        db_layout.addRow("Local Database:", self.local_enabled)
        
        self.local_learn = QCheckBox()
        learn_val = self.config.get('DATABASES', 'LocalDB_learn', fallback='false')
        self.local_learn.setChecked(bool(strtobool(learn_val)))
        self.local_learn.setToolTip("Save new lookups to local database")
        db_layout.addRow("Local Learning:", self.local_learn)
        
        self.collect_rejects = QCheckBox()
        reject_val = self.config.get('DATABASES', 'Collect_Rejects', fallback='false')
        self.collect_rejects.setChecked(bool(strtobool(reject_val)))
        self.collect_rejects.setToolTip("Collect failed lookups")
        db_layout.addRow("Collect Rejects:", self.collect_rejects)
        
        db_group.setLayout(db_layout)
        layout.addWidget(db_group)
        
        # Online databases
        online_group = QGroupBox("Online Databases")
        online_layout = QFormLayout()
        
        self.callook_enabled = QCheckBox()
        callook_val = self.config.get('DATABASES', 'Callook', fallback='false')
        self.callook_enabled.setChecked(bool(strtobool(callook_val)))
        self.callook_enabled.setToolTip("Enable Callook.info lookups")
        online_layout.addRow("Callook.info:", self.callook_enabled)
        
        self.hamcallol_enabled = QCheckBox()
        hcol_val = self.config.get('DATABASES', 'HamCallOnline', fallback='false')
        self.hamcallol_enabled.setChecked(bool(strtobool(hcol_val)))
        self.hamcallol_enabled.setToolTip("Enable HamCall.net lookups")
        online_layout.addRow("HamCall.net:", self.hamcallol_enabled)
        
        self.hc_username_edit = QLineEdit(self.config.get('DATABASES', 'HCusername', fallback=''))
        self.hc_username_edit.setToolTip("HamCall.net username")
        online_layout.addRow("HC Username:", self.hc_username_edit)
        
        self.hc_password_edit = QLineEdit(self.config.get('DATABASES', 'HCpassword', fallback=''))
        self.hc_password_edit.setEchoMode(QLineEdit.Password)
        self.hc_password_edit.setToolTip("HamCall.net password")
        online_layout.addRow("HC Password:", self.hc_password_edit)
        
        online_group.setLayout(online_layout)
        layout.addWidget(online_group)
        
        layout.addStretch()
        scroll_widget.setLayout(layout)
        widget.setWidget(scroll_widget)
        return widget
        
    def create_logging_tab(self):
        """Create logging tab"""
        widget = QScrollArea()
        widget.setWidgetResizable(True)
        scroll_widget = QWidget()
        layout = QVBoxLayout()
        
        # Debug logging
        debug_group = QGroupBox("Debug Logging")
        debug_layout = QFormLayout()
        
        self.console_level = QSpinBox()
        self.console_level.setRange(0, 10)
        self.console_level.setValue(int(self.config.get('DEBUG', 'consolelevel', fallback='0')))
        self.console_level.setToolTip("Console log level (0=off, 10=max)")
        debug_layout.addRow("Console Level:", self.console_level)
        
        self.logfile_level = QSpinBox()
        self.logfile_level.setRange(0, 10)
        self.logfile_level.setValue(int(self.config.get('DEBUG', 'logfilelevel', fallback='0')))
        self.logfile_level.setToolTip("File log level (0=off, 10=max)")
        debug_layout.addRow("File Level:", self.logfile_level)
        
        logfile_layout = QHBoxLayout()
        self.logfile_edit = QLineEdit(self.config.get('DEBUG', 'logfile', fallback='js8monitor.log'))
        logfile_layout.addWidget(self.logfile_edit)
        logfile_browse = QPushButton("Browse...")
        logfile_browse.clicked.connect(lambda: self.browse_file(self.logfile_edit))
        logfile_layout.addWidget(logfile_browse)
        debug_layout.addRow("Log File:", logfile_layout)
        
        debug_group.setLayout(debug_layout)
        layout.addWidget(debug_group)
        
        # SMTP Alerts
        smtp_group = QGroupBox("Email Alerts (SMTP)")
        smtp_layout = QFormLayout()
        
        self.smtp_enabled = QCheckBox()
        smtp_val = self.config.get('SMTP', 'enabled', fallback='false')
        self.smtp_enabled.setChecked(bool(strtobool(smtp_val)))
        smtp_layout.addRow("Enabled:", self.smtp_enabled)
        
        self.smtp_host_edit = QLineEdit(self.config.get('SMTP', 'host', fallback=''))
        smtp_layout.addRow("SMTP Host:", self.smtp_host_edit)
        
        self.smtp_port_edit = QSpinBox()
        self.smtp_port_edit.setRange(1, 65535)
        self.smtp_port_edit.setValue(int(self.config.get('SMTP', 'port', fallback='587')))
        smtp_layout.addRow("SMTP Port:", self.smtp_port_edit)
        
        self.smtp_user_edit = QLineEdit(self.config.get('SMTP', 'user', fallback=''))
        smtp_layout.addRow("Username:", self.smtp_user_edit)
        
        self.smtp_pass_edit = QLineEdit(self.config.get('SMTP', 'pass', fallback=''))
        self.smtp_pass_edit.setEchoMode(QLineEdit.Password)
        smtp_layout.addRow("Password:", self.smtp_pass_edit)
        
        self.mail_from_edit = QLineEdit(self.config.get('SMTP', 'mailfrom', fallback=''))
        smtp_layout.addRow("From Address:", self.mail_from_edit)
        
        self.mail_to_edit = QLineEdit(self.config.get('SMTP', 'mailto', fallback=''))
        smtp_layout.addRow("To Address:", self.mail_to_edit)
        
        smtp_group.setLayout(smtp_layout)
        layout.addWidget(smtp_group)
        
        layout.addStretch()
        scroll_widget.setLayout(layout)
        widget.setWidget(scroll_widget)
        return widget
        
    def create_grids_tab(self):
        """Create grid settings tab"""
        widget = QScrollArea()
        widget.setWidgetResizable(True)
        scroll_widget = QWidget()
        layout = QFormLayout()
        
        self.grid_length = QSpinBox()
        self.grid_length.setRange(1, 11)
        self.grid_length.setValue(int(self.config.get('GRIDS', 'gridlength', fallback='6')))
        self.grid_length.setToolTip("Gridsquare precision (4, 6, 8, or 10)")
        layout.addRow("Grid Length:", self.grid_length)
        
        self.grid_frominfo = QCheckBox()
        frominfo_val = self.config.get('GRIDS', 'frominfo', fallback='false')
        self.grid_frominfo.setChecked(bool(strtobool(frominfo_val)))
        self.grid_frominfo.setToolTip("Extract gridsquare from INFO messages")
        layout.addRow("From INFO:", self.grid_frominfo)
        
        self.map_all = QCheckBox()
        mapall_val = self.config.get('GRIDS', 'map_all', fallback='false')
        self.map_all.setChecked(bool(strtobool(mapall_val)))
        self.map_all.setToolTip("Map all stations regardless of callsign")
        layout.addRow("Map All:", self.map_all)
        
        self.map_cq = QCheckBox()
        mapcq_val = self.config.get('GRIDS', 'map_cq', fallback='true')
        self.map_cq.setChecked(bool(strtobool(mapcq_val)))
        layout.addRow("Map CQ:", self.map_cq)
        
        self.map_heartbeat = QCheckBox()
        maphb_val = self.config.get('GRIDS', 'map_heartbeat', fallback='true')
        self.map_heartbeat.setChecked(bool(strtobool(maphb_val)))
        layout.addRow("Map Heartbeat:", self.map_heartbeat)
        
        self.map_info = QCheckBox()
        mapinfo_val = self.config.get('GRIDS', 'map_info', fallback='true')
        self.map_info.setChecked(bool(strtobool(mapinfo_val)))
        layout.addRow("Map INFO:", self.map_info)
        
        self.map_status = QCheckBox()
        mapstatus_val = self.config.get('GRIDS', 'map_status', fallback='true')
        self.map_status.setChecked(bool(strtobool(mapstatus_val)))
        layout.addRow("Map STATUS:", self.map_status)
        
        self.map_log = QCheckBox()
        maplog_val = self.config.get('GRIDS', 'map_log', fallback='true')
        self.map_log.setChecked(bool(strtobool(maplog_val)))
        layout.addRow("Map LOG:", self.map_log)
        
        self.map_qso = QCheckBox()
        mapqso_val = self.config.get('GRIDS', 'map_qso', fallback='true')
        self.map_qso.setChecked(bool(strtobool(mapqso_val)))
        layout.addRow("Map QSO:", self.map_qso)
        
        self.map_snr = QCheckBox()
        mapsnr_val = self.config.get('GRIDS', 'map_snr', fallback='true')
        self.map_snr.setChecked(bool(strtobool(mapsnr_val)))
        layout.addRow("Map SNR:", self.map_snr)
        
        self.auto_close = QCheckBox()
        autoclose_val = self.config.get('GRIDS', 'auto_close', fallback='false')
        self.auto_close.setChecked(bool(strtobool(autoclose_val)))
        self.auto_close.setToolTip("Exit monitor when JS8Call closes")
        layout.addRow("Auto Close:", self.auto_close)
        
        layout.addRow(QLabel(""))
        info = QLabel("<i>These settings control which message types are logged and mapped</i>")
        layout.addRow(info)
        
        scroll_widget.setLayout(layout)
        widget.setWidget(scroll_widget)
        return widget
        
    def create_advanced_tab(self):
        """Create advanced settings tab"""
        widget = QScrollArea()
        widget.setWidgetResizable(True)
        scroll_widget = QWidget()
        layout = QVBoxLayout()
        
        # Authentication
        auth_group = QGroupBox("API Authentication")
        auth_layout = QFormLayout()
        
        self.auth_enabled = QCheckBox()
        auth_val = self.config.get('AUTH', 'enabled', fallback='false')
        self.auth_enabled.setChecked(bool(strtobool(auth_val)))
        self.auth_enabled.setToolTip("Require authentication for API commands")
        auth_layout.addRow("Enabled:", self.auth_enabled)
        
        self.auth_token_edit = QLineEdit(self.config.get('AUTH', 'token', fallback=''))
        self.auth_token_edit.setEchoMode(QLineEdit.Password)
        self.auth_token_edit.setToolTip("Authentication token for API commands")
        auth_layout.addRow("Auth Token:", self.auth_token_edit)
        
        auth_group.setLayout(auth_layout)
        layout.addWidget(auth_group)
        
        layout.addStretch()
        
        info = QLabel("<i>Advanced settings for API security</i>")
        layout.addWidget(info)
        
        scroll_widget.setLayout(layout)
        widget.setWidget(scroll_widget)
        return widget
        
    def browse_file(self, line_edit):
        """Browse for a file"""
        filename, _ = QFileDialog.getSaveFileName(self, "Select File", line_edit.text())
        if filename:
            line_edit.setText(filename)
            
    def browse_directory(self, line_edit):
        """Browse for a directory"""
        dirname = QFileDialog.getExistingDirectory(self, "Select Directory", line_edit.text())
        if dirname:
            line_edit.setText(dirname)
            
    def restore_defaults(self):
        """Restore default settings"""
        reply = QMessageBox.question(self, "Restore Defaults",
                                     "Are you sure you want to restore default settings?\n"
                                     "This will require restarting the application.",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, "Restore Defaults",
                                   "Please manually restore your config file backup.\n"
                                   "A restart will be required.")
            
    def save_config(self):
        """Save configuration to file"""
        try:
            # Update config object with form values
            
            # Station
            self.config.set('STATION', 'operator', self.operator_edit.text())
            self.config.set('STATION', 'class', self.class_edit.text())
            self.config.set('STATION', 'my_gridsquare', self.my_grid_edit.text())
            self.config.set('STATION', 'my_name', self.my_name_edit.text())
            self.config.set('STATION', 'my_county', self.my_county_edit.text())
            
            # TCP
            self.config.set('TCP', 'enabled', str(self.tcp_enabled.isChecked()).lower())
            self.config.set('TCP', 'host', self.tcp_host_edit.text())
            self.config.set('TCP', 'port', str(self.tcp_port_edit.value()))
            self.config.set('TCP', 'poll_status_interval', str(self.tcp_poll_edit.value()))
            
            # UDP (JS8Call)
            self.config.set('JS8Call', 'host', self.udp_host_edit.text())
            self.config.set('JS8Call', 'port', str(self.udp_port_edit.value()))
            
            # N1MM
            self.config.set('N1MM', 'enabled', str(self.n1mm_enabled.isChecked()).lower())
            self.config.set('N1MM', 'host', self.n1mm_host_edit.text())
            self.config.set('N1MM', 'port', str(self.n1mm_port_edit.value()))
            
            # GridTracker
            self.config.set('GRIDTRACKER', 'enabled', str(self.gt_enabled.isChecked()).lower())
            self.config.set('GRIDTRACKER', 'host', self.gt_host_edit.text())
            self.config.set('GRIDTRACKER', 'port', str(self.gt_port_edit.value()))
            
            # GeoServer
            self.config.set('GEOSERVER', 'enabled_msg', str(self.gs_msg_enabled.isChecked()).lower())
            self.config.set('GEOSERVER', 'enabled_spot', str(self.gs_spot_enabled.isChecked()).lower())
            self.config.set('GEOSERVER', 'host', self.gs_host_edit.text())
            self.config.set('GEOSERVER', 'port', str(self.gs_port_edit.value()))
            self.config.set('GEOSERVER', 'token', self.gs_token_edit.text())
            
            # YAAC
            self.config.set('YAAC', 'enabled', str(self.yaac_enabled.isChecked()).lower())
            self.config.set('YAAC', 'logfile', self.yaac_logfile_edit.text())
            
            # ADIF
            self.config.set('ADIF', 'enabled', str(self.adif_enabled.isChecked()).lower())
            self.config.set('ADIF', 'logfile', self.adif_logfile_edit.text())
            
            # Databases
            self.config.set('DATABASES', 'location', self.db_location_edit.text())
            self.config.set('DATABASES', 'FccData', str(self.fcc_enabled.isChecked()).lower())
            self.config.set('DATABASES', 'HamCallCD', str(self.hamcallcd_enabled.isChecked()).lower())
            self.config.set('DATABASES', 'RacCD', str(self.raccd_enabled.isChecked()).lower())
            self.config.set('DATABASES', 'LocalDB', str(self.local_enabled.isChecked()).lower())
            self.config.set('DATABASES', 'LocalDB_learn', str(self.local_learn.isChecked()).lower())
            self.config.set('DATABASES', 'Collect_Rejects', str(self.collect_rejects.isChecked()).lower())
            self.config.set('DATABASES', 'Callook', str(self.callook_enabled.isChecked()).lower())
            self.config.set('DATABASES', 'HamCallOnline', str(self.hamcallol_enabled.isChecked()).lower())
            self.config.set('DATABASES', 'HCusername', self.hc_username_edit.text())
            self.config.set('DATABASES', 'HCpassword', self.hc_password_edit.text())
            
            # Logging
            self.config.set('DEBUG', 'consolelevel', str(self.console_level.value()))
            self.config.set('DEBUG', 'logfilelevel', str(self.logfile_level.value()))
            self.config.set('DEBUG', 'logfile', self.logfile_edit.text())
            
            # SMTP
            self.config.set('SMTP', 'enabled', str(self.smtp_enabled.isChecked()).lower())
            self.config.set('SMTP', 'host', self.smtp_host_edit.text())
            self.config.set('SMTP', 'port', str(self.smtp_port_edit.value()))
            self.config.set('SMTP', 'user', self.smtp_user_edit.text())
            self.config.set('SMTP', 'pass', self.smtp_pass_edit.text())
            self.config.set('SMTP', 'mailfrom', self.mail_from_edit.text())
            self.config.set('SMTP', 'mailto', self.mail_to_edit.text())
            
            # Grids
            self.config.set('GRIDS', 'gridlength', str(self.grid_length.value()))
            self.config.set('GRIDS', 'frominfo', str(self.grid_frominfo.isChecked()).lower())
            self.config.set('GRIDS', 'map_all', str(self.map_all.isChecked()).lower())
            self.config.set('GRIDS', 'map_cq', str(self.map_cq.isChecked()).lower())
            self.config.set('GRIDS', 'map_heartbeat', str(self.map_heartbeat.isChecked()).lower())
            self.config.set('GRIDS', 'map_info', str(self.map_info.isChecked()).lower())
            self.config.set('GRIDS', 'map_status', str(self.map_status.isChecked()).lower())
            self.config.set('GRIDS', 'map_log', str(self.map_log.isChecked()).lower())
            self.config.set('GRIDS', 'map_qso', str(self.map_qso.isChecked()).lower())
            self.config.set('GRIDS', 'map_snr', str(self.map_snr.isChecked()).lower())
            self.config.set('GRIDS', 'auto_close', str(self.auto_close.isChecked()).lower())
            
            # Auth
            self.config.set('AUTH', 'enabled', str(self.auth_enabled.isChecked()).lower())
            self.config.set('AUTH', 'token', self.auth_token_edit.text())
            
            # Write to file
            with open('config', 'w') as configfile:
                self.config.write(configfile)
            
            QMessageBox.information(self, "Settings Saved",
                                   "Configuration saved successfully!\n\n"
                                   "Please restart the application for changes to take effect.")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error Saving Settings",
                               f"Failed to save configuration:\n{str(e)}")