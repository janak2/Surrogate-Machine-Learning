The repo is structured as following:

1. src/curve_fit
   a. We use laboratory data about voltage and current and then use a basic equation to fit the curve.

2. src/pybamm_code
   a. We use laboratory data and then use the pybamm package to estimate some of the parameters of the model.

3. src/pytorch
   a. We generate synthetic data using a basic equation.
   b. The pytorch models require two files to run output.csv and input.csv.
   c. input.csv file can be found here: https://drive.google.com/file/d/1-G707IBaEpxw_LROVk_1n-oS7z1xaJci/view?usp=share_link
