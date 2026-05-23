import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from selective_interference_v2 import add_phase_bands


def test_add_phase_bands_groups_contiguous_phase_labels():
    fig, axis = plt.subplots()

    add_phase_bands(axis, ["film", "film", "task", "task", "filler"])

    labels = [text.get_text() for text in axis.texts]
    assert labels == ["Film", "Task", "Filler"]
    assert len(axis.patches) == 3

    plt.close(fig)
