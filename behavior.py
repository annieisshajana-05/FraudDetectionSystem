def behavior_check(amount, avg_amount):
    """
    Checks if the transaction amount is unusual compared to user's normal behavior
    Returns:
        True  -> Suspicious behavior
        False -> Normal behavior
    """

    # Avoid division issues
    if avg_amount == 0:
        return False

    # Calculate ratio
    ratio = amount / avg_amount

    # Behavior rules
    if ratio > 5:
        return True   # Highly suspicious
    elif ratio > 3:
        return True   # Suspicious
    elif ratio > 2:
        return True   # Slightly suspicious

    return False