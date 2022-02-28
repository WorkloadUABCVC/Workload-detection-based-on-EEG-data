# Workload-Detection-Based-on-EEG


## Summary

We provide a script code to create input data for training **Mental Workload detectors** based en **Electroencephalogram** (EEG) signals.


## Requirements

* Dataset: From the [Epilots Dataset repository](http://iam.cvc.uab.es/portfolio/e-pilots-dataset/), download the dataset [Serious Games Dataset] (http://iam.cvc.uab.es/data-from-serious-games/).
* Python 3, Pandas with pluging Pyarrow, and other minors.

## Preparation

* In the root of your project, create make sure to creat two folders: /data and /input_features, then your data directories will be:
```
   ~/    
      /data/     
      /input_features/
```   

* Put the donwloades dataset in /data.
* After running the main script, data generated will be in /input_features

## Running the code

1. **Change the options** of data preparation by editing directly the file.
```
   eeg_config.py   
```
  Here, for example, the name of the **dataset to be processed**,  the **window size**, the **window overlapping**, the **filtering method**, etc.
  
2. Next, run the script
```
   main_create_input_data.py
```

