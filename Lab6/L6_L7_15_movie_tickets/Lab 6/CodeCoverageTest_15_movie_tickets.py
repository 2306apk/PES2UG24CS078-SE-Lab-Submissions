import pytest
from movie_tickets import ticket_price, group_discount, snack_combo


# ============================================================================
# Tests for ticket_price(seat, age, show_hour, is_weekend)
# ============================================================================

def test_ticket_price_invalid_seat():
    """Verify that ValueError is raised for an unrecognized seat type."""
    with pytest.raises(ValueError, match="unknown seat"):
        ticket_price("vip_box", 25, 14, False)


def test_ticket_price_invalid_show_hour_negative():
    """Verify that ValueError is raised when show_hour is less than 0."""
    with pytest.raises(ValueError, match="invalid show time"):
        ticket_price("regular", 25, -1, False)


def test_ticket_price_invalid_show_hour_exceeds_day():
    """Verify that ValueError is raised when show_hour is greater than 23."""
    with pytest.raises(ValueError, match="invalid show time"):
        ticket_price("regular", 25, 24, False)


def test_ticket_price_regular_morning_weekday_adult():
    """
    Regular seat (150), morning show (< 12: -50), weekday, adult (25).
    Expected price: 150 - 50 = 100.
    """
    assert ticket_price("regular", 25, 10, False) == 100


def test_ticket_price_premium_evening_weekday_adult():
    """
    Premium seat (250), evening show (>= 18: +30), weekday, adult (35).
    Expected price: 250 + 30 = 280.
    """
    assert ticket_price("premium", 35, 19, False) == 280


def test_ticket_price_recliner_afternoon_weekend_adult():
    """
    Recliner seat (400), afternoon (no time adjustment), weekend (+40), adult (30).
    Expected price: 400 + 40 = 440.
    """
    assert ticket_price("recliner", 30, 15, True) == 440


def test_ticket_price_infant_free_admission():
    """Verify that children under 3 receive free admission (price = 0)."""
    assert ticket_price("regular", 2, 14, False) == 0


def test_ticket_price_child_discount():
    """
    Child age (<= 12) receives 50% discount.
    Regular (150) afternoon weekday -> 150 // 2 = 75.
    """
    assert ticket_price("regular", 10, 15, False) == 75


def test_ticket_price_senior_discount():
    """
    Senior citizen age (>= 60) receives 50% discount.
    Regular (150) afternoon weekday -> 150 // 2 = 75.
    """
    assert ticket_price("regular", 65, 15, False) == 75


# ============================================================================
# Tests for group_discount(tickets, is_student_group)
# ============================================================================

def test_group_discount_invalid_ticket_count():
    """Verify that ValueError is raised when ticket count is less than 1."""
    with pytest.raises(ValueError, match="no tickets"):
        group_discount(0, False)


def test_group_discount_large_group_non_student():
    """Large group (>= 10 tickets) receives 15% discount."""
    assert group_discount(12, False) == 15


def test_group_discount_medium_group_non_student():
    """Medium group (5 to 9 tickets) receives 10% discount."""
    assert group_discount(6, False) == 10


def test_group_discount_small_group_non_student():
    """Small group (< 5 tickets) receives 0% discount."""
    assert group_discount(3, False) == 0


def test_group_discount_student_bonus():
    """Student group with discount > 0 gets an additional 5% discount."""
    assert group_discount(10, True) == 20


# ============================================================================
# Tests for snack_combo(size, has_coupon)
# ============================================================================

def test_snack_combo_small_without_coupon():
    """Small snack combo without coupon costs 120."""
    assert snack_combo("small", False) == 120


def test_snack_combo_medium_without_coupon():
    """Medium snack combo without coupon costs 180."""
    assert snack_combo("medium", False) == 180


def test_snack_combo_large_without_coupon():
    """Other/large snack combo without coupon costs 250."""
    assert snack_combo("large", False) == 250


def test_snack_combo_with_coupon_discount():
    """Snack combo with coupon receives 50 discount."""
    assert snack_combo("small", True) == 70

