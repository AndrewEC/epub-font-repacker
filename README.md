# Epub Font Repacker
A utility to change the primary font used in an epub file.

This will extract the contents of the epub file to a temp directory, copy in a css and font file, add the necessary
entries to the manifest, then updated all the identifiable xhtml and html files with links to the new CSS file,
and finally repackage the modified contents into a new epub file.

This will not delete or overwrite the existing epub but will create a whole a copy of the original with some
modifications.


### Usage
From the root of the project directory execute the powershell script `CreateVenv.ps1` the run the following command:
> python -m repack <Absolute_Path_To_Epub>

replacing &lt;Path_To_Epub&gt; with the absolute path to the epub file.