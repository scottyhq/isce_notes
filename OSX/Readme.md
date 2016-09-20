# Notes for installing ISCE_201609 (on Mac OSX 10.11.5 )
###https://winsar.unavco.org/isce.html
###updated 09/2016

## Installing single version from scratch


1) Download ISCE:
```
wget https://winsar.unavco.org/software/ISCE/isce-2.0.0_20160908.tar.bz2
bunzip2 isce-2.0.0_20160908.bz2
tar -xzf isce-2.0.0_20160908.tar
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
gcc-6 --version
gcc-6 (Homebrew gcc 6.2.0) 6.2.0
gfortran-6 --version
GNU Fortran (Homebrew gcc 6.2.0) 6.2.0
```


3) ISCE requires Python2 to install and Python3 to run. Use Anaconda Python installations for this:
```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
conda env create -f isce_201609.yml
conda env create -f scons.yml
```

Check the versions (need GDAL>2.0)
```
source activate isce_201609
gdalinfo --version
GDAL 2.1.0, released 2016/04/25
```

4) Update ISCE configuration file (here is mine as a template):
`vi ~/.isce/SConfigISCE`
```
PRJ_SCONS_BUILD=/Users/scott/Software/ISCE_SRC/isce-2.0.0_20160908/build
PRJ_SCONS_INSTALL=/Users/scott/Software/ISCE/isce_201609

LIBPATH=/Users/scott/miniconda3/envs/isce_201609/lib /usr/local/lib /usr/local/gfortran/lib
CPPPATH=/Users/scott/miniconda3/envs/isce_201609/include/python3.5m /usr/local/include
FORTRANPATH=/usr/local/include 

FORTRAN=/usr/local/bin/gfortran-6
CC=/usr/local/bin/gcc-6
CXX=/usr/local/bin/g++-6

MOTIFLIBPATH=/usr/local/lib
MOTIFINCPATH=/usr/local/include
X11LIBPATH=/opt/X11/lib
X11INCPATH=/opt/X11/include
```


4) Compile ISCE using scons:
```
cd /Users/scott/Software/ISCE_SRC/isce-2.0.0_20160908
export PYTHONPATH=/Users/scott/Software/ISCE_SRC/isce-2.0.0_20160908/configuration
export SCONS_CONFIG_DIR=/Users/scott/.isce
source activate scons
scons install 
# if scons fails for some reason, run this before running again:
rm -rf config.log .sconsign.dblite .sconf_temp build/
```

5) Create an alias in `.bashrc` to activate Python3 whenever you want to run isce
`alias start_isce_201609="source activate isce_201609; source ~/.isce/.isceenv_201609"`
Where `.isceenv` contains:
```
export ISCE_ROOT=/Users/scott/Software/ISCE/isce_201609
export ISCE_HOME=$ISCE_ROOT/isce
export PATH=$ISCE_HOME/applications:$ISCE_HOME/bin:$PATH
export PYTHONPATH=$ISCE_ROOT:$PYTHONPATH
```

6) Check installation:
```
start_isce_201609
python3
import isce
isce.version.release_version
```

7) Run ISCE! here is an easy place to get test data: http://topex.ucsd.edu/gmtsar/downloads/
```
start_isce_201609
insarApp.py --steps
```
