
Strain Mapping GPA method
This project provides a graphical user interface (GUI) for strain mapping from high-angle annular dark-field (HAADF) images. It utilizes Fourier-based methods to compute phase images, displacement fields, and strain maps (expressed in percentage), as well as a line-scan tool to analyze specific regions of the maps.

Overview
The GUI allows users to:

Load HAADF Images: Supports various file formats such as EMD, DM3, DM4, TIFF, and HDF5.
Process Images: Performs image preprocessing using Gaussian filtering, computes FFTs, and extracts phase information.
Strain Calculation: Uses selected FFT spots (via interactive point selection) to compute displacement fields and strain components (Exx, Eyy, Exy) as well as local rotations.
Visualization: Displays original images, FFT magnitudes, phase images, strain maps, and complex image magnitudes.
Line Scan Analysis: Enables users to select a line on a strain map and plot the strain profile along that line.
Save Results: Saves the processed images and maps as high-resolution TIFF files.
Features
Interactive GUI: Built with Tkinter and Matplotlib, the application provides an interactive environment for parameter tuning and result visualization.
FFT-based Strain Mapping: Computes strain using Fourier transforms and phase unwrapping techniques.
Flexible Parameter Settings: Users can adjust the FFT circle centers, Gaussian filter widths, and threshold values, along with reference area selection for displacement correction.
Line Scan Capability: Easily generate a profile line scan from any of the strain maps.
Installation
Requirements
Python 3.x
NumPy
Matplotlib
SciPy
scikit-image
HyperSpy
Tkinter (usually included with Python)
Installing Dependencies
You can install the required Python packages using pip:

bash
Copy
pip install numpy matplotlib scipy scikit-image hyperspy
Make sure that your Matplotlib backend is set to "TkAgg" as specified in the code.

Usage
Run the Application:

Execute the script in your terminal or command prompt:

bash
Copy
python v745L-co-percent.py
Load an Image:

Click the "Load New Image" button to select a HAADF image file.
Supported file formats include *.emd, *.dm3, *.dm4, *.tiff, *.tif, *.h5, and *.hdf.
Select FFT Spots:

Click "Select Points" to open a new window displaying the FFT magnitude.
Double-click on the left image to select the first FFT spot and on the right image for the second FFT spot.
The selected coordinates are automatically populated into the GUI fields.
Adjust Parameters:

Modify the circle center coordinates, inner and outer radii for FFT filtering.
Set the reference area for displacement correction.
Adjust the smoothing sigma and mask threshold using the provided sliders.
Define the display range for strain maps (Exx and Eyy).
Process the Image:

Click "Apply" to process the image and update the visualizations.
The application computes the FFT, phase images, displacement fields, and strain maps.
Save Images:

Use the "Save" button to select a directory where the processed images will be saved as TIFF files.
Line Scan:

Click "Line Scan" to choose a strain map and perform a line-scan analysis.
Follow the prompts to select the map, line thickness, and then click two points on the image to define the line.
The line scan profile is then displayed in a new plot window.
Code Structure
Global Parameters:

COLORMAP, DEFAULT_THRESHOLD_PERCENTILE, DEFAULT_SIGMA_STRAIN_SMOOTH, and ROTATION_IN_DEGREES are defined at the beginning to set default visualization and processing settings.
Helper Functions:

create_cosine_mask(shape, center, r_inner, r_outer): Creates a smooth cosine mask for filtering in the FFT domain.
load_haadf_image(): Opens a file dialog to load an image using HyperSpy, handling various file formats and converting to a grayscale float array.
preprocess_data(data, threshold_percent): Applies Gaussian filtering and thresholding to create a material mask.
compute_fft_and_contrast(smoothed_data): Computes the FFT of the image and returns the FFT data and its magnitude.
calculate_displacements_and_strain(...): Computes the phase images, displacement fields, and strain components from the FFT data.
GPAApp Class:

Implements the main GUI using Tkinter.
GUI Components: Contains frames, buttons, entries, and sliders for parameter input.
Visualization: Uses Matplotlib for displaying multiple plots in a grid layout.
Interactive Features: Includes functions for selecting FFT centers, processing images, saving results, and performing line scans.
Event Handling: Provides callback functions for button clicks and mouse events (for point selection and line scanning).
Contributing
Contributions and suggestions are welcome! Feel free to fork the repository and submit pull requests.

License
Include the license information for your project here.
