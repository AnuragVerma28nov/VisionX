# DEPLOYMENT

## Local Deployment

### 1. Clone Repository

```bash
git clone <repository-url>
cd Real-Time-Object-Detection
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Application

**Webcam Detection:**

```bash
python src/main.py --mode webcam
```

**Image Detection:**

```bash
python src/main.py --mode image --source input/images/test.jpg
```

**Video Detection:**

```bash
python src/main.py --mode video --source input/videos/test.mp4
```

## Future Deployment

- Docker support
- Streamlit web application
- Cloud deployment
- GPU acceleration
