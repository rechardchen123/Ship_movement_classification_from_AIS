# Ship movement classification from AIS
___
This is an repository for the paper named 'a novel ship movement classification from AIS data based on convolutional neural network'.
___
## Summary
This is the code repository for the paper entitled 'A novel ship movement classification from Automatic Identification System (AIS) data based on convolutional neural network', published to Ocean Engineering. 

If you are interested in this work and use the materials, please cite the paper.

The abstract is as follows: "In order to realise the maritime autonomy for the unmanned ships, it needs a lot of data to train. With the wide usage of AIS data in the maritime, the demand for the algorithms to efficiently classify the ship's AIS data into different movement types (static, normal navigation and manoeuvring) is increasing sharply. There are lots of studies based on the hand-crafted features and cannot effectively extract the details of the ship movement information. At the same time, the ship movement in water area is a free space movement and it cannot migrate algorithms that extract the vehicles' movement information in the road transportation into the maritime transportation. In this research, a novel method called CNN-SMMC (Convolutional Neural Network-Ship Movement Modes Classification) is proposed to address the issue. In order to make full advantage of CNN's ability to extract the images, a method called Ship Movement Image Generation and Labelling (SMIGL) algorithm is proposed to map the AIS trajectory into the trajectory images which they contains the ship's movement characteristics such as changing rate of speed and changing rate of courses. The CNN-SMMC models are constructed to classify the ship trajectory images. A variety of experiment for configuration the CNN layers are evaluated and the highest accuracy in the test dataset around 77\% are selected. In this research, the comparison of the CNN-SMMC with other machine learning algorithms demonstrate the advantage of the CNN-SMMC."

The dataset uses in this project is available at: https://drive.google.com/open?id=1IW4D4ISWlH-b4zq9_nOcqtGhnDCK5ncA 

___
### Code Repository
All the describled data processing and CNN frameworks are implemented with Python programming using Tensorflow for deep learning modesl and the classical machine learning algorithms use the Sklearn package. All experiments run on the UCL cluster. 
"The authors acknowledge the use of the UCL Myriad High Throughput Computing Facility (Myriad@UCL), and associated support services, in the completion of this work."
I divide the codes in two categories:
1. Ship Movement Image Generation and labelling. It contains the processing the raw AIS data in the subfolder '1.Process_ais_data' which includes 5 steps. The '2.Generate_image_labelling' is to generate the movement images from the AIS raw data and related movement labels (static, manoeuvring and normal navigation).
2. Training and Testing CNN. The convolutional neural network implements in the 'train_scratch.py' and the file named 'preprocess_data.py' is the prelimarly process for the data before sending into the CNN. The rest file 'classical_ML.py' is implemented by the Sklearn paackage for the KNN, SVM and DT.
___
### Contact Information 
Please email me at xiang.chen.17@ucl.ac.uk if you have any questions about the paper and the codes. 