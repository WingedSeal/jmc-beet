cd ./src/dist
rm -r jmc-beet* /a
cd ..
python setup.py sdist bdist_wheel 
twine upload dist/jmc-beet*
rm -r jmc-beet.egg-info
rm -r build
cd ..