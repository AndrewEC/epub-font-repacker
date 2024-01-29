# Epub Font Repacker
A utility to change the primary font used in an epub file.

To create the repackaged epub file this tool will perform the following steps:
1. Extract the contents of an epub file to a temp directory
2. Copy the CSS file and Font file to the temp directory
3. Add the CSS file and Font file to the epub manifest
4. Add a link to the CSS file in all identifiable xhtml and html files
5. Compress the temp directory contents into the new epub file

This will not delete or overwrite the existing epub file. It will generate a new epub with `-repacked` appended
to the file name.


### Usage
From the root of the project directory execute the powershell script `CreateVenv.ps1` then run the following command:
> python -m repack <Path_To_Epub>

replacing &lt;Path_To_Epub&gt; with the absolute path to the epub file.