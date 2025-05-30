# Image Color Quantization with K-Means Clustering

This project provides a graphical interface to perform **color quantization** on images using **MiniBatch K-Means clustering**. It allows users to reduce the number of colors in an image, making it simpler and more stylized while retaining the visual structure.

## Features

- Load and display images (JPEG, PNG, BMP, TIFF).
- Select the number of colors for quantization.
- Use multiprocessing for efficient computation.
- Preview original and quantized images.
- Save the quantized image to disk.

---

## Demo


| <img src="images/image4.jpg" alt="Original Image" width="300" /> | <img src="images/Q1.jpg" alt="Original Image" width="300" /> | <img src="images/Q16.jpg" alt="Original Image" width="300" />| <img src="images/Q64.jpg" alt="Original Image" width="300" /> |
|-----------------------|-----------------------------|---------------------------|---------------------------|
| Original Image | k=1 Image | k=16 Image | k=64 Image |  

k = no.of colors

---

## Requirements

- Python 3.7+
- Required packages:

```bash
pip install numpy scikit-learn pillow
````

---

## How It Works

1. The image is loaded and converted into an array of RGB pixels.
2. The pixel data is clustered using MiniBatch K-Means to find dominant colors.
3. Each pixel is replaced with its cluster's centroid color.
4. The quantized image is reconstructed and displayed.
5. Multiprocessing is used to handle large images efficiently.

---

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/JV-Vigneesh/Image-Color-Quantization-with-K-Means-Clustering.git
cd image-kmeans-quantizer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install numpy scikit-learn pillow
```

### 3. Run the Application

```bash
python main.py
```

---

## Notes

* The clustering is done using `MiniBatchKMeans` from `scikit-learn` for performance.
* Processing is parallelized across all CPU cores using the `multiprocessing` module.
* GUI built using `tkinter`, standard in Python.

---

## License

This project is licensed under the MIT License.

---
