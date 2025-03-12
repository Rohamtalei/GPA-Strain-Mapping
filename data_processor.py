import numpy as np
import hyperspy.api as hs
from tkinter import filedialog
from scipy.ndimage import gaussian_filter
from numpy.fft import fft2, fftshift

class DataProcessor:


    @staticmethod
    def load_haadf_image():
        file_path = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[
                ("Supported files", "*.emd *.dm3 *.dm4 *.tiff *.tif *.h5 *.hdf"),
                ("EMD files", "*.emd"),
                ("DM3 files", "*.dm3"),
                ("DM4 files", "*.dm4"),
                ("TIFF files", "*.tiff *.tif"),
                ("HDF5 files", "*.h5 *.hdf"),
                ("All files", "*.*")
            ]
        )

        if not file_path:
            raise FileNotFoundError("No file selected.")

        try:
            print(f"Loading file: {file_path}")
            data_obj = hs.load(file_path, lazy=False)  

            if hasattr(data_obj, 'data'):
                data = data_obj.data
            else:
                data = np.array(data_obj)

            if data.ndim == 3:
                data = np.sum(data, axis=0)

            if data.ndim > 2:
                data = np.mean(data, axis=-1)

            if data.dtype.names is not None:
                data = data.view(np.uint8).reshape(data.shape + (-1,))
                data = np.mean(data[:, :, :3], axis=-1)

            return data.astype(float)

        except Exception as e:
            raise RuntimeError(f"Error loading file: {e}")

    @staticmethod
    def preprocess_data(data, threshold_percent=0):
        smoothed_data = gaussian_filter(data, sigma=0)
        threshold_value = np.percentile(smoothed_data, threshold_percent)
        material_mask = smoothed_data > threshold_value
        return smoothed_data, material_mask

    @staticmethod
    def compute_fft_and_contrast(smoothed_data):
        fft_data = fftshift(fft2(smoothed_data))
        fft_magnitude = abs(fft_data)
        return fft_data, fft_magnitude
