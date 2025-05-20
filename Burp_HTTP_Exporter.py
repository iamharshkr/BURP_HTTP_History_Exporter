from burp import IBurpExtender, ITab, IHttpListener
from javax.swing import JPanel, JButton, JCheckBox, JScrollPane, BoxLayout, JLabel, BorderFactory, JFileChooser, JOptionPane
from javax.swing import JSeparator, SwingConstants
from java.awt import BorderLayout, Dimension, Font, Color, FlowLayout, GridLayout
import csv
from java.net import URL
from java.io import File
import json

class BurpExtender(IBurpExtender, ITab, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self._callbacks.setExtensionName("HTTP History Exporter")

        # UI Elements
        self.panel = JPanel()
        self.panel.setLayout(BorderLayout())
        self.panel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10))
        
        # Title Panel
        title_panel = JPanel()
        title_panel.setBackground(Color(50, 100, 150))  # Dark blue background
        title_label = JLabel("HTTP History Exporter")
        title_label.setFont(Font("Arial", Font.BOLD, 18))
        title_label.setForeground(Color.WHITE)  # White text
        title_panel.add(title_label)
        self.panel.add(title_panel, BorderLayout.NORTH)
        
        # Main content panel with split layout
        content_panel = JPanel(BorderLayout())
        
        # Domain Selection Panel
        self.domain_panel = JPanel()
        self.domain_panel.setLayout(BoxLayout(self.domain_panel, BoxLayout.Y_AXIS))
        self.domain_scroll = JScrollPane(self.domain_panel)
        self.domain_scroll.setPreferredSize(Dimension(400, 300))
        self.domain_scroll.setBorder(BorderFactory.createTitledBorder("Select Domains"))
        content_panel.add(self.domain_scroll, BorderLayout.CENTER)
        
        # Export Options Panel
        export_options_panel = JPanel()
        export_options_panel.setLayout(BoxLayout(export_options_panel, BoxLayout.Y_AXIS))
        export_options_panel.setBorder(BorderFactory.createTitledBorder("Export Options"))
        
        # Create checkboxes for export options
        self.export_params_checkbox = JCheckBox("Export Parameters", True)  # Checked by default
        self.export_request_checkbox = JCheckBox("Export Requests", False)
        self.export_response_checkbox = JCheckBox("Export Responses", False)
        
        export_options_panel.add(self.export_params_checkbox)
        export_options_panel.add(self.export_request_checkbox)
        export_options_panel.add(self.export_response_checkbox)
        
        # Add some padding
        export_options_panel.add(JPanel())  # Empty panel for spacing
        
        content_panel.add(export_options_panel, BorderLayout.SOUTH)
        self.panel.add(content_panel, BorderLayout.CENTER)
        
        # Button Panel
        button_panel = JPanel()
        self.refresh_domains_button = JButton("Refresh Domains", actionPerformed=self.load_domains)
        self.refresh_domains_button.setBackground(Color(70, 130, 180))  # Steel blue
        self.refresh_domains_button.setForeground(Color.WHITE)
        button_panel.add(self.refresh_domains_button)
        
        export_button = JButton("Export", actionPerformed=self.export_http_history)
        export_button.setBackground(Color(34, 139, 34))  # Forest green
        export_button.setForeground(Color.WHITE)
        button_panel.add(export_button)
        self.panel.add(button_panel, BorderLayout.SOUTH)

        # Add tab to Burp
        callbacks.addSuiteTab(self)
        
        # Register listener
        callbacks.registerHttpListener(self)
        
        self.load_domains(None)
        print("[*] Burp Extension Loaded: HTTP History Exporter")
    
    def getTabCaption(self):
        return "HTTP Exporter"
    
    def getUiComponent(self):
        return self.panel

    def load_domains(self, event):
        print("[*] Fetching domains from Site Map...")
        site_map = self._callbacks.getSiteMap(None)  # Get all entries
        domains = set()

        if not site_map:
            print("[!] No entries found in Site Map.")
            return
        
        for entry in site_map:
            try:
                url = entry.getUrl()
                if url:
                    parsed_url = URL(url.toString())  # Safer way to get domain
                    domains.add(parsed_url.getHost())  # Get domain
            except Exception as e:
                print("[!] Error parsing URL: {}".format(e))
        
        self.domain_panel.removeAll()
        self.checkboxes = []
        for domain in sorted(domains):
            checkbox = JCheckBox(domain)
            self.checkboxes.append(checkbox)
            self.domain_panel.add(checkbox)
        
        self.domain_panel.revalidate()
        self.domain_panel.repaint()
        print("[*] Domains updated: {} found.".format(len(domains)))

    def export_http_history(self, event):
        print("[*] Starting export process...")

        try:
            # Get export options
            export_params = self.export_params_checkbox.isSelected()
            export_request = self.export_request_checkbox.isSelected()
            export_response = self.export_response_checkbox.isSelected()
            
            if not any([export_params, export_request, export_response]):
                JOptionPane.showMessageDialog(self.panel, "Please select at least one export option!", "Error", JOptionPane.ERROR_MESSAGE)
                print("[!] No export options selected.")
                return

            # Check if domains are selected
            selected_domains = [cb.getText() for cb in self.checkboxes if cb.isSelected()]
            if not selected_domains:
                JOptionPane.showMessageDialog(self.panel, "No domains selected!", "Error", JOptionPane.ERROR_MESSAGE)
                print("[!] No domains selected.")
                return

            print("[*] Selected domains: {}".format(selected_domains))
            print("[*] Export options - Parameters: {}, Request: {}, Response: {}".format(
                export_params, export_request, export_response))

            # Open file save dialog
            file_chooser = JFileChooser()
            file_chooser.setDialogTitle("Save CSV File")
            file_chooser.setSelectedFile(File("http_history.csv"))
            user_selection = file_chooser.showSaveDialog(self.panel)

            if user_selection != JFileChooser.APPROVE_OPTION:
                print("[!] Export canceled by user.")
                return

            file_path = file_chooser.getSelectedFile().getAbsolutePath()
            print("[*] Saving to file: {}".format(file_path))

            # Get proxy history
            http_traffic = self._callbacks.getProxyHistory()
            if not http_traffic:
                JOptionPane.showMessageDialog(self.panel, "No HTTP history found!", "Error", JOptionPane.ERROR_MESSAGE)
                print("[!] No HTTP history found.")
                return

            print("[*] Found {} HTTP history entries.".format(len(http_traffic)))

            # Set to keep track of processed URLs
            processed_urls = set()

            # Prepare CSV headers based on selected options
            headers = ["S.No.", "API"]
            if export_params:
                headers.append("Parameters")
            if export_request:
                headers.append("Request")
            if export_response:
                headers.append("Response")

            # Write to CSV
            with open(file_path, "w") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)  # Dynamic headers

                count = 0
                for entry in http_traffic:
                    try:
                        request_info = self._helpers.analyzeRequest(entry)
                        url = request_info.getUrl().toString()
                        parsed_url = URL(url)

                        # Skip if URL is not in the selected domains
                        if parsed_url.getHost() not in selected_domains:
                            continue

                        # Skip if URL has already been processed
                        if url in processed_urls:
                            continue

                        # Mark the URL as processed
                        processed_urls.add(url)

                        method = request_info.getMethod()
                        endpoint = parsed_url.getPath()

                        # Extract query parameters (only keys)
                        query_params = parsed_url.getQuery()
                        query_keys = []
                        if query_params:
                            query_keys = [param.split("=")[0] for param in query_params.split("&") if "=" in param]

                        # Extract request body parameters (only keys)
                        request_bytes = entry.getRequest()
                        request_body = self._helpers.bytesToString(request_bytes)[request_info.getBodyOffset():].strip()
                        body_keys = []
                        formatted_body = None
                        if request_body:
                            try:
                                parsed_body = json.loads(request_body)
                                formatted_body = json.dumps(parsed_body, indent=4)  # Pretty-print JSON request body
                                if isinstance(parsed_body, dict):
                                    body_keys = list(parsed_body.keys())
                                elif isinstance(parsed_body, list) and len(parsed_body) > 0 and isinstance(parsed_body[0], dict):
                                    body_keys = list(parsed_body[0].keys())
                            except json.JSONDecodeError:
                                # Handle URL-encoded body parameters
                                body_keys = [param.split("=")[0] for param in request_body.split("&") if "=" in param]
                                formatted_body = request_body  # Keep raw body if not JSON

                        # Build "API" column with request and body (if available)
                        api_info = "{} {}".format(method, url)

                        # Prepare row data
                        row_data = [count + 1, api_info]  # S.No. and API are always included

                        # Add Parameters column if selected
                        if export_params:
                            parameters = "\n".join(query_keys + body_keys) if query_keys or body_keys else ""
                            row_data.append(parameters)

                        # Add Request column if selected
                        if export_request:
                            full_request = self._helpers.bytesToString(request_bytes)
                            row_data.append(full_request)

                        # Add Response column if selected
                        if export_response:
                            response_bytes = entry.getResponse()
                            if response_bytes:
                                full_response = self._helpers.bytesToString(response_bytes)
                                row_data.append(full_response)
                            else:
                                row_data.append("")  # Empty response

                        count += 1
                        writer.writerow(row_data)
                    except Exception as e:
                        print("[!] Error processing entry: {}".format(e))

            print("[*] HTTP history exported to {}".format(file_path))
            JOptionPane.showMessageDialog(self.panel, "Export completed successfully! {} entries exported.".format(count), 
                                         "Success", JOptionPane.INFORMATION_MESSAGE)
        except Exception as e:
            print("[!] Error during export: {}".format(e))
            JOptionPane.showMessageDialog(self.panel, "Error during export: {}".format(e), "Error", JOptionPane.ERROR_MESSAGE)

    
    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        pass
