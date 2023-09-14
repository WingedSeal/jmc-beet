cd src/dist
del jmc-beet* /a
cd ..
python setup.py sdist bdist_wheel 
START /B /wait cmd /c "twine upload dist/jmc-beet*"
rmdir /s /Q jmc_beet.egg-info
rmdir /s /Q build
cd ..