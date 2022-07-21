
## CABARET
<img src="https://github.com/adelval1/pyCabaret/blob/master/logo.png" width="620" height="450" /> 

## Installation and requirements ##

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

The python wrapper for the Mutation++ library can be found on https://github.com/mutationpp/Mutationpp

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