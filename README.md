# Ship movement classification from AIS
___
This is an repository for the paper named 'a novel ship movement classification from AIS data based on convolutional neural network'.
___
## Summary
This is the code repository for the paper entitled 'A novel ship movement classification from Automatic Identification System (AIS) data based on convolutional neural network', published to Ocean Engineering. 

If you are interested in this work and use the materials, please cite the paper.

The abstract is as follows: "With a wide usage of AIS data in maritime industry, the demand for the algorithms to efficiently classify the ship’s AIS data into different movements (static, normal navigation and manoeuvring) is increasing sharply. There are lots of studies based on the manual labeled features not to effectively extract the details of the ship movement information. On the other side, the ship movement is in a free space compared with vehicle’s movement in the road grids and it cannot easily migrate the classification methods in road transportation into the maritime area. To deal with this problem, a Convolutional Neural Network-Ship Movement Modes Classification (CNN-SMMC) algorithm is proposed. The main idea of this method is to use a neural network to learn from the labeled AIS data and then the rest of unlabeled AIS data is classified by the well-trained neural network. Firstly, the Ship Movement Image Generation and Labelling (SMIGL) algorithm is designed to transfer the ship’s AIS trajectories into different movement images which contain the ship’s movement characteristics such as changing rate of speed and changing rate of courses to make full use of the CNN’s ability of extracting images. Meanwhile, the CNN-SMMC architecture is built with a series of functional layers (convolutional layer, max-pooling layer, dense layer etc.) and seven experiments for CNN-SMMC are designed to find the optimal parameters. Moreover, considering the imbalanced AIS data, three metrics (average accuracy, F1 score and Area Under Curve (AUC)) are chosen to evaluate the CNN-SMMC. Finally, the classification algorithms (K-Nearest Neighbors (KNN), Support Vector Machine (SVM) and Decision Tree (DT)) are selected to compare with the CNN-SMMC. The results demonstrate that the proposed CNN-SMMC has a better performance to classify the AIS data."

The dataset uses in this project is available at: https://drive.google.com/open?id=1IW4D4ISWlH-b4zq9_nOcqtGhnDCK5ncA 

___
### Code Repository
All the describled data processing and CNN frameworks are implemented with Python programming using Tensorflow for deep learning modesl and the classical machine learning algorithms use the Sklearn package. All experiments run on the UCL Myriad cluster. 

I divide the codes in two categories:
1. Ship Movement Image Generation and labelling. It contains the processing the raw AIS data in the subfolder '1.Process_ais_data' which includes 5 steps. The '2.Generate_image_labelling' is to generate the movement images from the AIS raw data and related movement labels (static, manoeuvring and normal navigation).
2. Training and Testing CNN. The convolutional neural network implements in the 'train_scratch.py' and the file named 'preprocess_data.py' is the prelimarly process for the data before sending into the CNN. The rest file 'classical_ML.py' is implemented by the Sklearn paackage for the KNN, SVM and DT.

___
### Contact Information 
Please email me at xiang.chen.17@ucl.ac.uk if you have any questions about the paper and the codes. 

___
### Acknowledgement 

"The authors acknowledge the use of the UCL Myriad High Throughput Computing Facility (Myriad@UCL), and associated support services, in the completion of this work."
