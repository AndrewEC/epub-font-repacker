# Epub Font Repacker
A utility to change the primary font used in an epub file.

## Cloning
To clone the project and the required submodules run:
> git clone --recurse-submodules https://github.com/AndrewEC/epub-font-repacker.git

### Usage
From the root of the project (the same directory as this README.md file) execute
the powershell script `RunScript.ps1 Install` then run the following command:
> python -m repack Path_To_Epub Font

replacing `Path_To_Epub` with the absolute path to the epub file and `Font` with
the desired font.

To get a lit of the available fonts you can execute the following command:
> python -m repack --help

### Adding Fonts
To make a new font available to repackage an epub with simply copy the font file into the
`./core/resources/` directory where the pre-packaged fonts are already located.

## Process
To create the repackaged epub file this tool will:
1. Extract the contents of an epub file to a temp directory.
2. Copy the CSS file and Font file to the temp directory.
3. Add the CSS file and Font file to the epub manifest.
4. Add a link to the CSS file in all identifiable .xhtml and .html files.
5. Compress the temp directory contents into the new epub zip file.
6. Delete the temp directory.

This will not delete or overwrite the existing epub file. It will generate a new epub with `-repacked` appended
to the file name.

## Quality Metrics
Run the `Runscript.ps1 All` command to activate the virtual environment, install
dependencies, run flake8, run unit tests with code coverage metrics, and audit the
dependencies.
