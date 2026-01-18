# JS8Call Monitor

This program is designed to monitor the JS8Call application for various received messages, examine the messages, then pass on the relevant information to mapping application(s), so the contact can be automatically plotted.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Features](#features)
    - [New TCP Connector](#new-tcp-connector)
    - [GUI vs. CLI Monitor](#gui-vs-cli-monitor)
- [Mapping Applications Supported](#mapping-applications-supported)
- [Credits & Acknowledgments](#credits--acknowledgments)
- [Documentation (PDFs)](#documentation-pdfs)

## Prerequisites
- Python 3.x (Recommended) or Python 2.7
- JS8Call installed and running

## Installation & Setup

1.  **Clone this repository**
    Open your terminal and use `git` to clone the repository to your local machine:
    ```bash
    git clone https://github.com/Dkane00/JS8Call-Monitor.git
    ```

2.  **Install `pywsjtx` Library**
    You must copy the `pywsjtx` folder included in this download to your Python installation's library directory.

    **Windows:**
    Copy the entire `pywsjtx` folder and its contents to the `Lib` directory of your Python installation.
    *Example:* `C:\Program Files\Python39\Lib` or `C:\Users\YourName\AppData\Local\Programs\Python\Python39\Lib`

    **Linux and Raspberry Pi:**
    The exact name of the library directory depends on your Python version (e.g., `/usr/lib/python2.7` or `/usr/lib/python3.8`).

    First, identify your installed Python version(s):
    ```bash
    ls /usr/lib
    ```
    *Look for directories named pythonX.X*

    Then, copy the folder using the following command (substitute `python3.8` with your actual version):
    ```bash
    sudo cp -r pywsjtx /usr/lib/python3.8
    ```
    *If your system has several versions of Python installed, repeat the command for each version.*

3.  **Install Other Dependencies** using pip:
    ```bash
    pip install requests PyQt5
    ```

4.  **Run the Application**:

    Navigate to the project directory:
    ```bash
    cd js8call-monitor-v1.0
    ```

    You can run the monitor in two modes:

    **Option A: GUI Mode (Recommended)**
    ```bash
    python js8call_monitor_gui.py
    ```

    **Option B: Headless/CLI Mode**
    ```bash
    python js8call_monitor.py
    ```

## Features

### New TCP Connector
This version introduces a robust TCP connector for JS8Call. Unlike the previous UDP-only method, the TCP connection ensures a more reliable data stream directly from the JS8Call API.

-   **Default Port:** 2171
-   **Configuration:** You can enable/disable TCP and configure the host/port in the `config` file or via the GUI Settings (Source Connection tab).
-   **Benefit:** Provides a persistent connection state, reducing the chance of missed messages compared to UDP.

### GUI vs. CLI Monitor

**JS8Call Monitor GUI (`js8call_monitor_gui.py`)**
-   **Visual Interface:** Provides a user-friendly window displaying the health of all connections.
-   **Status Indicators:** Features LED-style indicators (Green/Red) for the Source connection (JS8Call) and all Client connections (N1MM, GridTracker, etc.), giving you immediate visual feedback on what is working.
-   **Easy Configuration:** Includes a built-in "Settings" menu to easily configure Station Info, API ports, and toggle features without editing text files manually.
-   **Real-time Feedback:** Shows instant connection status updates (refreshed every 2 seconds).

**Basic Monitor (`js8call_monitor.py`)**
-   **Lightweight:** Runs purely in the terminal without a graphical interface.
-   **Background Service:** Ideal for running on headless servers, Raspberry Pis without a display, or as a background service where visual feedback is not required.
-   **Console Output:** Displays detailed logs and status updates directly to the command line (console level configurable).

## Mapping Applications Supported
- N1MM+ with County Mapper - Available for Windows.
- GridTracker - Available for Windows, Mac, Linux, Raspberry Pi OS
- GeoChron Digital Displays - OS Independent
- Yet Another APRS Client (YAAC) - Available for Windows, Mac, Linux, Raspberry Pi OS
- Any mapping application that can import ADIF files.

## Credits & Acknowledgments
The original `JS8Call Monitor` code was created by **KK7JND**. The software provided in this repository has been modified and upgraded based on his original work.

You can find the original project repository here:  
[https://github.com/KK7JND/JS8Call-Monitor](https://github.com/KK7JND/JS8Call-Monitor)

## Documentation (PDFs)
- [JS8Call Monitor Architecture v3](js8call%20monitor%20architecture%20v3.pdf)
- [JS8Call Monitor LocalDB Readme v0.3](js8call%20monitor%20localdb%20readme%20v0.3.pdf)
- [Original Monitor Readme v0.21](js8call%20monitor%20readme%20v0.21.pdf)
