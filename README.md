# RaceResultConverter

This grabs results from StartLineTiming and formats them for UltraSignUp. 

To install requirements:

```
# Create a Python virtual environment
$ python3 -m venv env

# Activate the virtual environment
$ source env/bin/activate

# Install requirements
$ pip install -r requirements.txt
```

With the requirements installed and the virtual environment activated, you can run the script with:
```
$ python convert.py
Enter the StartLineTiming URL: https://startlinetiming.com/en/races/2022/survival/event/35K
```

Some manual data cleanup may still be required before it can be successfully uploaded to UltraSignUp, as their system is **picky**. 