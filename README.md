# DeepFake Detection  

## Table of Contents  
- Introduction  
- Demo  
- Impact of DeepFakes  
- Project Objectives  
- Project Pipeline  
  - Pre-processing Workflow  
  - Prediction Workflow  
- Models and Architectures  
- Deployment  
  - Running the Code  
- Technologies Used  
- Conclusion  
- Team  

---

## Introduction  
DeepFakes are manipulated images or videos where one person’s likeness is replaced with another’s, often through advanced *face swapping*. This technique is commonly powered by *Generative Adversarial Networks (GANs)*, which are becoming increasingly sophisticated.  

---

## Impact of DeepFakes  
- Can be exploited to spread misinformation, fake news, or political propaganda.  
- May be used for fraudulent purposes, including financial scams.  
- Can cause psychological stress and social unrest by fueling false rumors.  
- Industries such as film, media platforms, and content providers are actively working to counter misuse of this technology.  

---

## Project Objectives  
The ability to detect DeepFakes is essential to reduce harmful misuse of AI.  

Our goals:  
- Build a model that can classify a given video as **REAL** or **FAKE**.  
- Provide a solution that could be integrated into social media platforms to warn users when they upload potentially manipulated content.  

**Main Goal:**  
To design a deep learning system capable of identifying subtle artifacts in video frames that distinguish authentic footage from DeepFakes.  

---

## Project Pipeline  

| Step | Description |
| --- | --- |
| 1 | Load the dataset |
| 2 | Extract videos |
| 3 | Split videos into frames (both real & fake) |
| 4 | Detect faces within frames |
| 5 | Locate facial landmarks |
| 6 | Perform frame-by-frame analysis of landmark changes |
| 7 | Classify each video as REAL or FAKE |

### Pre-processing Workflow  
![image](https://user-images.githubusercontent.com/77656115/206968030-1e9729e7-8d34-4295-a110-d05ad0ade7bb.png)  

### Prediction Workflow  
![image](https://user-images.githubusercontent.com/77656115/206968272-73db6238-79a0-46a1-ad5b-e651ad002322.png)  

---

## Models and Architectures  

### CNN-based Models  
- **MesoNet** – Designed for image-level DeepFake detection, but struggles on full video sequences.  
- **ResNet50v** – Trained on cropped DeepFake frames using pretrained ImageNet weights.  
- **EfficientNetB0** – Also trained on cropped frames with pretrained ImageNet weights.  

### CNN + Sequential Models  

**InceptionV3 + GRU**  
- Combines CNN feature extraction with sequential learning.  
- Achieves around **82% test accuracy**.  
- Each video frame is converted into feature vectors, then passed to GRU for classification.  
- Uses Adam optimizer, accuracy as the metric, and `sparse_categorical_crossentropy` loss.  
- Accuracy improves with more epochs.  
- **Limitation:** performs poorly on videos containing multiple faces per frame.  

**EfficientNetB2 + GRU**  
- Another hybrid CNN + sequential approach with better performance.  
- Reaches about **85% test accuracy**.  
- Uses the same optimization setup as above.  
- **Limitation:** struggles on frames with dark or low-light backgrounds.  

---

## Deployment & Running the Code  

This project uses a hybrid CNN + RNN model that achieved **~85% test accuracy** on a subset of the DFDC dataset.  

1. Install the dependencies:  
```bash
pip install -r requirements.txt
```

**Run main.py file in deploy folder**
```bash
  python main.py
```
## Conclusion:

- In this project, we have implemented a method for the detection of Deep-Fake videos using the 
combination of CNN and RNN architecture. We have kept our focus on Face-Swapped Deep-Fake 
videos.

- We primarily experimented only with various pre-trained CNN models like EfficientNet, and 
ResNet by finding the probability of each video frame being fake and predicting the output based on an aggregate of these probabilities. But the results weren’t satisfactory, so we went forward by combining CNN and RNN models.

- For the CNN + RNN model, the features of face-cropped video frames are extracted using pretrained CNN models and it is passed onto the RNN model which classifies the video as REAL or 
FAKE. We Experimented with EfficientNet and inception net for the feature extraction part and 
GRU is used to make the classification. We have obtained a maximum Test Accuracy of ~85% 
using this approach. Our model has high precision for FAKE videos which is obtained by giving 
more FAKE videos during the training of the Model.

## Team : 
1. Darwin https://github.com/DarwinJohan 
2. Virly https://github.com/HinaKhina 
3. Kevin https://github.com/RaidToaster


