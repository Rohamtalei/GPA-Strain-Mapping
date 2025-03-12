
import numpy as np
from numpy.fft import ifft2, ifftshift
from scipy.ndimage import gaussian_filter
from skimage.restoration import unwrap_phase

ROTATION_IN_DEGREES = True  

class StrainCalculator:


    @staticmethod
    def create_cosine_mask(shape, center, r_inner, r_outer):

        ny, nx = shape
        cy, cx = center
        y, x = np.indices((ny, nx))
        R = np.sqrt((x - cx)**2 + (y - cy)**2)
        mask = np.zeros(shape, dtype=float)
        inside_inner = (R <= r_inner)
        mask[inside_inner] = 1.0
        transition_region = (R > r_inner) & (R < r_outer)
        R_tr = R[transition_region]
        mask[transition_region] = 0.5 * (
            1.0 + np.cos(np.pi * (R_tr - r_inner) / (r_outer - r_inner))
        )
        outside_outer = (R >= r_outer)
        mask[outside_outer] = 0.0
        return mask

    @staticmethod
    def calculate_displacements_and_strain(
        fft_data, material_mask,
        c1, g1, r1,
        c2, g2, r2,
        reference_area, sigma_smooth
    ):

        mask1 = StrainCalculator.create_cosine_mask(fft_data.shape, c1, g1, r1)
        mask2 = StrainCalculator.create_cosine_mask(fft_data.shape, c2, g2, r2)

        filtered_fft1 = fft_data * mask1
        filtered_fft2 = fft_data * mask2

        complex_img1 = ifft2(ifftshift(filtered_fft1))
        complex_img2 = ifft2(ifftshift(filtered_fft2))

        raw_phase_1 = np.angle(complex_img1)
        raw_phase_2 = np.angle(complex_img2)

        Ny, Nx = fft_data.shape
        cy, cx = Ny // 2, Nx // 2

        g1x = (c1[1] - cx) / Nx
        g1y = (c1[0] - cy) / Ny
        g2x = (c2[1] - cx) / Nx
        g2y = (c2[0] - cy) / Ny

        Y, X = np.indices((Ny, Nx))
        phase_image1 = raw_phase_1 - 2*np.pi * (g1x*X + g1y*Y)
        phase_image2 = raw_phase_2 - 2*np.pi * (g2x*X + g2y*Y)

        phase_image1 = unwrap_phase(phase_image1)
        phase_image2 = unwrap_phase(phase_image2)

        G = np.array([[g1x, g1y], [g2x, g2y]], dtype=float)
        G_inv = np.linalg.pinv(G)

        Pg1 = phase_image1
        Pg2 = phase_image2

        ux = (-1/(2*np.pi)) * (G_inv[0,0]*Pg1 + G_inv[0,1]*Pg2)
        uy = (-1/(2*np.pi)) * (G_inv[1,0]*Pg1 + G_inv[1,1]*Pg2)

        ux_ref_mean = np.mean(ux[reference_area])
        uy_ref_mean = np.mean(uy[reference_area])
        ux = ux - ux_ref_mean
        uy = uy - uy_ref_mean

        dux_dy, dux_dx = np.gradient(ux)
        duy_dy, duy_dx = np.gradient(uy)

        exx = dux_dx
        eyy = duy_dy
        exy = 0.5*(dux_dy + duy_dx)

        rotation_xy = 0.5*(duy_dx - dux_dy)
        if ROTATION_IN_DEGREES:
            rotation_xy = np.degrees(rotation_xy)

        exx_smooth = gaussian_filter(exx, sigma=sigma_smooth)
        eyy_smooth = gaussian_filter(eyy, sigma=sigma_smooth)
        exy_smooth = gaussian_filter(exy, sigma=sigma_smooth)
        rotation_smooth = gaussian_filter(rotation_xy, sigma=sigma_smooth)

        exx_smooth[~material_mask] = np.nan
        eyy_smooth[~material_mask] = np.nan
        exy_smooth[~material_mask] = np.nan
        rotation_smooth[~material_mask] = np.nan

        exx_smooth *= 100
        eyy_smooth *= 100
        exy_smooth *= 100

        return {
            'complex_image1': complex_img1,
            'complex_image2': complex_img2,
            'raw_phase_image1': raw_phase_1,
            'raw_phase_image2': raw_phase_2,
            'phase_image1': phase_image1,
            'phase_image2': phase_image2,
            'u1': ux,
            'u2': uy,
            'strain_xx': exx_smooth,    
            'strain_yy': eyy_smooth,    
            'strain_xy': exy_smooth,    
            'rotation_xy': rotation_smooth
        }
