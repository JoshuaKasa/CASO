# CASO Language Support in Vim and NeoVim

Enhance your Vim and NeoVim setup with syntax highlighting for the CASO programming language. This guide walks you through the process of integrating CASO syntax highlighting into your editor, ensuring `.caso` files are both recognized and beautifully styled.

## Setup Overview

The configuration involves two main components stored in distinct folders:

- `ftdetect`: Contains `caso.vim` for detecting `.caso` files and setting the appropriate filetype.
- `syntax`: Contains `caso.vim` for defining the syntax highlighting rules specific to CASO.

If you already got `ftdetect` and `syntax` directories within your Vim or NeoVim configuration space, you will merge the contents of this setup into your existing structure. Otherwise, just copy the provided folders directly into your configuration directory.

## Installation Instructions

1. **Prepare Configuration Directory**:
   - For **Vim**: Navigate to your `~/.vim` directory.
   - For **NeoVim**: Navigate to your `~/.config/nvim` directory.
   - **Note**: This might vary depending on your system and configuration, just go where your `init.vim` or `vimrc` file is located.

2. **Integrate Folders**:
   - If `ftdetect` and `syntax` directories do not exist, copy the provided folders directly into your configuration directory.
   - If these directories already exist, merge the content of the provided `ftdetect` and `syntax` folders with your existing ones.

3. **Verify Installation**:
   - Open a `.caso` file in Vim or NeoVim and the syntax highlighting should be automatically applied.

## Troubleshooting

If syntax highlighting does not appear or you encounter issues, follow these steps:

1. **Manually Set Syntax**: In Vim or NeoVim, execute `:set syntax=caso` to manually apply CASO syntax highlighting.

2. **Check Filetype Detection**:
   - Execute `:set filetype?` to confirm if the filetype is correctly identified as `caso`.
   - If the filetype is not set to `caso`, ensure the `ftdetect` folder is correctly placed within your configuration directory and contains the `caso.vim` file without errors.

3. **Recheck Folder Placement**:
   - Confirm that `ftdetect` and `syntax` folders are correctly integrated into your Vim/NeoVim configuration directory.
   - Ensure that the paths align with your editor's expectations, which may vary based on custom configurations or installation methods.

4. **File Permissions**:
   - Verify that the `caso.vim` files within `ftdetect` and `syntax` folders have the correct file permissions to be read by your editor.

5. **Configuration Conflicts**:
   - Look for any conflicting settings in your `vimrc` or `init.vim` file that might override or interfere with the CASO syntax highlighting.
   - Check if other plugins or syntax files are conflicting with CASO's syntax highlighting.

6. **Clear Cache**:
   - Some versions of Vim and NeoVim cache syntax files. Clearing the cache or restarting the editor can help ensure changes are applied.

If issues persist, consider re-copying the files to ensure correct placement and syntax. For further assistance, please open an issue in this repository, and we'll be glad to help.