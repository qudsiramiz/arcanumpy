# Generate the .rst files for the website
sphinx-apidoc -o /home/vetinari/Desktop/git/arcanumpy/src/rst_files /home/vetinari/Desktop/git/arcanumpy/arcanumpy/ --separate

# Run the update_index_rst_file.py script to update the index.rst file
python update_modules_rst_file.py

# Run the sphinx-build command to generate the html files
# sphinx-build -b html "/home/vetinari/Desktop/git/arcanumpy/src/" "/home/vetinari/Desktop/git/arcanumpy/docs"

git add --all
git commit -m "Update the documentation"
git push origin main

