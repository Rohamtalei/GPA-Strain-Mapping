# Strain Mapping GUI

This repository contains a graphical user interface (GUI) for strain mapping in materials using GPA (Geometric Phase Analysis). The application is built using `Tkinter` for the GUI and `matplotlib` for visualization.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Descriptions](#file-descriptions)
- [Dependencies](#dependencies)
- [License](#license)

## Features
- Load and preprocess HAADF images
- Perform FFT analysis on images
- Select points for geometric phase analysis
- Compute strain maps and rotation fields
- Save results as `.tif` images
- Interactive line scan analysis

## Installation

To run the application, first clone this repository and install the necessary dependencies:

```bash
git clone https://github.com/Rohamtalei/GPA-Strain-Mapping.git
cd strain-mapping-gui
pip install -r requirements.txt
```

## Usage

Run the application with:

```bash
python main.py
```

### Steps to Use the GUI
1. Load an HAADF image.
2. Perform FFT analysis and select points for phase calculations.
3. Define a reference area.
4. Compute strain fields.
5. Visualize and save strain maps.
6. Perform line scans if necessary.

## File Descriptions

### `main.py`
- Entry point for the application.
- Initializes the GUI using `GPAApp`.

### `gpa_app.py`
- Implements the GUI with `Tkinter`.
- Handles image processing, user interactions, and visualization.

### `data_processor.py`
- Provides functions to load, preprocess, and transform HAADF images.

### `strain_calculator.py`
- Computes displacements and strain fields from FFT analysis.
- Uses unwrapping techniques to extract phase images.

## Dependencies

Ensure the following packages are installed:
- `numpy`
- `matplotlib`
- `hyperspy`
- `scipy`
- `skimage`
- `tkinter`

Install dependencies using:

```bash
pip install -r requirements.txt
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

