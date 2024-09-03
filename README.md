# ADB_Data_Sync_and_Fetch_Toolset
This repository contains two Python scripts designed for automating data synchronization and retrieval from external devices. They are used to mount remote directories, sync files between local and remote systems, filter data by criteria, and rename file extensions, making it easier to manage and transfer data efficiently.

Repository Content:

sync_script.py - A script responsible for synchronizing data between a local and remote directory. It automates the process of mounting and unmounting remote resources and copying the latest files.

fetch_data.py - A script that facilitates fetching files from mobile devices using ADB commands. It allows filtering files by date, downloading them, and renaming file extensions to match a new format.

File Extension Handling: The fetch_data.py script also includes functionality for renaming files by changing their extensions. This is particularly useful for adapting files to new formats or ensuring compatibility with other systems.



Usage Instructions:

To use these scripts, the user must have access to the appropriate local and remote directories and Android devices with USB debugging enabled. The scripts can be run from the command line, and their configuration is done by editing the relevant paths in the code.
