# CCTV Fire and Smoke Detection

A Streamlit application for real-time detection of fire and smoke using YOLO models. The application supports image/video uploads, webcam monitoring, and screen capturing. Alerts can be sent via Telegram.

## Features

- **Upload Photo/Video:** Detect fire and smoke in uploaded media files.
- **Webcam Realtime Detection:** Monitor live webcam feed for fire and smoke.
- **Screen Monitoring:** Detect fire and smoke on the screen in real-time.
- **Telegram Alerts:** Receive notifications when fire or smoke is detected.

## Setup Instructions (To Train the Model)

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/LightRemedy/ICT304.git CCTV_detection
   cd CCTV_detection
   ```

2. **Download the Dataset:**
   ```bash
   This is a modified shortened version of the dataset from Middle East Tech University.
   Download the dataset from [here](https://murdochuniversity-my.sharepoint.com/:f:/r/personal/34944909_student_murdoch_edu_au/Documents/ICT304%20AI%20System%20Design/ICT304-PT%20GRP4%20Assignment%202%20Dataset/Dataset?csf=1&web=1&e=pVIoj8)
   Put into the HomeShield folder.
   It should look like this:
   HomeShield
   ├── dataset
   │   ├── train
   │   │   ├── images
   │   │   └── labels
   │   ├── valid
   │   ├── test
   Credits to https://universe.roboflow.com/middle-east-tech-university/fire-and-smoke-detection-hiwia for the full dataset.
   ```
   

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the Model:**
   ```bash
   python train.py
   ```
- **The Data.yaml file is automatically generated when the model started training.**

5. **The model will be saved in the HomeShield folder.**
- **This is where the model weights are saved.**
- **HomeShield/runs/detect/HomeShield/weights/best.pt**


### Setup Instructions (To Run the Application Locally)

1. **Run the Application:**
   ```bash
   streamlit run run.py
   ```

2. **The application will be running on localhost**

3. **You can test the application by uploading a photo/video, selecting the webcam option, or selecting the screen monitoring option.**

4. **You will be able to see the detections on the screen.**

5. **You will also be able to receive Telegram alerts when fire or smoke is detected.**


### Setup Instructions (To Run the Application Online)

1. **We will be using Streamlit Community Cloud to host the application online.**

2. **This is the link to the application:**
   ```bash
   https://share.streamlit.io/lightremedy/ict304/main/run.py
   ```

3 **The application will be hosted on streamlit community cloud.**

4. **You can test the application by uploading a photo/video, selecting the webcam option, or selecting the screen monitoring option.**

5. **You will be able to see the detections on the screen.**

6. **You will also be able to receive Telegram alerts when fire or smoke is detected.**
