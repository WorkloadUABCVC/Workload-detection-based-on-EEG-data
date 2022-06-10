# Mental Workload Detection Based on Electroencephalograms

![Alt text](figs/voluntary.png?raw=true "A voluntary facing a test")

## Summary

We provide some code to create the input data for training **Mental Workload detectors** based en **Electroencephalogram** (EEG) signals.


## Requirements

* Dataset: From the ["Dataset to predict mental workload based on physiological data"](https://doi.org/10.5565/ddd.uab.cat/259591),  download the EEG  data from the N-back test or the Heat-The-Chair game.



* Python 3, Pandas, Pyarrow, and other minors.

## Preparation

* In the root of your project, make sure to create two folders: /data and /input_features. 
```
   ~/    
      /data/     
      /input_features/
```   

* Put the donwloaded dataset in /data.
* At the end,  the generated input data for your model will be located in /input_features

## Running the code

1. **Select different options** of data preparation by editing directly the file.
```
   eeg_config.py   
```

  The options you can change are: the **dataset**,  the **window_size**, the **window_overlapping**, and the **filtering method**.
  
2. Next, **run** the script
```
   python main_create_input_data.py
```

## Further information

You can visit the web of our [Research Group](http://iam.cvc.uab.es/).



