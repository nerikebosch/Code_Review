HYDRATION_NEED_ML_PER_KG = 30 # amount of water per kg of the body weight.
ML_TO_LITERS = 1000 # conversion for milliliters to liter.

def calculate_hydration_needs(body_mass, height, activity_level="mid"):
    """
    Computes hydration needs for the user/patient.

    Args:
        body_mass (float): Body mass in kilos.
        height (float): Height in meters.
        activity_level (str): Can be "low", "mid", or "high". Default is "mid".

    Returns:
        (dict): Contains the files:
        BMI (float): Calculated body mass index,
        hydration_L (float): Calculated hydration need in liters.

    Disclaimer:
    - The code does not include it for fever or hot climates.
    - This function is for demo purpose only.
    """

    activity_level = activity_level.lower().strip()

    valid_levels = ["low", "mid", "high"]

    if activity_level not in valid_levels:
        raise ValueError(f"Invalid hydration level: {activity_level}")

    if body_mass <= 0:
        raise ValueError("Weight must be positive")

    if height <= 0:
        raise ValueError("Height must be positive")

    bmi = body_mass / (height ** 2)

    base = HYDRATION_NEED_ML_PER_KG * body_mass / ML_TO_LITERS

    if activity_level == "low":
        factor = 0.9
    elif activity_level == "mid":
        factor = 1.0
    elif activity_level == "high":
        factor = 1.2

    daily_liters = base * factor

    return {
        "BMI": round(bmi, 2),
        "hydration_L": round(daily_liters, 2)
    }
