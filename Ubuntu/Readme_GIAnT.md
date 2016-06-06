# Notes on installing CalTechs Earthdef on Ubuntu 14
## (GIAnT, PyAps, Varres)
http://earthdef.caltech.edu

## Register for an account (you will be asked for a password to download with svn)
http://earthdef.caltech.edu/account/register

## Download software
```
cd ~/Software/earthdef
svn co http://earthdef.caltech.edu/svn/giant
svn co http://earthdef.caltech.edu/svn/varres
svn co http://earthdef.caltech.edu/svn/pyaps
```

## Create a Python Environment with necessary dependencies
Some packages need to be downloaded from a non-default repository, so you have to first register it in a `~/.condarc` file:
```
channels:
- defaults
- https://conda.anaconda.org/conda-forge
```
Then run:
```
conda env create -f giant.yml
```

## Create an alias for initializing environment variables and correct python 
```
alias start_giant="source ~/.giant/.giantenv; source activate giant"
```
where `~/.giant/.giantenv` contains:
```
export GIANT=~/Software/earthdef/giant/GIAnT
export PYAPS=~/Software/earthdef
export VARRES=~/Software/earthdef/varres
export PYTHONPATH=$GIANT:$PYAPS:$VARRES
export PATH=~/Software/earthdef/giant/GIAnT/SCR:$PATH
``` 
