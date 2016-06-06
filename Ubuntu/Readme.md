# Notes for installing ISCE 2.0.0  (on Ubuntu 14 )
###https://winsar.unavco.org/isce.html

## Installing single version from scratch


1) A list of ubuntu packages that need to be installed (if they aren't already):
```
apt-get install libgmp-dev libmpfr-dev libmpc-dev libc6-dev-i386
```


2) ISCE requires Python2 to install and Python3 to run. Use Anaconda Python installations for this:
```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

conda env create -f isce.yml
conda env create -f scons.yml
source activate scons
```


3) Download ISCE and generate installation parameter file:
```
wget https://winsar.unavco.org/software/ISCE/isce-2.0.0.bz2
bunzip2 isce-2.0.0.bz2
mv isce-2.0.0 isce-2.0.0.tar
tar -xzf isce-2.0.0.tar
cd ./isce-2.0.0/setup
./install.sh -i NONE
```


4) Update ISCE configuration file (here is mine as a template):
`vi ~/.isce/SConfigISCE`
```
PRJ_SCONS_BUILD=/home/scott/Software/isce-2.0.0/build
PRJ_SCONS_INSTALL=/usr/local/isce-2.0.0

LIBPATH=/usr/lib/x86_64-linux-gnu
FORTRANPATH=/usr/include
CPPPATH=/home/scott/miniconda3/envs/isce/include/python3.4m

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
cd /home/scott/Software/isce-2.0.0
export PYTHONPATH=/home/scott/Software/isce-2.0.0/configuration
export SCONS_CONFIG_DIR=/home/scott/.isce

source activate scons
scons install
```

5) Create an alias in `.bashrc` to activate Python3 whenever you want to run isce
`alias start_isce="source activate isce; source ~/.isce/.isceenv"`
Where `.isceenv` contains:
```
export ISCE_HOME=/usr/local/isce
export PATH=$ISCE_HOME/bin:$ISCE_HOME/applications:$PATH
export PYTHONPATH=/usr/local:$ISCE_HOME/applications:$ISCE_HOME/component
```

6) To Run ISCE:
```
alias start_isce="source activate isce; source ~/.isce/.isceenv"
insarApp.py --steps
```


## Installing multiple versions / development snapshots


1) Change the SConfigISCE file
```
cp ~/.isce/SConfigISCE ~/.isce/SConfigISCE_2.0.0
vi ~/.isce/SConfigISCE
PRJ_SCONS_BUILD=/home/scott/Software/isce-2.0.0_201506/build
PRJ_SCONS_INSTALL=/usr/local/isce-2.0.0_201506
```


2) Install new version
```
su 
cd /home/scott/Software/isce-2.0.0_201506
export PYTHONPATH=/home/scott/Software/isce-2.0.0_201506/configuration
export SCONS_CONFIG_DIR=/home/scott/.isce

source activate scons
scons install
```


3) Change link for whichever version you want to run
*NOTE* that `/usr/local/isce` is a soft link to `/usr/local/isce-2.0.0`, so if you want to run a different version of isce, install the same way as above, but change the link to reflect the most recent version:

`sudo ln -s /usr/local/isce-2.0.0_201506 /usr/local/isce`






