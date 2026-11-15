import pytest
from movie_tickets import ticket_price, group_discount, snack_combo


# ============================================================================
# Branch Coverage Suite for ticket_price()
# Decision Branches:
# 1. if seat not in SEAT_PRICE (True / False)
# 2. if show_hour < 0 or show_hour > 23 (True[left] / True[right] / False)
# 3. if show_hour < 12 / elif show_hour >= 18 / else (Three-way branch)
# 4. if is_weekend (True / False)
# 5. if age < 3 (True / False)
# 6. if age <= 12 or age >= 60 (True[left] / True[right] / False)
# ============================================================================

class TestTicketPriceBranches:
    """Tests evaluating every decision point and compound condition in ticket_price."""

    # Branch 1: seat validity check
    def test_seat_not_in_price_list_true(self):
        """Branch: seat not in SEAT_PRICE -> True (raises ValueError)."""
        with pytest.raises(ValueError, match="unknown seat"):
            ticket_price("balcony", 20, 14, False)

    def test_seat_in_price_list_false_recliner(self):
        """Branch: seat not in SEAT_PRICE -> False (valid 'recliner' seat)."""
        assert ticket_price("recliner", 25, 14, False) == 400

    def test_seat_in_price_list_false_premium(self):
        """Branch: seat not in SEAT_PRICE -> False (valid 'premium' seat)."""
        assert ticket_price("premium", 25, 14, False) == 250

    # Branch 2: show_hour validation (compound OR condition)
    def test_show_hour_less_than_zero_true(self):
        """Branch: show_hour < 0 -> True (raises ValueError)."""
        with pytest.raises(ValueError, match="invalid show time"):
            ticket_price("regular", 20, -5, False)

    def test_show_hour_greater_than_23_true(self):
        """Branch: show_hour < 0 -> False, show_hour > 23 -> True (boundary 24)."""
        with pytest.raises(ValueError, match="invalid show time"):
            ticket_price("regular", 20, 24, False)

    def test_show_hour_valid_lower_boundary_zero(self):
        """Branch: show_hour validity -> False for both checks (boundary 0)."""
        # 0 is morning (< 12: -50) -> 150 - 50 = 100
        assert ticket_price("regular", 25, 0, False) == 100

    def test_show_hour_valid_upper_boundary_23(self):
        """Branch: show_hour validity -> False for both checks (boundary 23)."""
        # 23 is evening (>= 18: +30) -> 150 + 30 = 180
        assert ticket_price("regular", 25, 23, False) == 180

    # Branch 3: show time pricing tiers (< 12, >= 18, and 12..17)
    def test_show_hour_morning_boundary_11(self):
        """Branch: show_hour < 12 -> True (boundary 11, morning discount -50)."""
        assert ticket_price("regular", 30, 11, False) == 100

    def test_show_hour_afternoon_lower_boundary_12(self):
        """Branch: show_hour < 12 -> False, show_hour >= 18 -> False (boundary 12)."""
        assert ticket_price("regular", 30, 12, False) == 150

    def test_show_hour_afternoon_upper_boundary_17(self):
        """Branch: show_hour < 12 -> False, show_hour >= 18 -> False (boundary 17)."""
        assert ticket_price("regular", 30, 17, False) == 150

    def test_show_hour_evening_boundary_18(self):
        """Branch: show_hour >= 18 -> True (boundary 18, evening surcharge +30)."""
        assert ticket_price("regular", 30, 18, False) == 180

    # Branch 4: weekend surcharge
    def test_is_weekend_true(self):
        """Branch: is_weekend -> True (adds 40 weekend surcharge)."""
        # regular 150 + 40 weekend = 190
        assert ticket_price("regular", 30, 15, True) == 190

    def test_is_weekend_false(self):
        """Branch: is_weekend -> False (no weekend surcharge)."""
        assert ticket_price("regular", 30, 15, False) == 150

    # Branch 5: toddler / infant free admission
    def test_age_under_three_boundary_two(self):
        """Branch: age < 3 -> True (boundary age 2, free admission = 0)."""
        assert ticket_price("regular", 2, 20, True) == 0

    def test_age_under_three_boundary_zero(self):
        """Branch: age < 3 -> True (boundary age 0, free admission = 0)."""
        assert ticket_price("regular", 0, 10, False) == 0

    def test_age_at_least_three_boundary_three(self):
        """Branch: age < 3 -> False (boundary age 3, child discount applies)."""
        # regular 150, child discount -> 150 // 2 = 75
        assert ticket_price("regular", 3, 15, False) == 75

    # Branch 6: age discounts (<= 12 or >= 60)
    def test_age_child_boundary_12(self):
        """Branch: age <= 12 -> True (boundary 12, gets 50% discount)."""
        assert ticket_price("regular", 12, 15, False) == 75

    def test_age_just_above_child_boundary_13(self):
        """Branch: age <= 12 -> False, age >= 60 -> False (boundary 13, full price)."""
        assert ticket_price("regular", 13, 15, False) == 150

    def test_age_just_below_senior_boundary_59(self):
        """Branch: age <= 12 -> False, age >= 60 -> False (boundary 59, full price)."""
        assert ticket_price("regular", 59, 15, False) == 150

    def test_age_senior_boundary_60(self):
        """Branch: age <= 12 -> False, age >= 60 -> True (boundary 60, gets 50% discount)."""
        assert ticket_price("regular", 60, 15, False) == 75


# ============================================================================
# Branch Coverage Suite for group_discount()
# Decision Branches:
# 7. if tickets < 1 (True / False)
# 8. if tickets >= 10 / elif tickets >= 5 / else (Three tiers)
# 9. if is_student_group and discount > 0:
#    - True and True   -> discount += 5
#    - True and False  -> no bonus (student group with tickets < 5)
#    - False and True  -> no bonus (non-student group with tickets >= 5)
#    - False and False -> no bonus (non-student group with tickets < 5)
# ============================================================================

class TestGroupDiscountBranches:
    """Tests evaluating all branch outcomes in group_discount."""

    def test_tickets_less_than_one_boundary_zero(self):
        """Branch: tickets < 1 -> True (boundary 0, raises ValueError)."""
        with pytest.raises(ValueError, match="no tickets"):
            group_discount(0, False)

    def test_tickets_negative_count(self):
        """Branch: tickets < 1 -> True (negative count, raises ValueError)."""
        with pytest.raises(ValueError, match="no tickets"):
            group_discount(-3, True)

    def test_tickets_tier_large_boundary_10_non_student(self):
        """Branch: tickets >= 10 -> True (boundary 10, discount 15%, student=False)."""
        assert group_discount(10, False) == 15

    def test_tickets_tier_large_boundary_10_student(self):
        """
        Branch: tickets >= 10 -> True, is_student_group -> True, discount > 0 -> True.
        Expected: 15 + 5 = 20%.
        """
        assert group_discount(10, True) == 20

    def test_tickets_tier_medium_boundary_5_non_student(self):
        """Branch: tickets >= 5 -> True (boundary 5, discount 10%, student=False)."""
        assert group_discount(5, False) == 10

    def test_tickets_tier_medium_boundary_9_student(self):
        """
        Branch: tickets >= 5 -> True (boundary 9), is_student_group -> True, discount > 0 -> True.
        Expected: 10 + 5 = 15%.
        """
        assert group_discount(9, True) == 15

    def test_tickets_tier_small_boundary_4_non_student(self):
        """Branch: tickets < 5 -> else branch (boundary 4, discount 0%, student=False)."""
        assert group_discount(4, False) == 0

    def test_student_group_with_no_base_discount(self):
        """
        Branch: is_student_group -> True, BUT discount > 0 -> False.
        A student group with fewer than 5 tickets gets 0% base discount,
        so the student bonus branch condition evaluates to False.
        """
        assert group_discount(3, True) == 0

    def test_tickets_tier_small_boundary_1_non_student(self):
        """Branch: tickets = 1 (valid minimum), student=False -> discount = 0%."""
        assert group_discount(1, False) == 0


# ============================================================================
# Branch Coverage Suite for snack_combo()
# Decision Branches:
# 10. if size == "small" / elif size == "medium" / else (Three branches)
# 11. if has_coupon (True / False)
# ============================================================================

class TestSnackComboBranches:
    """Tests evaluating all branch outcomes in snack_combo."""

    def test_snack_size_small_without_coupon(self):
        """Branch: size == 'small' -> True, has_coupon -> False (cost 120)."""
        assert snack_combo("small", False) == 120

    def test_snack_size_small_with_coupon(self):
        """Branch: size == 'small' -> True, has_coupon -> True (120 - 50 = 70)."""
        assert snack_combo("small", True) == 70

    def test_snack_size_medium_without_coupon(self):
        """Branch: size == 'medium' -> True, has_coupon -> False (cost 180)."""
        assert snack_combo("medium", False) == 180

    def test_snack_size_medium_with_coupon(self):
        """Branch: size == 'medium' -> True, has_coupon -> True (180 - 50 = 130)."""
        assert snack_combo("medium", True) == 130

    def test_snack_size_large_without_coupon(self):
        """Branch: size == 'medium' -> False (else: 'large'), has_coupon -> False (cost 250)."""
        assert snack_combo("large", False) == 250

    def test_snack_size_large_with_coupon(self):
        """Branch: else branch ('large'), has_coupon -> True (250 - 50 = 200)."""
        assert snack_combo("large", True) == 200

    def test_snack_size_other_variant_without_coupon(self):
        """Branch: unknown/custom size falls into else branch, has_coupon -> False (cost 250)."""
        assert snack_combo("family_pack", False) == 250

