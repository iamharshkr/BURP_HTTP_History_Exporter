# HTTP History Exporter - Burp Suite Extension

## Overview

The **HTTP History Exporter** is a Burp Suite extension designed to help users export HTTP request and response data from Burp Suite's proxy history. The extension allows you to select specific domains, filter the HTTP traffic, and export the data in a structured CSV format. This is especially useful for auditing, analyzing API requests, or exporting traffic for later analysis.

## Features

- **Domain Filtering**: Select specific domains to export based on the captured requests.
- **Customizable Export Options**: Choose what to export:
  - **Parameters**: Export parameter keys from both query strings and request bodies.
  - **Full HTTP Requests**: Export complete raw HTTP requests.
  - **Full HTTP Responses**: Export complete raw HTTP responses.
- **CSV Export**: Export HTTP history into a well-structured CSV file with dynamic columns based on selected export options.
- **Duplicate Removal**: Ensure that only unique URLs are included in the exported file.
- **Customizable UI**: User-friendly graphical interface for interacting with Burp Suite.

## Prerequisites

To use this extension, you need the following:
- **Burp Suite** (Pro or Community Edition)
- Python 2.7.x or 3.x (depends on your environment)
- The Burp Suite Python API available (ensure your environment has the necessary modules)

## Installation

1. **Download the Extension**:
   - Download the `.py` file of the extension or clone the GitHub repository if available.

2. **Install in Burp Suite**:
   - Open Burp Suite.
   - Go to the "Extender" tab.
   - In the "Extensions" sub-tab, click on "Add".
   - Select the `.py` file of the extension and add it to Burp Suite.

3. **Python Dependencies**:
   - Ensure Python and the necessary libraries are installed as required by Burp Suite extensions.

## How to Use

1. **Starting the Extension**:
   - Once the extension is installed, a new tab titled **"HTTP Exporter"** will appear in Burp Suite under the "Extender" tab.
   - Click on the **"HTTP Exporter"** tab to access the extension.

2. **Select Domains**:
   - Click the **"Refresh Domains"** button to load all available domains from the Burp Suite site map.
   - Select the domains whose HTTP history you wish to export by checking the corresponding checkboxes.

3. **Configure Export Options**:
   - Select which components you want to export:
     - **Export Parameters** (checked by default): Exports parameter keys from query strings and request bodies.
     - **Export Requests**: Exports the complete raw HTTP requests.
     - **Export Responses**: Exports the complete raw HTTP responses.

4. **Export HTTP History**:
   - After selecting the desired domains and export options, click the **"Export"** button to start the export process.
   - A file dialog will appear allowing you to save the exported data in CSV format.

5. **CSV Output Format**:
   The exported CSV file will contain the following columns (based on your selected export options):
   - **S.No.**: A serial number for each request.
   - **API**: The request method (e.g., GET, POST) and the requested URL.
   - **Parameters**: (Optional) Query and body parameters of the request (one per line).
   - **Request**: (Optional) The complete raw HTTP request.
   - **Response**: (Optional) The complete raw HTTP response.

## Configuration Options

### Domains
- **Refresh Domains**: Fetches the list of domains from the Burp Suite site map to filter by.
- **Select Domains**: Choose the domains you want to export traffic for. Multiple domains can be selected.

### Export Options
- **Export Parameters**: Include parameter keys from both query strings and request bodies in the output.
- **Export Requests**: Include the complete raw HTTP requests in the output.
- **Export Responses**: Include the complete raw HTTP responses in the output.

### Exporting
- **Export to CSV**: Allows the user to save the HTTP history as a CSV file with the selected columns.

## Troubleshooting

- **No HTTP History Found**: If no HTTP traffic is found in the Burp Suite proxy history, ensure that the proxy is actively intercepting requests.
- **No Domains Selected**: Ensure you have selected at least one domain before attempting the export.
- **No Export Options Selected**: Ensure you have selected at least one export option (Parameters, Request, or Response).
- **Error Parsing URL**: If an error occurs while parsing a URL, it might be due to malformed URLs in the history. Check the traffic logs for any irregularities.

## Code Overview

- **BurpExtender**: This class implements the main functionality for the Burp Suite extension, including registering the extension, handling UI components, and exporting HTTP history.
- **UI Components**: The extension provides a graphical interface with checkboxes to select domains and export options, along with buttons to refresh domains or export the HTTP history.
- **Export Process**: The HTTP history is filtered based on selected domains, and duplicate URLs are removed before exporting the data into a CSV file with dynamically selected columns.

## License

This extension is open-source and is provided under the MIT License. You are free to use, modify, and distribute it as per the terms of the license.

## Contact

For any issues or contributions, feel free to open an issue on the GitHub repository or contact the developer at harshkumar9430@gmail.com.
