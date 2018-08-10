# Notes for installing ISCE 2.2.0 (on Ubuntu 18.04 LTS)
### https://winsar.unavco.org/isce.html

### Last update 07/2018

## NOTE: this is a simplified instruction set for installing [ISCE 2.2.0](https://winsar.unavco.org/software/isce) on [Ubuntu 18.04 LTS](https://wiki.ubuntu.com/BionicBeaver/ReleaseNotes?_ga=2.87047249.813606057.1533187033-1771092189.1532981728) 

[Notes](Readme_201609.md) on installing previous versions used the [conda](https://conda.io/docs/) package manager for custom Python environments. The drawback with conda is that you can run into errors if conda packages and system libraries are built against different compiler versions  (see [this ISCE user forum post](http://earthdef.caltech.edu/boards/4/topics/1925)). See these notes [here](https://conda.io/docs/user-guide/tasks/build-packages/compiler-tools.html) about conda compilers. 

One solution is either use entirely system installed dependencies or install all dependencies with conda, and the following notes are for installing ISCE without conda. Check out other installation notes [here](https://github.com/piyushrpt/oldLinuxSetup). Or consider using [Docker](../Docker)!


1) A list of Ubuntu packages that need to be installed (if they aren't already):
```
sudo apt update
sudo apt install -y gfortran libmotif-dev libhdf5-dev libfftw3-dev libgdal-dev scons python3 cython3 python3-scipy python3-matplotlib python3-h5py python3-gdal python3-pip
```

2) Download ISCE to location where you want to keep the source code:
```
cd /opt
wget https://imaging.unavco.org/software/ISCE/isce-2.2.0.tar.bz2
bunzip2 isce-2.2.0.tar.bz2
tar -xvf isce-2.2.0.tar.bz2
```

3) Update this ISCE scons installation configuration file (and move to /opt/isce-2.2.0):
```
PRJ_SCONS_BUILD=/opt/isce-2.2.0/build
PRJ_SCONS_INSTALL=/opt/isce-2.2.0/install/isce

LIBPATH=/usr/lib/x86_64-linux-gnu /usr/lib /usr/lib/x86_64-linux-gnu/hdf5/serial
CPPPATH=/usr/include/x86_64-linux-gnu /usr/include /usr/include/python3.6m /usr/include/hdf5/serial /usr/include/gdal
FORTRANPATH=/usr/include /usr/lib/gcc/x86_64-linux-gnu/7/finclude

FORTRAN=/usr/bin/gfortran
CC=/usr/bin/gcc
CXX=/usr/bin/g++

MOTIFLIBPATH = /usr/lib/x86_64-linux-gnu
X11LIBPATH = /usr/lib/x86_64-linux-gnu
MOTIFINCPATH = /usr/include/Xm
X11INCPATH = /usr/include/X11

ENABLE_CUDA=False
```

4) Install ISCE with scons
```
cd isce-2.2.0
export PYTHONPATH=/opt/isce-2.2.0/configuration
export SCONS_CONFIG_DIR=/opt/isce-2.2.0
scons install --skipcheck
```

5) Create a configuration file (`~/ISCE_CONFIG`) with the correct evironment variables to run ISCE
```
export ISCE_ROOT=/opt/isce-2.2.0/install
export ISCE_HOME=$ISCE_ROOT/isce
export PATH=$ISCE_HOME/bin:$ISCE_HOME/applications:$PATH
export PYTHONPATH=$ISCE_ROOT:$ISCE_HOME/applications:$ISCE_HOME/component
```

6) After sourcing the configuration file, you should be able to run ISCE!
```
source ~/ISCE_CONFIG
topsApp.py --steps --help
```
