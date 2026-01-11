HYDRATION_NEED_ML_PER_KG = 30 # amount of water per kg of the body weight.
ML_TO_LITERS = 1000 # conversion for milliliters to liter.

def check_hydro(bm, ht, act_lvl="mid"):
    """
    Computes hydration needs for the user/patient.

    Args:
        bm (float): Body mass in kilos.
        ht (float): Height in meters.
        act_lvl (str): Can be "low", "mid", or "high". Default is "mid".

    Returns:
        (dict):
        BMI (float): Calculated body mass index.
        hydration_L (float): Calculated hydration need in liters.

    Disclaimer:
    - The code does not include it for fever or hot climates.
    - This function is for demo purpose only.
    """

    valid_levels = ["low", "mid", "high"]

    if act_lvl not in valid_levels:
        raise ValueError(f"Invalid hydration level: {act_lvl}")

    if bm <= 0:
        raise ValueError("Weight must be positive")

    if ht <= 0:
        raise ValueError("Height must be positive")

    bmi = bm / (ht ** 2)

    base = HYDRATION_NEED_ML_PER_KG * bm / ML_TO_LITERS

    if act_lvl == "low":
        factor = 0.9
    elif act_lvl == "mid":
        factor = 1.0
    elif act_lvl == "high":
        factor = 1.2

    daily_liters = base * factor

    return {
        "BMI": round(bmi, 2),
        "hydration_L": round(daily_liters, 2)
    }
