"""
--- Ångström ---
Cell class for Ångström Python package.
"""
import numpy as np


class Cell:
    """Cell class for unit cell and periodic boundary operations."""
    def __init__(self, cellpar):
        """Initialize cell for a molecule with cell parameters. Cell angles in degrees. """
        self.a, self.b, self.c = cellpar[:3]
        self.alpha, self.beta, self.gamma = [np.radians(i) for i in cellpar[3:]]

    def calculate_volume(self):
        """ Calculates cell volume. """
        volume = 1 - np.cos(self.alpha)**2 - np.cos(self.beta)**2 - np.cos(self.gamma)**2
        volume += 2 * np.cos(self.alpha) * np.cos(self.beta) * np.cos(self.gamma)
        self.volume = self.a * self.b * self.c * np.sqrt(volume)
        self.frac_volume = volume / (self.a * self.b * self.c)

    def calculate_vectors(self):
        """ Calculates cell vectors. """
        x_v = [self.a, 0, 0]
        y_v = [self.b * np.cos(self.gamma), self.b * np.sin(self.gamma), 0]
        z_v = [0.0] * 3
        z_v[0] = self.c * np.cos(self.beta)
        z_v[1] = (self.c * self.b * np.cos(self.alpha) - y_v[0] * z_v[0]) / y_v[1]
        z_v[2] = np.sqrt(self.c * self.c - z_v[0] * z_v[0] - z_v[1] * z_v[1])
        self.vectors = [x_v, y_v, z_v]
