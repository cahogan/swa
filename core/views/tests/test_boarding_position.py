import pytest
from core.views import get_boarding_position


class TestGetBoardingPosition:
    @pytest.mark.parametrize(
            ("current_bookings", "expected_group", "expected_number"),
            [
                (0, "A", 1), (1, "A", 2), (9, "A", 10),
                (10, "B", 1), (11, "B", 2), (19, "B", 10),
            ]
    )
    def test_returns_boarding_position(self, current_bookings, expected_group, expected_number):
        group, number = get_boarding_position(current_bookings)
        assert group == expected_group
        assert number == expected_number
