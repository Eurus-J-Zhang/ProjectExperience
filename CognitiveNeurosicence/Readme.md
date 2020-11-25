This folder includes the scripts developed by me and my college Joonas Haakana during the summer intern in 2020 at the Brain and Mind Laboratory at Department of Neuroscience and Biomedical Engineering, Aalto University.
Our working content is to develop the scripts for 
1. Preprocessing the raw MEG data
   1. Creating epoched data structures
   2. Fliter data
   3. Computing ICA (Independent component analysis)
   4. Zero-padding bad trials and/or channels
2. Filter the preprocessed data to a specific bandpass
3. MCCA (Multiset Canonical Correlation Analysis)
   1. PCA Calculation (Principal component analysis)
   2. Calculate mcca
   3. Calculate pair-wise correlations between different subject pair combinations
   
The interesting part in this project is about the signal processing using methods like ICA, PCA and MCCA. 
* ICA is about separating a multivariate signal into subcomponents.
* PCA is about data dimensionality reduction, using the first few principal components to represent the whole data.
* MCCA is about defining the stucture in each variate, as well as the relationships among multiple sets of variables.

These methods can be quite informative for the data comprehension and processing.
