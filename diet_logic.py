def calculate_bmi(weight, height):
    height_m = height / 100  # convert cm to m
    return round(weight / (height_m ** 2), 2)

def get_sample_indian_diet(goal):
    if goal == "weight_loss_ ":
        return "🥗 Sample Indian Diet (Weight Loss):\n- Breakfast: Poha + Green Tea\n- Lunch: Roti + Sabzi + Dal\n- Dinner: Grilled Paneer + Salad"
    elif goal == "muscle_gain_":
        return "🍗 Sample Indian Diet (Muscle Gain):\n- Breakfast: Eggs + Banana\n- Lunch: Chicken Curry + Rice\n- Dinner: Paneer Bhurji + Chapati"
    elif goal == "PCOS":
        return "🥗 Ideal PCOS Diet Plan (Sample Day):\n- 🕓 Early Morning (on waking):- 1 glass warm water + 1 tsp apple cider vinegar OR 1 soaked methi seeds water "\
        "🍳 Breakfast:- 1 multigrain toast + 2 boiled eggs OR "
    elif goal == "Diabetics":
        return ""
    elif goal == "POST hERNIATED Surgery":
        return ""
    else:
        return "🍽️ Balanced_Diet_🍽️:\n- Breakfast: Idli + Sambhar\n- Lunch: Veg Pulao + Raita\n- Dinner: Khichdi + Curd"

