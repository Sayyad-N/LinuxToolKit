# LinuxToolKit

## Overview

LinuxToolKit is a Python-based utility designed to simplify various Linux-related tasks, such as package management, system updates, and information retrieval. It provides a user-friendly interface to interact with common Linux commands and package managers.

## Features

-   **Package Management**: Install, remove, update, upgrade, and search for packages using the system's default package manager.
-   **System Information**: Display detailed system information, including OS version, architecture, CPU, memory, and disk usage.
-   **Network Connectivity**: Check network connectivity by pinging a specified host.
-   **AI Assistance**: Integrated AI help for troubleshooting package management issues.
-   **Automated Package Manager Detection**: Automatically detects the system's package manager.
-   **Admin Privileges**: Automatically requests admin privileges when required.
-   **Comprehensive Application List**: Includes a detailed list of available Linux applications across various categories.

## Requirements

-   Python 3.x
-   requirements.txt (All libs in it ) 

## Installation

1.  **Clone the repository:**

    ```bash
    git clone [repository_url]
    cd LinuxToolKit
    ```

2.  **Install the required Python libraries:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **API Key Configuration (For AI Assistance):**

    -   Obtain an API key from Google Gemini API.
    -   Set the API key in your environment or directly in the script.

    ```python
    GenAI.configure(api_key="YOUR_API_KEY") Already Added 
    ```

## Usage

1.  **Run the script:**

    ```bash
    python LinuxToolKit.py
    ```

2.  **Follow the on-screen menu to perform various tasks.**

## Code Structure

-   `LinuxToolKit.py`: The main script containing all the functionalities.
-   `pm_commands`: Dictionary mapping package managers to their respective commands.
-   `linux_apps`: Dictionary containing a comprehensive list of Linux applications.

## Functions

-   `detect_package_manager()`: Detects the system's package manager.
-   `is_admin()`: Checks if the script is running with admin privileges.
-   `run_as_admin(cmd)`: Runs a command with admin privileges.
-   `print_linux_apps()`: Prints a list of available Linux applications.
-   `ai_help(error_message)`: Provides AI assistance for troubleshooting.
-   `install_package()`: Installs a specified package.
-   `remove_package()`: Removes a specified package.
-   `update()`: Updates the system.
-   `upgrade()`: Upgrades the system.
-   `search_package()`: Searches for a package.
-   `list_installed_packages()`: Lists all installed packages.
-   `cleanup_system()`: Cleans up unused packages.
-   `display_system_info()`: Displays system information.
-   `check_network_connectivity()`: Checks network connectivity.
-   `ask_continue(message)`: Asks the user if they want to continue.
-   `main_menu()`: The main menu of the script.

## Package Manager Support

The script supports the following package managers:

-   `apt`
-   `dnf`
-   `yum`
-   `zypper`
-   `pacman`
-   `apk`
-   `snap`
-   `flatpak`

## Contributing

Feel free to contribute to the project by submitting pull requests or reporting issues.

## License

This project is licensed under the MIT License.

## Author

SayyadN
```