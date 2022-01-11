# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 09:03:37 2022

@author: Scott Greenwood
"""

from fmpy import simulate_fmu
import pandas as pd  
import sys 
import re

def simulateFMU(inputFileName,outputFileName):
    '''
    Read an input file of a specific format, update setting values, simulate the FMU, and output results.

    *Note* - Current flexibility, i.e., for time depedent inputs is not handled but could be by modifying/expanding
    this file or perhaps creating a RAVEN interface specifically for pyfmi or, preferably, the FMI standard.

    inputFileName = 'referenceInput.txt' (default)
    outputFileName = 'results.csv' (default)

    Format of inputFileName:
    Requires -
    1) the location and name of the FMU     <--- Only one, must be the first line
    2) variables to be set by RAVEN         <--- May include any number
    3) and variables to be output to RAVEN     <--- May include any number

    Example:
    fmuName = 'PATHTOFMU/myFMU.fmu' <--- Must be the first line!!!
    sigma = $RAVEN-sigma$
    rho = $RAVEN-rho$
    lorenzSystem.x
    lorenzSystem.y
    '''
    
    # Read the input file
    with open(inputFileName,'r') as f:
        lines = f.readlines() 
    
    # Extract file name of FMU
    if "fmuName" in lines[0]:
        fmuName = ''.join(re.findall("'([^']*')", lines[0])).replace("'","")
    else:
        raise ValueError('fmuName must be specified in first line of input file. Found instead:\n',lines[0])

    # Initialize inputs/outputs
    start_time = None
    stop_time = None
    output_interval = None
    
    start_values = {}
    output = []
    for i, line in enumerate(lines):
        if i == 0:
            # Skip first line which contains fmuName
            pass
        elif '=' in line:
            # Set the new model parameters
            key, value = line.replace(' ','').strip().split('=')
            if key == 'start_time':
                start_time = float(value)
            elif key == 'stop_time':
                stop_time = float(value)
            elif key == 'output_interval':
                output_interval = float(value)
            else:
                start_values[key] = float(value)
        else:
            # Generate key for variable to be saved
            key = line.replace(' ','').strip()
            output.append(key)
            
    # If empty set to None to return default output variables
    if len(output) == 0: output = None
    
    # Simulate
    results = simulate_fmu(fmuName,start_time=start_time,stop_time=stop_time,output_interval=output_interval,start_values=start_values,output=output)

    # Save results to csv (column - variable, row - values)
    pd.DataFrame(results).to_csv(outputFileName, index=False)
    
if __name__ == '__main__':

    # Check for number of arguments provided by raven and define appropriate file name
    if len(sys.argv) == 1:
        inputFileName = "referenceInput.txt"
    else:
        inputFileName = sys.argv[1]
        
    if len(sys.argv) < 3:
        outputFileName = "results.csv"
    else:
        outputFileName = sys.argv[2]

    if outputFileName.endswith(".csv"):
        outputFileName = outputFileName
    else:
        outputFileName = outputFileName + ".csv"

    # Run the FMU and create the output file
    simulateFMU(inputFileName,outputFileName)

    