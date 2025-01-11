![MOVIESTREAMZ Logo](https://github.com/user-attachments/assets/225fba2f-ef5f-46a1-a1ab-028cff07b54a)

MOVIESTREAMZ is a video streaming platform designed to provide users with a seamless and high-quality video streaming experience. This project leverages advanced video compression algorithms, modern technologies, and robust frameworks to deliver efficient video content while ensuring minimal storage and bandwidth requirements.

---

## Features

- **Video Uploading**: Easily upload video content.
- **Video Encoding and Compression**: Uses advanced algorithms like Per-Title Encoding and Iterative CRF Encoding.
- **Efficient Streaming**: Powered by H.265 encoding and HLS (HTTP Live Streaming).
- **Payment Integration**: Supports Khalti/Esewa for payment processing.
- **Scalable Backend**: Built with Django and PostgreSQL for robust database management.
- **Background Processing**: Celery handles video encoding and processing tasks efficiently.

---

## Project Overview

### Key Objectives

- Provide a seamless video streaming experience.
- Optimize video compression for fast loading times.
- Minimize bandwidth and storage requirements.

### Technologies Used

- **Backend**: Django Web Framework
- **Database**: PostgreSQL
- **Task Queue**: Celery with Redis as the message broker
- **Video Encoding**: H.265, Per-Title Encoding, Iterative CRF Encoding
- **Frontend**: Mobile-unfriendly, intuitive, and desktop focused interface

---

## Setup and Installation

Follow these steps to set up the MOVIESTREAMZ project on your local machine:

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Redis Server
- Virtual Environment (optional but recommended)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/833M0L3/moviestreamz.git
   cd moviestreamz
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the root directory with the following content:
   ```env
   DB_NAME=postgres
   DB_USER=admin
   DB_PASSWORD=admin
   DB_HOST=192-168-1-108
   DB_PORT=5432

   DEBUG=True
   SECRET_KEY=my_very_secure_secret_key
   ALLOWED_HOSTS=*

   CELERY_BROKER_URL=redis://192-168-1-108:6379
   CELERY_RESULT_BACKEND=redis://192-168-1-108:6379
   CELERY_ACCEPT_CONTENT=application/json
   CELERY_TASK_SERIALIZER=json
   CELERY_RESULT_SERIALIZER=json
   CELERY_TIMEZONE=Asia/Kathmandu
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the Server**
   ```bash
   python manage.py runserver
   ```

7. **Start Celery Worker**
   ```bash
   celery -A moviestreamz worker --loglevel=info
   ```

8. **Visit the Application**
   Open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

### Screenshots
![image](https://github.com/user-attachments/assets/628d0a9d-2509-40bd-b21a-be8f33a3069b)
![image](https://github.com/user-attachments/assets/93893dca-2efe-44ad-b92b-a22cd588efac)
![image](https://github.com/user-attachments/assets/61b8497a-b04f-43d9-8413-261dbb824c36)
![image](https://github.com/user-attachments/assets/4288709d-9553-479b-94fe-d1fb561dd25c)
![image](https://github.com/user-attachments/assets/942a3727-3b3d-4750-9ae8-e9e9f3b1ec4d)
![image](https://github.com/user-attachments/assets/eb4585b0-7670-46cc-a7b4-0aa98288ef5f)


### References
- [Automating CRF Optimization: Smarter Video Compression with VMAF, PSNR, and SSIM](https://www.linkedin.com/pulse/automating-crf-optimization-smarter-video-compression-zaki-ahmed-fjdqf/)
- [Per-Title Encode Optimization](https://netflixtechblog.com/per-title-encode-optimization-7e99442b62a2)
- [Benchmarking Learning-based Bitrate Ladder Prediction Methods for Adaptive Video Streaming](https://hal.science/hal-04407094/document)
- [Django Video Encoding and Streaming App](https://github.com/mahmudtopu3/django-tube)
- [Khalti Payment Docs](https://docs.khalti.com/khalti-epayment/)
- [Esewa Payment Docks](https://developer.esewa.com.np/pages/Epay#transactionflow)
- [Building Progress Bars for the Web with Django and Celery](https://www.saaspegasus.com/guides/django-celery-progress-bars/)



