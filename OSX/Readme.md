# Notes for installing ISCE (on Mac OSX 10.11.5 )
###https://winsar.unavco.org/isce.html
###updated June 2016

## Installing single version from scratch


1) Download ISCE:
```
wget https://winsar.unavco.org/software/ISCE/isce-2.0.0_201604.bz2
bunzip2 isce-2.0.0_201604.bz2
tar -xzf isce-2.0.0_201604.tar
```


2) Install dependencies with Homebrew:
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install gcc gfortran fftw lesstif imagemagick
```
Or if you already have homebrew, it might be a good idea to upgrade packages before installing:
```
brew update
brew upgrade
```
Check the versions:
```
gcc-5 --version
gcc-5 (Homebrew gcc 5.3.0) 5.3.0
gfortran-5 --version
GNU Fortran (Homebrew gcc 5.3.0) 5.3.0
```


3) ISCE requires Python2 to install and Python3 to run. Use Anaconda Python installations for this:
```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
conda env create -f isce.yml
conda env create -f scons.yml
```


4) Update ISCE configuration file (here is mine as a template):
`vi ~/.isce/SConfigISCE`
```
PRJ_SCONS_BUILD=/Users/scott/Software/ISCE_SRC/isce-2.0.0_201604/build
PRJ_SCONS_INSTALL=/Users/scott/Software/ISCE/isce-2.0.0_201604

LIBPATH= /usr/local/Cellar/gcc/5.3.0/lib/gcc/5 /Users/scott/Software/miniconda3/envs/isce/lib /usr/local/lib /opt/X11/lib
CPPPATH=/Users/scott/Software/miniconda3/envs/isce/include/python3.5m /usr/local/include /opt/X11/include
FORTRANPATH=/usr/local/include 

FORTRAN=/usr/local/bin/gfortran-5
CC=/usr/local/bin/gcc-5
CXX=/usr/local/bin/g++-5

MOTIFLIBPATH=/usr/local/lib
MOTIFINCPATH=/usr/local/include
X11LIBPATH=/opt/X11/lib
X11INCPATH=/opt/X11/include
```


4) Compile ISCE using scons:
```
cd /Users/scott/Software/ISCE_SRC/isce-2.0.0_201604
export SCONS_CONFIG_DIR=/Users/scott/.isce
source activate scons
scons install 
ln -s /Users/scott/Software/ISCE/isce-2.0.0_201604 /Users/scott/Software/ISCE/isce 
```

5) Create an alias in `.bashrc` to activate Python3 whenever you want to run isce
`alias start_isce="source activate isce; source ~/.isce/.isceenv"`
Where `.isceenv` contains:
```
export ISCE_ROOT_DIR=/Users/scott/Software/ISCE
export ISCE_HOME=$ISCE_ROOT_DIR/isce
export PATH=$ISCE_HOME/applications:$ISCE_HOME/bin:$PATH
export PYTHONPATH=$ISCE_ROOT_DIR:$PYTHONPATH
```

6) Check installation:
```
start_isce
python3
import isce
isce.version.release_version
```

7) Run ISCE!
```
start_isce
insarApp.py --steps
```
