Updating  



Strain Mapping GUI
Introduction
The Strain Mapping GUI is a Python-based graphical tool for analyzing and visualizing strain in materials from high-resolution microscopy images. It uses Geometric Phase Analysis (GPA) to compute deformation (strain) fields from an image's Fourier transform. The GUI provides an interactive workflow for researchers to load an electron microscopy image, select diffraction spots in the image’s FFT, and generate strain maps (εxx, εyy, εxy) along with the local rotation field. This tool is designed to simplify strain mapping analysis by offering a user-friendly interface, real-time visualization of results, and easy exporting of output images.
Features
Interactive GPA Analysis: Allows selection of two reciprocal lattice points (diffraction spots) on the FFT of the image to perform GPA and compute in-plane strain components.
Multiple Format Support: Can load various electron microscopy image formats (EMD, DM3/DM4, TIFF, HDF5) commonly used in TEM/STEM, making it flexible for different data sources.
Real-Time Visualization: Displays the original image, its Fourier transform, filtered phase images, calculated strain maps (εxx, εyy, εxy), and rotation map in a convenient panel layout immediately after processing.
Adjustable Parameters: Provides controls to fine-tune the analysis – users can set mask radii for frequency selection, define a reference region for zero-strain calibration, apply Gaussian smoothing to strain maps, and threshold low-intensity regions to mask out background (vacuum) areas.
Line Scan Analysis: Includes a Line Scan feature to interactively draw a line on any strain map and plot the strain values along that line, useful for quantitative profile analysis across a region of interest.
Export of Results: One-click saving of all generated output images (original, FFT, phase images, strain maps, rotation map, etc.) as high-resolution TIFF files for documentation or further analysis.
Requirements
Make sure your system meets the following requirements before using the Strain Mapping GUI:
Python 3.x (tested on Python 3.x; a recent version like 3.8 or above is recommended)
Conda (Miniconda or Anaconda) for managing the environment (optional but recommended)
NumPy – array and FFT computations
SciPy – numerical algorithms (used for Gaussian filtering, etc.)
Matplotlib – plotting and rendering of images (with TkAgg backend for GUI)
scikit-image – image processing (phase unwrapping, line profile extraction)
HyperSpy – for loading microscopy data formats (.emd, .dm3, .dm4, etc.)
Tkinter – standard Python GUI toolkit (comes with Python; used for the interface)
All required Python packages can be installed via conda or pip. Using a conda environment will ensure the correct versions of these libraries are installed.
Installation
Follow these steps to install the Strain Mapping GUI and set up the environment using conda:
Clone the Repository: Download the project source code from GitHub (or your source). You can use git:
bash
Copy
Edit
git clone https://github.com/YourUsername/StrainMappingGUI.git
cd StrainMappingGUI
(Replace the URL with the actual repository link.)
Create a Conda Environment: Create a new conda environment (named for example strainmapgui) with the required Python version:
bash
Copy
Edit
conda create -n strainmapgui python=3.9 -y
conda activate strainmapgui
Install Dependencies: Use conda (with the conda-forge channel) to install all required libraries:
bash
Copy
Edit
conda install -c conda-forge numpy scipy matplotlib scikit-image hyperspy -y
Note: This will also install tkinter if not already present (as part of the Python installation). If you prefer, you can alternatively use pip install numpy scipy matplotlib scikit-image hyperspy.
Verify Installation: After installing, you should have all required packages in the environment. You can verify by running Python and attempting to import the libraries:
bash
Copy
Edit
python -c "import numpy, scipy, matplotlib, skimage, hyperspy"
If no errors occur, the environment is ready.
With the environment set up and the code obtained, you are ready to run the Strain Mapping GUI.
Usage
To run the program, first activate the conda environment and navigate to the project directory. Then launch the GUI by executing the main application script. For example:
bash
Copy
Edit
conda activate strainmapgui
python StrainMappingGUI.py
(Replace StrainMappingGUI.py with the actual filename if different.) Once the application launches, a window will appear with the GUI. Basic usage workflow:
Load an Image: Click “Load New Image” and browse to select an input file. Supported formats include EMD, DM3, DM4, TIFF, or HDF5 (see Supported File Formats below). After loading, the image will be displayed in the GUI.
(Optional) Adjust Threshold: If your image has background regions (e.g., vacuum in a TEM image), use the “Mask Threshold (%)” slider to set an intensity percentile for masking. This will ignore pixels below the given percentile (highlighted as background) in strain calculations, helping to focus on the material region.
Select Diffraction Spots: Click “Select Points” to pick two points on the FFT for strain analysis. This opens an interactive window showing the Fourier transform of the image:
Double-click on a prominent diffraction spot in the left panel (this sets Point 1).
Double-click on another spot in the right panel for Point 2. After selecting, the coordinates for Center 1 and Center 2 will automatically populate in the GUI fields.
Refine Selection (Optional): You can fine-tune the frequency selection parameters:
Adjust Center 1 X/Y and Center 2 X/Y fields if you need to tweak the exact position of the selected FFT peaks.
Adjust Inner Radius and Outer Radius for each point (these define the size of the circular mask around each selected FFT peak; the inner radius is where the mask is fully applied and the outer radius is where it tapers off).
By default, Inner Radius = 10 and Outer Radius = 20 (in pixels). Increase these if the diffraction spot is larger or to capture more of its intensity, but avoid overlapping with other spots.
Set Reference Area (Optional): The fields Ref Area Top-Left X/Y and Bottom-Right X/Y define a reference region in the image that is assumed to have no strain (reference lattice). By default, it’s set to coordinates (0,0) to (50,50) – the top-left corner of the image. You can change these values to specify a different rectangular region (in pixel coordinates) that should represent an unstrained area. The average displacement in this region will be set as zero to calibrate the strain maps.
Smoothing (Optional): Adjust the Sigma slider to apply Gaussian smoothing to the computed strain fields. A value of 0 means no smoothing, while higher values (e.g., 1–5) will smooth out noise in the strain maps at the cost of some spatial resolution. Choose this based on the noise level in your data.
Process the Image: Click “Apply” to run the strain mapping computation with the current settings. The GUI will process the image (this may take a few seconds for large images) and then display the results in the output panels on the right side (see GUI Overview below for details on the displayed results). A message dialog will confirm when processing is complete.
Inspect Results: Examine the strain maps and other output in the GUI window. You can identify regions of tensile vs compressive strain from the color maps (by default, a jet colormap is used for phase and strain images, where red vs blue indicates positive vs negative values for strain).
Line Scan Analysis (Optional): For a more detailed analysis, use the “Line Scan” feature:
Click Line Scan. You will be prompted to choose which strain component to analyze (εxx, εyy, εxy, or rotation) and to specify a line thickness (in pixels) for averaging.
After confirming, the program will open the chosen strain map in a new window. You can then interactively draw a line by clicking two endpoints on the map.
The GUI will plot the strain values along that line, allowing you to see how strain varies across a particular direction or feature in your image. Note: The line profile will appear in a matplotlib window; you can save the figure from that window if needed.
Save Outputs: Once you are satisfied with the results, click “Save” to export all result images. You will be asked to select a directory. The tool will then save a series of TIFF files to that folder, including:
The original image (01_Original_HAADF.tif)
The FFT magnitude (02_FFT_Magnitude.tif)
Phase images for each selected spot (03_Raw_Phase_Image_1.tif, 04_Raw_Phase_Image_2.tif, 05_Phase_Image_1.tif, 06_Phase_Image_2.tif)
Strain maps (07_Strain_xx.tif, 08_Strain_yy.tif, 09_Strain_xy.tif) and the rotation map (10_Rotation_xy.tif)
Additional debug images like the masked FFT components (11_Complex_Image_1_Mag.tif, 12_Complex_Image_2_Mag.tif)
These files are saved at high resolution (600 DPI) suitable for documentation or publication. A confirmation message will appear when saving is complete.
Following the above steps, you can iteratively load different images or adjust parameters to analyze multiple datasets. Tip: If you want to start fresh, simply load a new image or restart the program to clear previous results.
GUI Overview
The Strain Mapping GUI window is divided into two main areas: the Control Panel (left side) and the Output Display (right side).
Control Panel
This section of the GUI contains all interactive controls and input fields:
Load New Image: Opens a file dialog to select a new image or dataset. Once selected, the image is loaded and displayed. (If an image is already loaded, it will be replaced.)
FFT Plot: Select Circle Centers (Select Points): Opens an interactive FFT view for picking two diffraction spots. Double-clicking on the left plot sets the first spot, and on the right plot sets the second spot. The chosen coordinates populate the Center 1 and Center 2 fields.
Center 1 X / Center 1 Y: Coordinates (in pixels) of the first selected diffraction spot in the FFT. These fields are filled automatically by Select Points, but you can also enter or adjust values manually.
Inner Radius 1 / Outer Radius 1: The inner and outer radii (in pixels) of the circular mask around the first selected spot. The mask between these radii is applied to isolate the Fourier component corresponding to that spot (using a soft cosine edge between inner and outer radius). Inner Radius 1 defines the radius of full inclusion of the spot, and Outer Radius 1 defines where the inclusion tapers to zero. Similarly, Inner Radius 2 / Outer Radius 2 apply to the second spot.
Center 2 X / Center 2 Y: Coordinates of the second selected diffraction spot in the FFT (analogous to Center 1 X/Y).
Ref Area Top-Left X / Y: The pixel coordinates (X,Y) of the top-left corner of the reference region in the image. This, together with the bottom-right coordinates, defines a rectangular area assumed to have zero strain.
Ref Area Bottom-Right X / Y: The pixel coordinates of the bottom-right corner of the reference region. By default, the reference area is a 50×50 pixel square at the top-left of the image (0,0 to 50,50). You can adjust these four values to select any region in the image that should be considered strain-free. The average displacement in this region will be subtracted from the displacement fields to set the baseline (zero) strain.
Sigma: A slider to adjust the smoothing applied to strain and rotation maps. Range is 0 to 50 (in units of standard deviation for a Gaussian kernel). Increasing this value will smooth out noise in the strain maps but may blur fine features. The default value is 0 (no smoothing).
Mask Threshold (%): A slider to set the intensity percentile threshold for masking. Range is 0 to 100%. This is used to create a mask (typically to exclude vacuum/background). For example, setting this to 5% will mask (ignore) the dimmest 5% of pixels in the image (assuming those are background). The masked areas will not contribute to the strain calculation and will appear blank (NaN) in output maps. Default is 0 (no masking, entire image used).
Apply: Processes the currently loaded image with all the above settings. When clicked, the program computes the FFT, applies the masks for the two selected spots, performs phase unwrapping and displacement calculation, then computes the strain and rotation fields. It updates the Output Display with the results. (If required inputs are missing, e.g. no image loaded or invalid entries, it will show an error dialog.)
Save: Saves all result images to disk (as described in the Usage section). If you click Save before running Apply, it will prompt that there are no results to save.
Line Scan: Initiates the line scan tool. When clicked, a dialog asks which map to analyze (εxx, εyy, εxy, or rotation) and the thickness for the line. After you provide this info, a new window opens showing the chosen map; you can then select two points on that map to define a line. A profile plot of the values along the line will be generated. Use this to quantitatively examine strain variations along a line of interest.
All buttons and controls are arranged in a logical order in the panel. Typically, you would work from top to bottom: load image, select points, adjust parameters, then apply and possibly save or perform a line scan.
Output Display
After you click Apply, the right side of the GUI displays a grid of result plots for analysis. The layout is typically arranged in rows and columns, for example:
Original Image: The top-left panel shows the loaded image (in grayscale). If a reference area was specified, it is highlighted with a yellow rectangular outline on this image for reference.
FFT Magnitude: The top-middle panel shows the Fourier transform (magnitude spectrum) of the image on a log scale (grayscale). The two selected frequency spots are indicated by circle overlays:
A red circle (inner) and magenta circle (outer) around the first spot.
A blue circle (inner) and green circle (outer) around the second spot.
These circles correspond to the Inner/Outer Radius settings for each selected point, helping you see the masked region used for GPA.
Phase Image 1: The top-right panel (or next in sequence) displays the unwrapped phase image corresponding to the first selected diffraction spot (after applying the circular mask). This phase image represents the displacement field in the direction of that lattice periodicity.
Phase Image 2: Similarly, another panel shows the unwrapped phase for the second selected spot. Areas of uniform phase indicate consistent lattice spacing; gradients in this image relate to lattice distortions.
Strain Maps (εxx, εyy, εxy): In the next row, the GUI shows the calculated strain components:
Exx: Strain in the x-direction (horizontal strain) as a percentage or fraction (depending on the context, typically displayed as a dimensionless strain value).
Eyy: Strain in the y-direction (vertical strain).
Exy: Shear strain (xy component).
These maps are shown with the chosen colormap (default jet), with colorbars indicating the scale. Red/yellow regions might indicate positive strain (tension) and blue regions negative strain (compression), relative to the reference.
Rotation Map: Also in the results, the in-plane rotation field (often denoted ω or θ) is shown. This represents the local rotation (in degrees by default) of the lattice at each point, which can occur alongside strain. The rotation map panel is labeled “Rotation (deg)” (or radians if configured otherwise).
Raw Phase Images: The GUI also includes panels for Raw Phase Image 1 and Raw Phase Image 2. These are the unprocessed phase maps from each FFT spot before subtracting the reference phase offset. They appear in grayscale. They are mainly provided for completeness or advanced inspection – most users will focus on the processed phase (Phase Image 1/2) and strain maps instead.
Filtered Component Magnitudes: Additionally, panels labeled Complex Image 1 Mag and Complex Image 2 Mag display the magnitude of the inverse FFT of each isolated frequency component. In simpler terms, these show the real-space intensity of the lattice fringes corresponding to each selected diffraction spot (essentially highlighting the regions of the image contributing to each frequency). These are shown in grayscale and can be useful to verify that the masking captured the correct features in the image.
All the output panels include colorbars (where applicable) and titles for clarity. You can visually correlate features between the images – for example, a region of the original image might correspond to a certain pattern in the phase image and show up as a hot spot in the strain map. The multi-panel display allows easy side-by-side comparison. You may resize the window or zoom into panels as needed (standard matplotlib navigation tools are available for the plots).
Supported File Formats
The Strain Mapping GUI supports a variety of microscopy image formats commonly used in electron microscopy. You can load files with the following extensions:
EMD (.emd): Electron Microscopy Dataset files (often produced by 4D STEM or other microscope data exports; loaded via HyperSpy).
DM3 / DM4 (.dm3, .dm4): Gatan DigitalMicrograph® files, typically high-resolution TEM images or EELS/EFTEM data. Both version 3 and 4 are supported.
TIFF (.tif, .tiff): Tagged Image File Format images. High-bit-depth TIFFs (such as 16-bit images from detectors) are supported.
HDF5 (.h5, .hdf): Hierarchical Data Format files containing image data. If the HDF5 file contains a dataset with a 2D image (or 3D stack), it can be loaded.
When using Load New Image, the file dialog by default filters for the above types. If you select an unsupported format, the program will raise an error. Note: Standard image formats like JPEG or PNG are not directly supported in the file dialog filter. If you need to analyze such images, convert them to TIFF first or use the “All files” option in the dialog (but be aware the program expects a grayscale image input). For multi-dimensional data:
If a 3D dataset is loaded (for example, an EMD file with a 2D image series or a 4D STEM dataset collapsed to 3D), the program will automatically sum across the third dimension to produce a 2D image for analysis. This ensures, for instance, that a stack of images or a 4D dataset (diffraction patterns) is reduced appropriately.
If the image data has multiple channels (e.g., an RGB image or a hyper-spectral dataset), the GUI will convert it to grayscale by averaging the first three channels. This is done to yield a single intensity image for FFT and strain computation.
It is recommended to use high-resolution, high signal-to-noise images for best results. The accuracy of the strain mapping is directly related to the quality of the input image and the clarity of the diffraction spots.
Known Limitations
While the Strain Mapping GUI is a powerful tool for strain analysis, be aware of the following constraints and limitations:
Two-Spot GPA Assumption: The tool uses two Fourier spots for GPA, meaning it computes strain relative to two specific lattice directions. This covers in-plane strain for a roughly hexagonal or orthogonal lattice grid. However, it might not capture more complex strain scenarios that require multiple diffraction vectors or a full 2D strain tensor beyond the two components provided.
Image Size and Performance: Very large images (e.g., >4k x 4k pixels) may be slow to process and visualize. The computations (FFT, unwrapping, etc.) are done on the CPU via NumPy/SciPy. Ensure your system has sufficient memory for large datasets. In some cases, downsampling the image or cropping to the region of interest can help.
Manual Reference Selection: The reference area for zero strain must be manually entered as pixel coordinates. The GUI does not currently provide an interactive way to draw or adjust this region on the image (though the chosen region is shown as a yellow box after processing). This requires the user to have some a priori knowledge of an unstrained area or to assume part of the image is strain-free. Mis-selection of the reference region can offset the strain values.
Limited File Type Scope: The program is tailored to electron microscopy data formats. It does not natively read common photography formats like JPEG, PNG, or BMP without conversion. Additionally, some specialized microscope file formats might not be supported unless they can be read via HyperSpy.
GUI Environment: Since it uses a Tkinter GUI, a display environment is required. On headless servers or remote machines, you may need to use X11 forwarding or a virtual display to run the interface. The tool is not designed to run purely from the command line (there is no non-GUI batch mode).
Dependency Footprint: The use of HyperSpy (for file I/O) means the environment might be relatively heavy, and installing HyperSpy can be complex on some systems. Using conda with the conda-forge channel is recommended for a smoother installation. If HyperSpy fails to load a certain file, you may need to update HyperSpy or convert the file to a supported format.
Accuracy Considerations: The strain calculation assumes good quality phase unwrapping and clear diffraction spots. Noisy images, significant drift or distortion, or very weak diffraction features can lead to inaccurate or noisy strain maps. Some experimentation with smoothing (Sigma) and thresholding is necessary in such cases. The user should interpret results carefully, especially at image edges or in low-signal areas (where phase unwrapping can be less reliable).
Despite these limitations, the tool is highly useful for quick strain analyses on high-resolution TEM/STEM images. Ongoing improvements aim to address some of the above constraints (for example, adding more automated reference selection or GPU acceleration for large data).
License
This project is licensed under the MIT License. You are free to use, modify, and distribute the code under the terms of this license. See the LICENSE file in the repository for detailed information.
