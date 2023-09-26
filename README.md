# LCBOX

Welcome to the LBOX!

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuring Shodan API Key](#configuring-shodan-api-key)
- [Usage](#usage)
  - [Network Scanner](#network-scanner)
  - [ADB Exploiter](#adb-exploiter)
  - [Additional Commands](#additional-commands)
- [Contributing](#contributing)

## Getting Started

### Prerequisites

Before using this tool, ensure you have the following prerequisites:

- Python 3.x installed on your system.
- [MariaDB](https://mariadb.org/download/) installed and running as your database server.

### Installation

1. Clone this repository to your local machine:

   ```
   git clone https://github.com/yourusername/network-scanner-adb-exploiter.git
   ```

2. Install the required Python packages by running:

   ```
   pip install -r requirements.txt
   ```

### Configuring Shodan API Key

To utilize the Shodan functionality, you'll need to configure your Shodan API key:

1. Sign up at [Shodan](https://www.shodan.io/) to obtain your API key.

2. Open the `server.py` file and locate the `API_KEY` variable. Replace the empty string with your Shodan API key:

   ```
   API_KEY = "your_shodan_api_key_here"
   ```

## Usage

### Network Scanner

To scan your local network and gather information about active devices:

```
python server.py
```

Use the following commands in the interactive shell:

- `scan port [IP] [start_port] [end_port]`: Scan a specific IP address for open ports within a given range.

- `status`: Check the status of the autoscan feature and the number of devices found.

- `devices`: Display information about devices found on the network.

- `disable autoscan`: Disable autoscan.

- `enable autoscan`: Enable autoscan.

- `pingthemall`: Manually trigger a network scan.

### ADB Exploiter

To exploit ADB connections on Android devices:

```
adb-scan
```

This command will continuously search for ADB-enabled devices on the internet using Shodan. If a device is found, it will attempt to connect to it using the `adb shell` command. If successful, the IP address of the device will be saved to the database.

You can check the list of exploited devices with:

```
adb-devices
```

### Additional Commands

- `clear`: Clear the terminal screen.

- `connect`: Reconnect to the database if the connection is lost.

- `exit`: Exit the program.

- `hello`: Print a friendly greeting.

- `help`: Display a list of available commands and their descriptions.

## Contributing

If you have suggestions or improvements for this script, feel free to open an issue or create a pull request.
