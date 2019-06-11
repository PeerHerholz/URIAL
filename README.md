&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/PeerHerholz/URIAL/blob/master/img/URIAL_logo.png"
     alt="URIAL logo"
     height="250"
     style="float: center; margin-right: 10px;"/>

[![GitHub issues](https://img.shields.io/github/issues/PeerHerholz/URIAL.svg)](https://github.com/PeerHerholz/URIAL/issues/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/PeerHerholz/URIAL.svg)](https://github.com/PeerHerholz/URIAL/pulls/)
[![GitHub contributors](https://img.shields.io/github/contributors/PeerHerholz/URIAL.svg)](https://GitHub.com/PeerHerholz/URIAL/graphs/contributors/)
[![GitHub Commits](https://github-basic-badges.herokuapp.com/commits/PeerHerholz/URIAL.svg)](https://github.com/PeerHerholz/URIAL/commits/master)
[![GitHub size](https://github-size-badge.herokuapp.com/PeerHerholz/URIAL.svg)](https://github.com/PeerHerholz/URIAL/archive/master.zip)
[![GitHub HitCount](http://hits.dwyl.io/PeerHerholz/URIAL.svg)](http://hits.dwyl.io/PeerHerholz/URIAL)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)



## Description
URIAL is a toolbox (and hopefully soon BIDS app) for [representational similarity analysis](https://doi.org/10.3389/neuro.06.004.2008) in python. In more detail, it includes functions for computing, plotting and comparing Representational Dissimilarity Matrices (RDMs). It's based on the famous [matlab toolbox](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003553) ([github repo](https://github.com/rsagroup/rsatoolbox)), extending it with a variety of utility functions like the conversion from MATLAB (e.g., .mat) to open file types (e.g., .csv) and customizable graphics for both RDMs and MDS, as well as correlation of RDMs across trials. It heavily utilizes the following python libraries: [pandas](https://pandas.pydata.org/), [pingouin](https://github.com/raphaelvallat/pingouin), [scikit-learn](https://scikit-learn.org/), [nilearn](http://nilearn.github.io/index.html), [nistats](https://nistats.github.io/) & [MNE](https://martinos.org/mne/stable/index.html).  

## Overview of functionality

As mentioned above, URIAL's is divided into three sections that include respective functions:

### Computing

- computation of RDMs from neuroimaging data, including fMRI (within ROIs) & EEG (across time)
- generate conceptual model RDMs

### Comparing RDMs

- rank correlation based model comparisons between RDMs and model RDMs
- correlation between RDMs within a certain modality
- RDM based spatio-temporal searchlights in fMRI & EEG

### Plotting

- RDMs as matrices, dendograms and via MDS
- model comparison results
- stability and correlation of RDMs across trials



## Documentation
A documentation is currently in the works and will be available soon. Sorry for any inconvenience this might cause.   

## How to report errors
Running into any bugs :beetle:? Check out the [open issues](https://github.com/PeerHerholz/URIAL/issues) to see if we're already working on it. If not, open up a new issue and we will check it out when we can!

## How to contribute
Thank you for considering contributing to our project! Before getting involved, please review our [Code of Conduct](https://github.com/PeerHerholz/URIAL/blob/master/CODE_OF_CONDUCT.md). Next, you can review  [open issues](https://github.com/PeerHerholz/URIAL/issues) that we are looking for help with. If you submit a new pull request please be as detailed as possible in your comments. Please also have a look at our [contribution guidelines](https://github.com/PeerHerholz/URIAL/blob/master/CONTRIBUTING.md).

### Acknowledgements
If you intend to or already used ANSL, we would be very happy if you cite this github repo, till we have "something" out there!
