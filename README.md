# EconomicTrender

Make sure to have IDLE installed
Run python version 3 (3.10)
1) Requests is not a built in module (does not come with the default python installation), so you will have to install it:

OSX/Linux
Use $ pip install requests (or pip3 install requests for python3) if you have pip installed. If pip is installed but not in your path you can use python -m pip install requests (or python3 -m pip install requests for python3)

Alternatively you can also use sudo easy_install -U requests if you have easy_install installed.

Alternatively you can use your systems package manager:

For centos: yum install python-requests For Ubuntu: apt-get install python-requests

Windows
Use pip install requests (or pip3 install requests for python3) if you have pip installed and Pip.exe added to the Path Environment Variable. If pip is installed but not in your path you can use python -m pip install requests (or python3 -m pip install requests for python3)

Alternatively from a cmd prompt, use > Path\easy_install.exe requests, where Path is your Python*\Scripts folder, if it was installed. (For example: C:\Python32\Scripts)

If you manually want to add a library to a windows machine, you can download the compressed library, uncompress it, and then place it into the Lib\site-packages folder of your python path. (For example: C:\Python27\Lib\site-packages)

From Source (Universal)
For any missing library, the source is usually available at https://pypi.python.org/pypi/. You can download requests here: https://pypi.python.org/pypi/requests

On mac osx and windows, after downloading the source zip, uncompress it and from the termiminal/cmd run python setup.py install from the uncompressed dir.

Reference: https://stackoverflow.com/questions/17309288/importerror-no-module-named-requests


2) You need to install pandas with:
pip install pandas
If you run into issues with privileges, you may need to run:
sudo pip install pandas
It is also possible on Python 3 that you may need to run:
pip3 install pandas (although pip may be pointing to pip3 already). You can read about differences between pip versions on this SO post.
If you don't have pip installed, see here for installation.

Reference: https://stackoverflow.com/questions/54497098/import-pandas-as-pd-importerror-no-module-named-pandas



3) Install matplotlib. Command: pip3 install matplotlib
Reference: https://stackoverflow.com/questions/18176591/importerror-no-module-named-matplotlib-pyplot

4) Install seaborn. Command: pip3 install seaborn

