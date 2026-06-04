import numpy as np
import pytest

from selective_interference_v2 import periodic_cue_mask


def test_periodic_cue_mask_schedules_after_requested_attempts():
    mask = np.asarray(
        periodic_cue_mask(
            max_recall=12,
            cue_interval=4,
            first_cue_after=4,
        ),
        dtype=bool,
    )
    cue_attempts = np.flatnonzero(mask) + 1
    np.testing.assert_array_equal(cue_attempts, np.array([4, 8, 12]))


@pytest.mark.parametrize(
    ("cue_interval", "first_cue_after"),
    [(0, 4), (4, 0)],
)
def test_periodic_cue_mask_rejects_invalid_schedule(
    cue_interval,
    first_cue_after,
):
    with pytest.raises(ValueError):
        periodic_cue_mask(
            max_recall=12,
            cue_interval=cue_interval,
            first_cue_after=first_cue_after,
        )
