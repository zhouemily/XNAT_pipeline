
import argparse
import os
import pysend
from pysend import StorageCommitmentClient

def send_dicom_to_server(server_host, server_port, dicom_path, debug_mode=False):
    client = StorageCommitmentClient(server_host, server_port, debug=debug_mode)
    
    if os.path.isfile(dicom_path):
        try:
            response = client.send_file(dicom_path)
            if response.success:
                print(f"DICOM file '{dicom_path}' sent successfully to {server_host}:{server_port}.")
            else:
                print(f"Failed to send DICOM file '{dicom_path}'.")
                print("Response status:", response.status)
        except Exception as e:
            print(f"An error occurred while sending '{dicom_path}':", str(e))
    elif os.path.isdir(dicom_path):
        for root, _, files in os.walk(dicom_path):
            for file in files:
                dicom_file_path = os.path.join(root, file)
                try:
                    response = client.send_file(dicom_file_path)
                    if response.success:
                        print(f"DICOM file '{dicom_file_path}' sent successfully to {server_host}:{server_port}.")
                    else:
                        print(f"Failed to send DICOM file '{dicom_file_path}'.")
                        print("Response status:", response.status)
                except Exception as e:
                    print(f"An error occurred while sending '{dicom_file_path}':", str(e))
    else:
        print("Invalid input. Please provide a valid DICOM file or directory path.")

def main():
    parser = argparse.ArgumentParser(description="Send DICOM files to a specified server and port.")
    
    # Define command-line arguments
    parser.add_argument("-f", "--file", type=str, help="Path to the DICOM file to send.")
    parser.add_argument("-d", "--directory", type=str, help="Path to the directory containing DICOM files to send.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode.")
    parser.add_argument("-D", "--debug", action="store_true", help="Enable debug mode.")
    
    args = parser.parse_args()
    
    server_host = "xnat1.beckman.illinois.edu"
    server_port = 8104
    
    if args.verbose:
        pysend.set_verbose()
    
    if args.file:
        send_dicom_to_server(server_host, server_port, args.file, args.debug)
    elif args.directory:
        send_dicom_to_server(server_host, server_port, args.directory, args.debug)
    else:
        print("Please specify either a DICOM file (-f) or a directory of DICOM files (-d).")

if __name__ == "__main__":
    main()

