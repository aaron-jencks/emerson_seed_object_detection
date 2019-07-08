##Installation
You'll want the conda environment first, so run the following code, replacing the `...` with the absolute path to 
your github repo clone or the `labview_recorder` folder.

```powershell
cd "...\emerson_seed_object_detection\PyCharm\pmd_implementation\labview_recorder"
conda create --name test --file .\environment.yml
```

Then you can activate the new conda environment with `conda activate test`

##Running the code
###Automated Execution
To run the code, I've put the required commands into a simple `.bat` file that you can run straight out of the box.
All you have to do is run the `run_me.bat` file and it will take care of building the correct c files and doing its 
thing.

###Manual Execution
Alternatively, if you would like to know how it works, or you would like to run it manually, you can do the following

Navigate, in an anaconda prompt, either cmd, or powershell, to the folder where you extracted the `labview_recorder` or
the github repo.

```
cd "...\emerson_seed_object_detection\PyCharm\pmd_impelementation\labview_recorder"
```

if you are using a command prompt, anaconda prompt, then you need to add the `/d` option.

Then you need to run the setup script, this is a bit different than a normal python file, this builds the cython files
and converts them into python executable code.

```
python setup.py build_ext
```

Now you can run `main.py` like you normally would.

```
python main.py
```