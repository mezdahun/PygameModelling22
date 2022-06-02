# **PyGame Modelling Workshop 2022**

**Pyg**ame **Mod**elling **W**orkshop 20**22** (pygmodw22).

This is the offcicial repo of the pygame modelling course for collective systems workshop 2022 Berlin.

## Welcome to the Workshop
During this workshop you will learn about using a python-based game engine (pygame) for agent-based modelling and simulation tasks to model collective behavior.
To use the provided code base you will need the following:

### Prerequisites
1. **Operating System:** The code has been tested on Ubuntu 18, Windows 10, and ...
2. **Python 3.7+:** You will need to have a python version >=3.7.0. You can check the version of your python interpreter with `python --version`. In case you have multiple python base version (e.g. 2.x and 3.x) use `python3 --version`. In case your python (3) version is lower than 3.7 or you don't have python3 installed on your system yet, please follow [this guide](https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/) to install python 3.7 on Ubuntu, Windows or Mac.
3. **pip:** To install all the requirements of the code we will use pip. Please be sure to have a pip version for python 3+ (and not for python 2). You can check this with `pip --version` or sometimes `pip3 --version` in case of multiple python base versions (e.g. 2.x and 3.x) and by that multiple pip versions. The resulting line should end with "(python 3.x)" where x is the minor version of your python interpreter and should be larger or equal than 7. In case you have multiple minor versions (e.g. 3.5 and 3.7, use `python3.7 -m pip --version` or any minor version larger or equal to 7). In case you don't have pip installed yet use this guide to install pip on [Windows](https://www.liquidweb.com/kb/install-pip-windows/), [Ubuntu](https://www.odoo.com/forum/help-1/how-to-install-pip-in-python-3-on-ubuntu-18-04-167715) or [Mac](https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/#macos).
4. **GIT:** to access the code you will need git installed on your system. In case this is not yet done, please install it using [this guide](https://github.com/git-guides/install-git).

**At this point you have python3.7+, pip (for the same python version) and git installed on your system.**

### Installation
5. **Clone this repo:** Open the terminal and use the following command to clone the repo `git clone https://github.com/mezdahun/PygameModelling22.git`.
6. **(optional) Create new virtual environment**: We highly recommend using a virtual environment for the workshop so that you don't have version mismatches with other projects. We recommend using [pipenv](https://pipenv.pypa.io/en/latest/) or [venv](https://docs.python.org/3/library/venv.html). As creating and managing virtual environments can change depending on which software you are using (e.g. pipenv, venv, conda, etc.), we mark this point as optional and is out of scope for this workshop due to time limitation. They are highly recommended nonetheless. You can read about how to create and activate virtual environments under the links provided above.
7. **Installation of the code base**: At this point you can install the code base with all it's dependencies. Move into the newly created/cloned folder with `cd PygameModelling22` and install the package with all it's dependencies using `pip install -e .`. Note that we used the `-e` flag to install the code. This way if you change something in the provided scripts that change will automatically be present in your pip package. (In case in step 2 you had to use `pip3` for the correct python version, here you also need to use `pip3 install -e .` or if you have multiple minor versions `python3.x -m pip install -e .` where x is your minor python3 version and is larger or equal than 7)
8. **Test the installation**: Now you can test if everything went well by running a test simulation. From the same folder run `python test_installation.py`. In case you have multiple python base versions installed (e.g. 2.x and 3.x), be sure you are using python3.7 or higher, so use `python3 test_installation.py` or `python3.x test_installation.py` accordingly (where again, x is the minor version of your python3 installation and is larger or equal than 7).

**At this point you are ready for the workshop! Happy coding!**
