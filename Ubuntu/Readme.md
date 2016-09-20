# Notes for installing ISCE 2.0.0_20160908 (on Ubuntu 16.04 LTS)
###https://winsar.unavco.org/isce.html

### Last update 09/2016

## Installing single version from scratch


1) A list of ubuntu packages that need to be installed (if they aren't already):
```
apt-get install libgmp-dev libmpfr-dev libmpc-dev libc6-dev-i386
```


2) ISCE requires Python2 to install and Python3 to run. Use Anaconda Python installations for this:
```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

conda env create -f isce_201609.yml
conda env create -f scons.yml
source activate scons
```


3) Download ISCE to location where you want to keep the source code:
```
wget http://winsar.unavco.org/software/ISCE/isce-2.0.0_20160908.tar.bz2
mv ~/Downloads/isce-2.0.0_20160908.tar.bz2 ~/Software/ISCE
bunzip2 isce-2.0.0_20160908.tar.bz2
tar -xvf isce-2.0.0_20160908.tar
```


4) Update ISCE configuration file (here is mine as a template):
`vi ~/.isce/SConfigISCE`
```
PRJ_SCONS_BUILD=/home/scott/Software/ISCE/isce-2.0.0_20160908/build
PRJ_SCONS_INSTALL=/usr/local/isce-2.0.0_20160908/isce

LIBPATH=/home/scott/miniconda3/envs/isce_201609/lib /usr/lib/x86_64-linux-gnu
CPPPATH=/home/scott/miniconda3/envs/isce_201609/include/python3.5m
FORTRANPATH=/usr/include

FORTRAN=/usr/bin/gfortran
CC=/usr/bin/gcc
CXX=/usr/bin/g++

MOTIFLIBPATH = /usr/lib/x86_64-linux-gnu 
X11LIBPATH = /usr/lib/x86_64-linux-gnu  
MOTIFINCPATH = /usr/include/Xm    
X11INCPATH = /usr/include/X11   
```


4) Install ISCE with scons (example as root to install to `/usr/local`)
```
su 
cd isce-2.0.0_20160908
export PYTHONPATH=/home/scott/Software/isce-2.0.0_20160908/configuration
export SCONS_CONFIG_DIR=/home/scott/.isce

source activate scons
scons install
```

5) Create an alias in `.bashrc` to activate Python3 whenever you want to run isce
`alias start_isce_201609="source activate isce_201609; source ~/.isce/.isceenv_201609"`
Where `.isceenv_201609` contains:
```
export ISCE_ROOT=/usr/local/isce-2.0.0_20160908
export ISCE_HOME=$ISCE_ROOT/isce
export PATH=$ISCE_HOME/bin:$ISCE_HOME/applications:$PATH
export PYTHONPATH=$ISCE_ROOT:$ISCE_HOME/applications:$ISCE_HOME/component
```

6) To Run ISCE:
```
alias start_isce="source activate isce_201609; source ~/.isce/.isceenv_201609"
insarApp.py --steps
```


## Installing multiple versions / development snapshots
1) Clone the previous conda environment and update packages (if you want). 
```
conda create --name isce_XXXXX --clone isce_201609
conda update --all
```

2) Change the SConfigISCE file
```
cp ~/.isce/SConfigISCE ~/.isce/SConfigISCE_201609
vi ~/.isce/SConfigISCE
PRJ_SCONS_BUILD=/home/scott/Software/isce-2.0.0_XXXXX/build
PRJ_SCONS_INSTALL=/usr/local/isce-2.0.0_XXXXX/isce
LIBPATH=/home/scott/miniconda3/envs/isce_XXXXX/lib /usr/lib/x86_64-linux-gnu
CPPPATH=/home/scott/miniconda3/envs/isce_XXXXX/include/python3.5m

3) Install with scons as root
```
su 
cd /home/scott/Software/isce-2.0.0_XXXXX
export PYTHONPATH=/home/scott/Software/isce-2.0.0_XXXXX/configuration
export SCONS_CONFIG_DIR=/home/scott/.isce

source activate scons
scons install
```

4) Create a new alias and environment file
```
alias start_isce_XXXXX="source activate isce_XXXXX; source ~/.isce/.isceenv_XXXX"`
```


5) Update the environment file `~/.isce/.isceenv_XXXXX`:
```
export ISCE_ROOT=/usr/local/isce-2.0.0_XXXXX
export ISCE_HOME=$ISCE_ROOT/isce
export PATH=$ISCE_HOME/bin:$ISCE_HOME/applications:$PATH
export PYTHONPATH=$ISCE_ROOT:$ISCE_HOME/applications:$ISCE_HOME/component
```

