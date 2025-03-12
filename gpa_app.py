import os
import sys
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from tkinter import (
    Tk, Label, Entry, Button as TkButton, StringVar, messagebox, filedialog,
    Scale, HORIZONTAL, Frame, simpledialog
)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, Circle
from skimage.measure import profile_line

from data_processor import DataProcessor
from strain_calculator import StrainCalculator

COLORMAP = 'jet'
DEFAULT_THRESHOLD_PERCENTILE = 0
DEFAULT_SIGMA_STRAIN_SMOOTH = 0

class GPAApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Strain Mapping GUI (in %)")

        self.master.rowconfigure(0, weight=0)
        self.master.columnconfigure(0, weight=1)

        self.center1_x = StringVar(value="0")
        self.center1_y = StringVar(value="0")
        self.gaussian_width1 = StringVar(value="10")
        self.circle_radius1 = StringVar(value="20")

        self.center2_x = StringVar(value="0")
        self.center2_y = StringVar(value="0")
        self.gaussian_width2 = StringVar(value="10")
        self.circle_radius2 = StringVar(value="20")

        self.ref_x0 = StringVar(value="0")
        self.ref_y0 = StringVar(value="0")
        self.ref_x1 = StringVar(value="50")
        self.ref_y1 = StringVar(value="50")

        self.sigma_smooth_var = StringVar(value=str(DEFAULT_SIGMA_STRAIN_SMOOTH))

        self.exx_min_var = StringVar(value="-5")
        self.exx_max_var = StringVar(value="5")
        self.eyy_min_var = StringVar(value="-5")
        self.eyy_max_var = StringVar(value="5")

        self.selected_points = []
        self.data = None
        self.smoothed_data = None
        self.material_mask = None
        self.fft_data = None
        self.fft_magnitude = None
        self.colorbars = []
        self.last_results = None
        self.out_dir = None  

        self.build_gui()
        self.load_data_initial()
        self.init_matplotlib_canvas()

    def build_gui(self):
        self.control_frame = Frame(self.master)
        self.control_frame.grid(row=0, column=0, sticky="nsew")

        TkButton(
            self.control_frame, 
            text="Load New Image", 
            command=self.load_new_image
        ).grid(row=0, columnspan=2, pady=5)

        Label(self.control_frame, text="FFT Plot: Select Circle Centers").grid(row=1, columnspan=2)
        TkButton(
            self.control_frame, 
            text="Select Points", 
            command=self.select_centers
        ).grid(row=2, columnspan=2, pady=5)

        Label(self.control_frame, text="Center 1 X:").grid(row=3, column=0, sticky="e")
        Entry(self.control_frame, textvariable=self.center1_x).grid(row=3, column=1)
        Label(self.control_frame, text="Center 1 Y:").grid(row=4, column=0, sticky="e")
        Entry(self.control_frame, textvariable=self.center1_y).grid(row=4, column=1)
        Label(self.control_frame, text="Inner Radius 1:").grid(row=5, column=0, sticky="e")
        Entry(self.control_frame, textvariable=self.gaussian_width1).grid(row=5, column=1)
        Label(self.control_frame, text="Outer Radius 1:").grid(row=6, column=0, sticky="e")
        Entry(self.control_frame, textvariable=self.circle_radius1).grid(row=6, column=1)

        Label(self.control_frame, text="Center 2 X:").grid(row=7, column=0, sticky="e")
        Entry(self.control_frame, textvariable=self.center2_x).grid(row=7, column=1)
        Label(self.control_frame, text="Center 2 Y:").grid(row=8, column=0, sticky="e")
        Entry(self.control_frame, textvariable=self.center2_y).grid(row=8, column=1)
        Label(self.control_frame, text="Inner Radius 2:").grid(row=9, column=0, sticky="e")
        Entry(self.control_frame, textvariable=self.gaussian_width2).grid(row=9, column=1)
        Label(self.control_frame, text="Outer Radius 2:").grid(row=10, column=0, sticky="e")
        Entry(self.control_frame, textvariable=self.circle_radius2).grid(row=10, column=1)

        Label(self.control_frame, text="Ref Area Top-Left X:").grid(row=11, column=0, sticky="e")
        Entry(self.control_frame, textvariable=self.ref_x0).grid(row=11, column=1)
        Label(self.control_frame, text="Ref Area Top-Left Y:").grid(row=12, column=0, sticky="e")
        Entry(self.control_frame, textvariable=self.ref_y0).grid(row=12, column=1)
        Label(self.control_frame, text="Ref Area Bottom-Right X:").grid(row=13, column=0, sticky="e")
        Entry(self.control_frame, textvariable=self.ref_x1).grid(row=13, column=1)
        Label(self.control_frame, text="Ref Area Bottom-Right Y:").grid(row=14, column=0, sticky="e")
        Entry(self.control_frame, textvariable=self.ref_y1).grid(row=14, column=1)

        Label(self.control_frame, text="Sigma").grid(row=15, column=0, sticky="e")
        self.sigma_scale = Scale(self.control_frame, from_=0, to=50, resolution=0.1, orient=HORIZONTAL)
        self.sigma_scale.set(float(self.sigma_smooth_var.get()))
        self.sigma_scale.grid(row=15, column=1, sticky="ew")

        Label(self.control_frame, text="Mask Threshold (%)").grid(row=16, column=0, sticky="e")
        self.threshold_scale = Scale(self.control_frame, from_=0, to=100, resolution=0.1, orient=HORIZONTAL)
        self.threshold_scale.set(DEFAULT_THRESHOLD_PERCENTILE)
        self.threshold_scale.grid(row=16, column=1, sticky="ew")

        # Strain scale (in %)
        Label(self.control_frame, text="Exx min (%):").grid(row=17, column=0, sticky="e")
        Entry(self.control_frame, textvariable=self.exx_min_var).grid(row=17, column=1)

        Label(self.control_frame, text="Exx max (%):").grid(row=18, column=0, sticky="e")
        Entry(self.control_frame, textvariable=self.exx_max_var).grid(row=18, column=1)

        Label(self.control_frame, text="Eyy min (%):").grid(row=19, column=0, sticky="e")
        Entry(self.control_frame, textvariable=self.eyy_min_var).grid(row=19, column=1)

        Label(self.control_frame, text="Eyy max (%):").grid(row=20, column=0, sticky="e")
        Entry(self.control_frame, textvariable=self.eyy_max_var).grid(row=20, column=1)

        TkButton(self.control_frame, text="Apply", command=self.process_selection).grid(row=21, columnspan=2, pady=10)
        TkButton(self.control_frame, text="Save", command=self.save_images).grid(row=22, columnspan=2, pady=10)
        TkButton(self.control_frame, text="Line Scan", command=self.line_scan_dialog).grid(row=23, columnspan=2, pady=10)

        for i in range(24):
            self.control_frame.rowconfigure(i, weight=0)
        self.control_frame.columnconfigure(0, weight=1)
        self.control_frame.columnconfigure(1, weight=1)

    def load_data_initial(self):
        """Attempt to load data once the app starts."""
        try:
            self.data = DataProcessor.load_haadf_image()
            threshold_val = self.threshold_scale.get()
            self.smoothed_data, self.material_mask = DataProcessor.preprocess_data(
                self.data, threshold_percent=threshold_val
            )
            self.fft_data, self.fft_magnitude = DataProcessor.compute_fft_and_contrast(
                self.smoothed_data
            )
        except FileNotFoundError:
            messagebox.showerror("File Selection Error", "No file selected. Exiting.")
            self.master.destroy()
            sys.exit(1)
        except Exception as e:
            messagebox.showerror("Initialization Error", str(e))
            self.master.destroy()
            sys.exit(1)

    def load_new_image(self):
        try:
            data_new = DataProcessor.load_haadf_image()
        except FileNotFoundError:
            return
        except Exception as e:
            messagebox.showerror("Loading Error", str(e))
            return

        self.data = data_new
        threshold_val = self.threshold_scale.get()
        self.smoothed_data, self.material_mask = DataProcessor.preprocess_data(
            self.data, threshold_percent=threshold_val
        )
        self.fft_data, self.fft_magnitude = DataProcessor.compute_fft_and_contrast(
            self.smoothed_data
        )
        self.last_results = None

        # Clear colorbars and axes
        for cbar in self.colorbars:
            cbar.remove()
        self.colorbars.clear()

        for ax in self.axs.flatten():
            ax.clear()

        self.canvas.draw()
        messagebox.showinfo("New Image Loaded",
                            "Successfully loaded a new image.\nSet parameters and click 'Apply' to process.")

    def select_centers(self):
        if self.fft_magnitude is None:
            return
        self.selected_points.clear()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        fig.suptitle("Double-click on left to pick dot1, on right to pick dot2")

        im1 = ax1.imshow(np.log(self.fft_magnitude + 1), cmap='gray')
        ax1.set_title("Left (dot1)")
        plt.colorbar(im1, ax=ax1)

        im2 = ax2.imshow(np.log(self.fft_magnitude + 1), cmap='gray')
        ax2.set_title("Right (dot2)")
        plt.colorbar(im2, ax=ax2)

        def on_click(event):
            if event.dblclick:
                ix, iy = int(event.xdata), int(event.ydata)
                if event.inaxes == ax1:
                    self.selected_points.append((iy, ix))
                elif event.inaxes == ax2:
                    self.selected_points.append((iy, ix))

                if len(self.selected_points) == 2:
                    fig.canvas.mpl_disconnect(cid)
                    plt.close(fig)
                    self.center1_y.set(str(self.selected_points[0][0]))
                    self.center1_x.set(str(self.selected_points[0][1]))
                    self.center2_y.set(str(self.selected_points[1][0]))
                    self.center2_x.set(str(self.selected_points[1][1]))

        cid = fig.canvas.mpl_connect('button_press_event', on_click)
        plt.show()

    def process_selection(self):
        try:
            if self.data is None:
                messagebox.showerror("No Data", "Please load an image first.")
                return

            threshold_val = self.threshold_scale.get()
            self.smoothed_data, self.material_mask = DataProcessor.preprocess_data(
                self.data, threshold_percent=threshold_val
            )
            self.fft_data, self.fft_magnitude = DataProcessor.compute_fft_and_contrast(self.smoothed_data)

            c1 = (int(self.center1_y.get()), int(self.center1_x.get()))
            g1 = float(self.gaussian_width1.get())
            r1 = float(self.circle_radius1.get())

            c2 = (int(self.center2_y.get()), int(self.center2_x.get()))
            g2 = float(self.gaussian_width2.get())
            r2 = float(self.circle_radius2.get())

            x0 = int(self.ref_x0.get())
            y0 = int(self.ref_y0.get())
            x1 = int(self.ref_x1.get())
            y1 = int(self.ref_y1.get())
            reference_area = (
                slice(min(y0, y1), max(y0, y1)),
                slice(min(x0, x1), max(x0, x1))
            )

            sigma_smooth = float(self.sigma_scale.get())

            results = StrainCalculator.calculate_displacements_and_strain(
                self.fft_data,
                self.material_mask,
                c1, g1, r1,
                c2, g2, r2,
                reference_area, 
                sigma_smooth
            )

            self.last_results = results
            self.update_plots(results, c1, g1, r1, c2, g2, r2, reference_area)

            messagebox.showinfo("Process Done", "Processing completed.")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values.")
        except Exception as e:
            messagebox.showerror("Processing Error", str(e))

    def init_matplotlib_canvas(self):
        self.canvas_frame = Frame(self.master)
        self.canvas_frame.grid(row=0, column=1, sticky="nsew", padx=0.1, pady=0.1)

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)

        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

        self.fig = Figure(figsize=(15, 12), dpi=100)
        self.axs = self.fig.subplots(3, 4)
        self.fig.subplots_adjust(wspace=0.3, hspace=0.3)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")

        self.toolbar_frame = Frame(self.master)
        self.toolbar_frame.grid(row=1, column=1, sticky="ew")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()

    def update_plots(self, results, c1, g1, r1, c2, g2, r2, reference_area):
        raw_phase_image1 = results['raw_phase_image1']
        raw_phase_image2 = results['raw_phase_image2']
        phase_image1 = results['phase_image1']
        phase_image2 = results['phase_image2']
        strain_xx = results['strain_xx']  # in %
        strain_yy = results['strain_yy']  # in %
        strain_xy = results['strain_xy']  # in %
        rotation_xy = results['rotation_xy']
        comp1_mag = np.abs(results['complex_image1'])
        comp2_mag = np.abs(results['complex_image2'])

        exx_min = float(self.exx_min_var.get())
        exx_max = float(self.exx_max_var.get())
        eyy_min = float(self.eyy_min_var.get())
        eyy_max = float(self.eyy_max_var.get())

        exy_min, exy_max = -5, 5  
        rot_min, rot_max = -5, 5

        for cbar in self.colorbars:
            cbar.remove()
        self.colorbars.clear()

        for ax in self.axs.flatten():
            ax.clear()

        ax0 = self.axs[0, 0]
        im0 = ax0.imshow(self.data, cmap='gray')
        ax0.set_title("Original HAADF")
        cbar0 = self.fig.colorbar(im0, ax=ax0, fraction=0.046, pad=0.04)
        self.colorbars.append(cbar0)

        rect = Rectangle(
            (reference_area[1].start, reference_area[0].start),
            reference_area[1].stop - reference_area[1].start,
            reference_area[0].stop - reference_area[0].start,
            linewidth=2, edgecolor='yellow', facecolor='none'
        )
        ax0.add_patch(rect)

        ax1 = self.axs[0, 1]
        im1 = ax1.imshow(np.log(self.fft_magnitude + 1), cmap='gray')
        ax1.set_title("FFT Magnitude")
        cbar1 = self.fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
        self.colorbars.append(cbar1)

        circle1_in = Circle((c1[1], c1[0]), g1, color='red', fill=False, linewidth=1)
        circle1_out = Circle((c1[1], c1[0]), r1, color='magenta', fill=False, linewidth=1)
        ax1.add_patch(circle1_in)
        ax1.add_patch(circle1_out)

        circle2_in = Circle((c2[1], c2[0]), g2, color='blue', fill=False, linewidth=1)
        circle2_out = Circle((c2[1], c2[0]), r2, color='green', fill=False, linewidth=1)
        ax1.add_patch(circle2_in)
        ax1.add_patch(circle2_out)

        ax2 = self.axs[0, 2]
        im2 = ax2.imshow(phase_image1, cmap=COLORMAP)
        ax2.set_title("Phase Image 1")
        cbar2 = self.fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
        self.colorbars.append(cbar2)

        ax3 = self.axs[0, 3]
        im3 = ax3.imshow(phase_image2, cmap=COLORMAP)
        ax3.set_title("Phase Image 2")
        cbar3 = self.fig.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)
        self.colorbars.append(cbar3)

        ax4 = self.axs[1, 0]
        im4 = ax4.imshow(strain_xx, cmap=COLORMAP, vmin=exx_min, vmax=exx_max)
        ax4.set_title("Exx (%)")
        cbar4 = self.fig.colorbar(im4, ax=ax4, fraction=0.046, pad=0.04)
        self.colorbars.append(cbar4)

        ax5 = self.axs[1, 1]
        im5 = ax5.imshow(strain_yy, cmap=COLORMAP, vmin=eyy_min, vmax=eyy_max)
        ax5.set_title("Eyy (%)")
        cbar5 = self.fig.colorbar(im5, ax=ax5, fraction=0.046, pad=0.04)
        self.colorbars.append(cbar5)

        ax6 = self.axs[1, 2]
        im6 = ax6.imshow(strain_xy, cmap=COLORMAP, vmin=exy_min, vmax=exy_max)
        ax6.set_title("Exy (%)")
        cbar6 = self.fig.colorbar(im6, ax=ax6, fraction=0.046, pad=0.04)
        self.colorbars.append(cbar6)

        ax7 = self.axs[1, 3]
        rot_label = "Rotation (deg)"
        im7 = ax7.imshow(rotation_xy, cmap=COLORMAP, vmin=rot_min, vmax=rot_max)
        ax7.set_title(rot_label)
        cbar7 = self.fig.colorbar(im7, ax=ax7, fraction=0.046, pad=0.04)
        self.colorbars.append(cbar7)

        ax8 = self.axs[2, 0]
        im8 = ax8.imshow(raw_phase_image1, cmap='gray')
        ax8.set_title("Raw Phase Image 1")
        cbar8 = self.fig.colorbar(im8, ax=ax8, fraction=0.046, pad=0.04)
        self.colorbars.append(cbar8)

        ax9 = self.axs[2, 1]
        im9 = ax9.imshow(raw_phase_image2, cmap='gray')
        ax9.set_title("Raw Phase Image 2")
        cbar9 = self.fig.colorbar(im9, ax=ax9, fraction=0.046, pad=0.04)
        self.colorbars.append(cbar9)

        ax10 = self.axs[2, 2]
        im10 = ax10.imshow(comp1_mag, cmap='gray')
        ax10.set_title("Complex Image 1 Mag")
        cbar10 = self.fig.colorbar(im10, ax=ax10, fraction=0.046, pad=0.04)
        self.colorbars.append(cbar10)

        ax11 = self.axs[2, 3]
        im11 = ax11.imshow(comp2_mag, cmap='gray')
        ax11.set_title("Complex Image 2 Mag")
        cbar11 = self.fig.colorbar(im11, ax=ax11, fraction=0.046, pad=0.04)
        self.colorbars.append(cbar11)

        self.canvas.draw()

    def save_figure_with_colorbar(self, img_data, cmap, filename,
                                  title=None, do_log=False,
                                  vmin=None, vmax=None):
        """Helper to save a figure with consistent colorbar and scale."""
        fig, ax = plt.subplots(figsize=(5,4), dpi=100)
        if do_log and np.all(img_data >= 0):
            plot_data = np.log(img_data + 1)
        else:
            plot_data = img_data

        im = ax.imshow(plot_data, cmap=cmap, vmin=vmin, vmax=vmax)
        ax.set_xticks([])
        ax.set_yticks([])
        if title:
            ax.set_title(title)
        cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        out_path = os.path.join(self.out_dir, filename)
        fig.savefig(out_path, dpi=600, format='tif', bbox_inches='tight')
        plt.close(fig)

    def save_images(self):
        """Main save function triggered by the Save button."""
        if self.last_results is None:
            messagebox.showerror("No Results", "Please click 'Apply' first to generate results.")
            return

        self.out_dir = filedialog.askdirectory(title="Select folder to save .tif images")
        if not self.out_dir:
            return

        exx_min = float(self.exx_min_var.get())
        exx_max = float(self.exx_max_var.get())
        eyy_min = float(self.eyy_min_var.get())
        eyy_max = float(self.eyy_max_var.get())
        exy_min, exy_max = -5, 5
        rot_min, rot_max = -5, 5

        r = self.last_results
        raw_phase_image1 = r['raw_phase_image1']
        raw_phase_image2 = r['raw_phase_image2']
        phase_image1 = r['phase_image1']
        phase_image2 = r['phase_image2']
        strain_xx = r['strain_xx']
        strain_yy = r['strain_yy']
        strain_xy = r['strain_xy']
        rotation_xy = r['rotation_xy']
        comp1_mag = np.abs(r['complex_image1'])
        comp2_mag = np.abs(r['complex_image2'])

        self.save_figure_with_colorbar(self.data, 'gray',
                                       "01_Original_HAADF.tif",
                                       title="Original HAADF",
                                       do_log=False)

        self.save_figure_with_colorbar(self.fft_magnitude, 'gray',
                                       "02_FFT_Magnitude.tif",
                                       title="FFT Magnitude",
                                       do_log=True)

        self.save_figure_with_colorbar(raw_phase_image1, 'gray',
                                       "03_Raw_Phase_Image_1.tif",
                                       title="Raw Phase Image 1")
        self.save_figure_with_colorbar(raw_phase_image2, 'gray',
                                       "04_Raw_Phase_Image_2.tif",
                                       title="Raw Phase Image 2")

        self.save_figure_with_colorbar(phase_image1, COLORMAP,
                                       "05_Phase_Image_1.tif",
                                       title="Phase Image 1")
        self.save_figure_with_colorbar(phase_image2, COLORMAP,
                                       "06_Phase_Image_2.tif",
                                       title="Phase Image 2")

        self.save_figure_with_colorbar(strain_xx, COLORMAP,
                                       "07_Strain_xx_percent.tif",
                                       title="Strain XX (%)",
                                       vmin=exx_min, vmax=exx_max)
        self.save_figure_with_colorbar(strain_yy, COLORMAP,
                                       "08_Strain_yy_percent.tif",
                                       title="Strain YY (%)",
                                       vmin=eyy_min, vmax=eyy_max)
        self.save_figure_with_colorbar(strain_xy, COLORMAP,
                                       "09_Strain_xy_percent.tif",
                                       title="Strain XY (%)",
                                       vmin=exy_min, vmax=exy_max)
        self.save_figure_with_colorbar(rotation_xy, COLORMAP,
                                       "10_Rotation_xy.tif",
                                       title="Rotation XY",
                                       vmin=rot_min, vmax=rot_max)

        self.save_figure_with_colorbar(comp1_mag, 'gray',
                                       "11_Complex_Image_1_Mag.tif",
                                       title="Complex Image 1 Mag")
        self.save_figure_with_colorbar(comp2_mag, 'gray',
                                       "12_Complex_Image_2_Mag.tif",
                                       title="Complex Image 2 Mag")

        messagebox.showinfo("Save Complete", f"Images saved in:\n{self.out_dir}")

    def line_scan_dialog(self):
        """Dialog to pick which strain map to line-scan."""
        if self.last_results is None:
            messagebox.showerror("No Results", "Please click 'Apply' first to generate strain maps.")
            return

        strain_map_choices = ["strain_xx", "strain_yy", "strain_xy", "rotation_xy"]
        choice = simpledialog.askstring(
            "Line Scan Choice",
            f"Which map do you want to line-scan?\nOptions: {', '.join(strain_map_choices)}",
            initialvalue="strain_xx"
        )
        if not choice:
            return
        if choice not in strain_map_choices:
            messagebox.showerror("Invalid Choice", "Please choose a valid map name.")
            return

        thickness = simpledialog.askinteger(
            "Line Thickness",
            "Enter line-scan thickness (integer pixels):",
            minvalue=1,
            maxvalue=100,
            initialvalue=1
        )
        if thickness is None:
            return

        self.line_scan(map_name=choice, thickness=thickness)

    def line_scan(self, map_name="strain_xx", thickness=1):
        """Perform a line scan on the chosen strain map."""
        data = self.last_results.get(map_name, None)
        if data is None:
            messagebox.showerror("Data Error", f"No data found for '{map_name}'.")
            return

        exx_min = float(self.exx_min_var.get())
        exx_max = float(self.exx_max_var.get())
        eyy_min = float(self.eyy_min_var.get())
        eyy_max = float(self.eyy_max_var.get())
        exy_min, exy_max = -5, 5
        rot_min, rot_max = -5, 5

        if map_name == 'strain_xx':
            this_vmin, this_vmax = exx_min, exx_max
        elif map_name == 'strain_yy':
            this_vmin, this_vmax = eyy_min, eyy_max
        elif map_name == 'strain_xy':
            this_vmin, this_vmax = exy_min, exy_max
        else:
            this_vmin, this_vmax = rot_min, rot_max

        fig, ax = plt.subplots()
        ax.set_title(f"Click two points to define line on {map_name}")

        im = ax.imshow(data, cmap=COLORMAP, vmin=this_vmin, vmax=this_vmax)
        plt.colorbar(im, ax=ax)

        points = []

        def on_click(event):
            if event.inaxes == ax and event.button == 1:
                points.append((int(event.ydata), int(event.xdata)))
                if len(points) == 2:
                    fig.canvas.mpl_disconnect(cid)
                    p0, p1 = points
                    profile = profile_line(
                        data,
                        p0,
                        p1,
                        linewidth=thickness,
                        order=1,
                        reduce_func=np.mean
                    )
                    fig2, ax2 = plt.subplots()
                    ax2.plot(profile, 'o-', lw=1.5)
                    ax2.set_title(f"Line Scan of {map_name} (thickness={thickness})")
                    ax2.set_xlabel("Distance (pixels along line)")
                    if map_name.startswith('strain_'):
                        ax2.set_ylabel(f"{map_name} (%)")
                    else:
                        ax2.set_ylabel(map_name)
                    ax2.set_ylim([this_vmin, this_vmax])

                    fig2.tight_layout()
                    plt.show()

        cid = fig.canvas.mpl_connect('button_press_event', on_click)
        plt.show()
