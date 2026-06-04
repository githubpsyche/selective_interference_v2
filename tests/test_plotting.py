import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb

from selective_interference_v2 import add_phase_bands, light_to_dark_colors


def test_add_phase_bands_groups_contiguous_phase_labels():
    fig, axis = plt.subplots()

    add_phase_bands(axis, ["film", "film", "task", "task", "filler"])

    labels = [text.get_text() for text in axis.texts]
    assert labels == ["Film", "Task", "Filler"]
    assert len(axis.patches) == 3

    plt.close(fig)


def test_light_to_dark_colors_uses_visible_ordered_blue_ramp():
    colors = light_to_dark_colors(4)

    assert colors == ["#d7e8fa", "#86b6e2", "#2c7fb8", "#08306b"]

    rgb = np.asarray([to_rgb(color) for color in colors])
    luminance = rgb @ np.asarray([0.2126, 0.7152, 0.0722])
    assert np.all(np.diff(luminance) < 0)


def test_light_to_dark_colors_handles_empty_and_singleton_requests():
    assert light_to_dark_colors(0) == []
    assert light_to_dark_colors(1) == ["#08306b"]
