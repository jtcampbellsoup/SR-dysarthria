This repository contains the code used to train the DBLSTM and LAS models for speech recognition. Here is the organization breakdown of this repository:

<b>DBLSTM_pics/</b> - pictures used for report and poster for DBLSTM model (CS 230)<br>
<b>LAS_pics/</b> - pictures used for report and poster for LAS model (CS 229)<br>
<b>get_goog_results.py</b> - uses the Google Cloud speech recognition toolkit to get a reference success rate of our test set with a commerical ASR system<br>
<b>FeautureViz.ipynb</b> - Runs through an example file in the data to demonstrate the feature processing<br>
<b>analyze_data_DBLSTM.ipynb</b> - (for CS 230 only) this reads in the transcriptions of the final DBLSTM model on the test set and breaks down and plots results by their phonemes<br>
<b>analyze_data_LAS.ipynb</b> - (for CS 229 only) this reads in the transcriptions of the final LAS model on the test set and breaks down and plots results by their phonemes<br>

<b>nab/</b> - directory that mostly contains starter code from Nabu speech recognition code base.<br>
<b>nab/Data/</b> - contains all the code used to process the data to break down words into phonemes, and to disperse audio files into their proper locations to be processed. nab/Data/SampleData/ has a few examples of audio files used to train the model and the corresponding feature vectors computed from the files.<br>
<b>nab/Results/</b> - contains the dev set results that were outputted by the specified model. The final models also contain the phoneme transcriptions and the test set results so we can investigate the results further. Final model also has the loss during training.<br>
<b>nab/config/recipes/DBLSTM</b> - (CS 230 only) the configuration files used for training the DBLSTM model. Specifies all the the details about the encoder and decoder and hyperparameters, etc.<br>
<b>nab/config/recipes/LAS</b> - (CS 229 only) the configuration files used for training the LAS model. Specifies all the the details about the encoder and decoder and hyperparameters, etc.<br>

Using Nabu speech recognition code base:
https://github.com/vrenkens/nabu


