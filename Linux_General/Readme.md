# How to install ISCE 2.2.0 on Linux-based machines, using (almost) stand-alone miniconda3 packages

### https://winsar.unavco.org/software/isce

### Last update 11/2018

This note will show you how to install the latest [ISCE](https://winsar.unavco.org/software/isce) (**2.2.0**) on 
various **64-bit, Linux-based machines**, including the most popular **Ubuntu**. The routines were tested on **NASA's 
supercomputer Pleiades** and worked well. It works the best if you have either 
of the following situations:

* You don't have any _root_ privileges (e.g. `su` or `sudo`) on the machine you are going to install ISCE
* You are installing ISCE on the machine that does not have a package manager (such as Ubuntu's `apt`)
* You don't want to install ISCE using packages in your system because their versions may be out of date or because of other reasons

We will assume that you want to install ISCE in your `~/Software` directory, using all packages and compilers of your own.
We recommend the [conda](https://conda.io/docs/) package manager for sorting all the dependencies out. 



## Install conda and all the prerequisites

Go to the [Miniconda download page](https://conda.io/miniconda.html) and download the 64-bit installer for Python 3.7,
or you can run this on your terminal:

    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

If you choose to install _anaconda_ instead of _miniconda_, later you have to set up a separate environment for `gdal`
since some of our packages will come from the user-contributed repository. To make it simple, we use _miniconda_ here
and will only install the minimum required packages. 

Run the script and choose a path to install _miniconda_, and let's say it would be installed at `~/Software/miniconda3`.

    ./Miniconda3-latest-Linux-x86_64.sh

Next, it's time to install all the dependencies. Make sure the `conda` command is available now (if not, add the `bin` 
folder in _miniconda3_ into your **PATH** variable). Run the following commands in order:

    conda config --add channels conda-forge    # openmotif is only in this channel
    conda install openmotif                    # required by mdx, for visualizing interferograms
    conda install scons                        # ISCE installer
    conda install gcc libgcc
    conda install fftw                         
    conda install hdf5 h5py
    conda install numpy scipy matplotlib
    conda install ipython
    conda install opencv
    conda install gdal
    conda install cython

## Steps before installing ISCE

Firstly go to where `cython` is and make a soft link to cython3:

    cd ~/Software/miniconda3/bin/
    ln -s cython cython3

Next, go to the library folder and change the soft-link pointer of `libstdc++.so`. The latest version 
(e.g. `6.0.25` or `6.0.24`) should work:

    cd ~/Software/miniconda3/lib/
    unlink libstdc++.so
    unlink libstdc++.so.6
    ln -s libstdc++.so.6.0.25 libstdc++.so
    ln -s libstdc++.so.6.0.25 libstdc++.so.6

Finally, there are other three required libraries that would not be found in miniconda. These libraries are fundamentals
of a linux system and can be found somewhere in the system, and all we have to do is to manually make a soft link 
of these libraries to this folder. `/usr/lib64` is a possible locations for these, but they may be at different folders
on your machine. 

    cd ~/Software/miniconda3/lib/
    ln -s /usr/lib64/libc.so libc.so
    ln -s /usr/lib64/libm.so libm.so
    ln -s /usr/lib64/libpthread.so libpthread.so

## Make the configuration file for installing ISCE

Download ISCE from the website, extract it, and go to the extracted folder, here assuming `~/Software/isce-2.2.0`.

    cd ~/Software/isce-2.2.0
    touch SConfigISCE    # make an empty text file

Open `SConfigISCE` and enter the following entries:

    # PRJ_SCONS_BUILD is where the temporary files are when installing ISCE
    PRJ_SCONS_BUILD =   ~/Software/isce-2.2.0/build
    # PRJ_SCONS_INSTALL is where the ISCE binaries and python modules can be accessed
    PRJ_SCONS_INSTALL = ~/Software/isce-2.2.0-build

    # LIBPATH points to miniconda3's lib
    LIBPATH = ~/Software/miniconda3/lib
    # CPPPATH points to the c libraries (include) and python 3.x bindings (here it's include/python3.6m)
    CPPPATH = ~/Software/miniconda3/include/python3.6m ~/Software/miniconda3/include 
    # FORTRANPATH points to the c libraries (include)
    FORTRANPATH = ~/Software/miniconda3/include  

    # libraries needed for mdx display utility, point to miniconda's lib or include
    MOTIFLIBPATH = ~/Software/miniconda3/lib       # path to libXm.dylib
    X11LIBPATH =   ~/Software/miniconda3/lib       # path to libXt.dylib
    MOTIFINCPATH = ~/Software/miniconda3/include/Xm   # path to location of the Xm
    X11INCPATH =   ~/Software/miniconda3/include/X11  # path to location of the X11 directory

    # locations of the compilers
    FORTRAN = ~/Software/miniconda3/bin/gfortran
    CC =      ~/Software/miniconda3/bin/gcc
    CXX =     ~/Software/miniconda3/bin/g++ 

## Install ISCE

As long as you set up the requirements correctly, this step should be simple:

    cd ~/Software/isce-2.2.0
    SCONS_CONFIG_DIR=. scons install

## Make ISCE searchable by your shell and Python

Note that in ISCE 2.2.0 there's no folder named `isce` inside the installation folder -- all the files are now directly
under the installation folder. Therefore, to make the python command `import isce` available, you can choose one of 
these two ways:

* when setting up `SConfigISCE`, make _PRJ\_SCONS\_INSTALL_ end with `isce`; for example, 
    `PRJ_SCONS_INSTALL = ~/Software/isce-2.2.0/isce`

* go to the installation folder and make a soft link; for example,
    `ln -s ~/Software/isce-2.2.0-build ~/Software/isce-2.2.0-build/isce`

The last step goes here. Open your shell configuration file (e.g. `~/.bashrc`) or create a 
separate configuration file (e.g. `~/ISCE_CONFIG`), and add the following lines:

    export ISCE_HOME="~/Software/isce-2.2.0-build"    # your installation folder
    export PYTHONPATH="$ISCE_HOME:$PYTHONPATH"        # there should be a folder named "isce" inside the newly added python path
    export PATH="$ISCE_HOME/applications:$PATH"

After sourcing the configuration file (`source ~/ISCE_CONFIG` or `source ~/.bashrc`), you should be able to run ISCE!
There are two ways to test if ISCE is correctly installed:

* `topsApp.py --steps --help`
* Open Python, and `import isce`
