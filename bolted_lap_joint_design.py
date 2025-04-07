import math

# --- Mock IS800 functions (replace with actual IS800 standard formulas if needed) ---
class IS800_2007:
    @staticmethod
    def cl_10_3_3_bolt_shear_capacity(fy, A1, A2, n, k, condition):
        # Simplified shear capacity formula (mock)
        return 0.6 * fy * A1 / 1.25  # 1.25 = partial safety factor

    @staticmethod
    def cl_10_3_4_bolt_bearing_capacity(fu_plate, fu_bolt, t, d, e, p, hole_type, condition):
        # Simplified bearing capacity formula (mock)
        k_b = min(e / (3 * d), p / (3 * d) - 0.25, fu_bolt / fu_plate, 1)
        return 2.5 * k_b * d * t * fu_plate / 1.25


# --- Bolt strength calculator ---
def calculate_bolt_strength(bolt_grade):
    """
    Calculate the ultimate tensile strength and yield strength of the bolt based on its grade.
    :param bolt_grade: Bolt grade (e.g., 4.6, 5.6)
    :return: List containing [ultimate tensile strength, yield strength] of the bolt
    """
    bolt_fu = int(bolt_grade) * 100
    bolt_fy = (bolt_grade - int(bolt_grade)) * bolt_fu
    return [bolt_fu, bolt_fy]


# --- Lap Joint Design Function ---
def design_lap_joint(P, w, t1, t2):
    """
    Design a bolted lap joint connecting two plates.
    :param P: Tensile force in kN
    :param w: Width of the plates in mm
    :param t1: Thickness of plate 1 in mm
    :param t2: Thickness of plate 2 in mm
    :return: Dictionary of design parameters and results
    """

    P_N = P * 1000  # Convert kN to N

    d_list = [10, 12, 16, 20, 24]  # Bolt diameters in mm
    GB_list = [3.6, 4.6, 4.8, 5.6, 5.8]  # Bolt grades
    GP_list = ["E250", "E275", "E300", "E350", "E410"]  # Plate grades

    plate_grades = {
        "E250": (250, 410),
        "E275": (275, 440),
        "E300": (300, 470),
        "E350": (350, 510),
        "E410": (410, 550)
    }

    # Use highest grade plate
    plate_grade = GP_list[-1]
    fy_plate, fu_plate = plate_grades[plate_grade]

    best_design = None
    min_length = float("inf")

    for d in d_list:
        for GB in GB_list:
            bolt_fu, bolt_fy = calculate_bolt_strength(GB)
            A_bolt = math.pi * (d / 2) ** 2  # Area of bolt

            V_b = IS800_2007.cl_10_3_3_bolt_shear_capacity(bolt_fy, A_bolt, A_bolt, 0, 0, 'Field')

            if V_b == 0:
                continue

            N_b = math.ceil(P_N / (V_b * 0.75))  # Safety factor

            if N_b < 2:
                continue

            e = d + 5
            p = d + 10
            g = w / 2
            length_of_connection = w + 2 * e

            V_dpb = IS800_2007.cl_10_3_4_bolt_bearing_capacity(fu_plate, bolt_fy, t1 + t2, d, e, p, 'Standard', 'Field')

            Utilization_ratio = P_N / (N_b * V_b * 0.75)

            if Utilization_ratio <= 1 and length_of_connection < min_length:
                min_length = length_of_connection
                best_design = {
                    "bolt_diameter": d,
                    "bolt_grade": GB,
                    "number_of_bolts": N_b,
                    "pitch_distance": p,
                    "gauge_distance": g,
                    "end_distance": e,
                    "edge_distance": e,
                    "number_of_rows": 1,
                    "number_of_columns": N_b,
                    "hole_diameter": d + 2,
                    "strength_of_connection": round(N_b * V_b * 0.75, 2),
                    "yield_strength_plate_1": fy_plate,
                    "yield_strength_plate_2": fy_plate,
                    "length_of_connection": round(length_of_connection, 2),
                    "efficiency_of_connection": round(Utilization_ratio, 3)
                }

    if best_design is None:
        raise ValueError("No suitable design found that meets the requirements.")

    return best_design


# --- Example usage ---
if __name__ == "__main__":
    P = 100  # kN
    w = 150  # mm
    t1 = 10  # mm
    t2 = 12  # mm

    design = design_lap_joint(P, w, t1, t2)

    print("\n--- Final Lap Joint Design ---")
    for key, value in design.items():
        print(f"{key}: {value}")
