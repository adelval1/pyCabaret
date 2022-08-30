
## CABARET
<img src="https://github.com/adelval1/pyCabaret/blob/master/logo.png" width="620" height="450" /> 

## Installation and requirements ##

CABARET works hand in hand with the Mutation++ library https://github.com/mutationpp/Mutationpp. For CABARET to work, you need to make sure several things work with Mutation++. 

* First, download and install Mutation++ from the link above. 
* Subsequently, add this snippet of code to the file "Mutationpp/interface/python/src/pyMixture.cpp"
```
.def("mixtureSMass",
           static_cast<double (Mutation::Mixture::*)(void) const>(
               &Mutation::Mixture::mixtureSMass),
           "Returns the mixture averaged entropy in J/kg-K.")
```
* Type in the terminal in the build directory inside your Mutationpp folder
```
ccmake ..
```
and turn BUILD_PYTHON_WRAPPER from OFF to ON.

* Compile Mutation++.

Once Mutation++ is installed, you need to get a local python module built in order to use it in Python. From your Mutationpp directory

* To compile the wrapper you need [pybind11](https://github.com/pybind/pybind11) in `thirdparty/pybind11`:

 ```
 git submodule add -b stable ../../pybind/pybind11 thirdparty/pybind11
 git submodule update --init
 ```

* and  [scikit-build](https://scikit-build.readthedocs.io/en/latest/installation.html#install-package-with-pip) (use pip or pip3 depending on your local installation):

 ```
 pip install scikit-build
 ```

* We will use the file `setup.py` automatically provided with Mutation++ in order to generate the package (use python or python3 depending on your local installation):

 ```
 python3 setup.py build
 ```

The procedure might take some minutes to complete. The built package is in `_skbuild/[your_distribution]/cmake-install/interface/python/mutationpp` (NOTE:  `your_distribution` varies with the OS you are using, e.g. `macosx-12.0-arm64-3.9`, `linux-x86_64-3.7` and the architecture used e.g. `macosx-12.0-x86_64-3.9`: be sure you check the name of the folder automatically generated in  `_skbuild/`); now you only need to

* Define a system variable in the right file for you (`.bashrc`, `.zprofile`, `.bash_profile`, `.zshrc`).
```
export MPP_LOCALPY=$MPP_DIRECTORY/_skbuild/[your_distribution]/cmake-install/interface/python/mutationpp
```
* Close the terminal or `source` the right file (`.bashrc`, `.zprofile`, `.bash_profile`, `.zshrc`).

Your local Mutation++ Python module is now readily accessible by CABARET.

To install CABARET just do in your terminal in the directory of your choice

```
git clone https://github.com/adelval1/pyCabaret.git
```

CABARET uses the following package versions

```
python 3.9.1
numpy 1.20.1
scipy 1.8.0
```

To run CABARET just specify the options you want in the input.in file and do in the /src folder

```
python cabaret.py
```

where python is your python installation.

For help on understanding the input file you can go to /docs/explanatory_input.in. To check out a comprehensive example you can go to /examples and run the jupyter notebook.

## CABARET applications ##
The theoretical aspects of the modules included in CABARET can be found in the following conference paper:

* del Val, A., Magin, T.E., Dias, B. and Chazot, O., 2015. Characterization of ground testing conditions in high enthalpy and plasma wind tunnels for aerospace missions. In 8th European Symposium on Aerothermodynamics for Space Vehicles, Lisbon, Portugal (Vol. 107, p. 171).

If used, CABARET should be cited as:

**Bibtex**
```bibtex
@inproceedings{cabaret,
  title={Characterization of ground testing conditions in high enthalpy and plasma wind tunnels for aerospace missions},
  author={del Val, A. and Magin, Thierry E and Dias, Bruno and Chazot, Olivier},
  booktile={8th European Symposium on Aerothermodynamics for Space Vehicles, Lisbon, Portugal, 2015}

}
```