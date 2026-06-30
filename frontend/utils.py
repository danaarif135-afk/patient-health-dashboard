"""
Frontend Utility Functions

Formatting helpers used throughout
the Streamlit dashboard.
"""

# ==========================================================
# Risk Colors
# ==========================================================

RISK_COLORS = {

    "Low": "green",

    "Moderate": "orange",

    "High": "red"

}


# ==========================================================
# Trend Icons
# ==========================================================

TREND_ICONS = {

    "rising": "📈",

    "falling": "📉",

    "stable": "➖"

}


# ==========================================================
# Trend Color
# ==========================================================

TREND_COLORS = {

    "rising": "#d62728",

    "falling": "#2ca02c",

    "stable": "#1f77b4"

}


# ==========================================================
# Get Risk Color
# ==========================================================

def risk_color(risk):

    return RISK_COLORS.get(

        risk,

        "gray"

    )


# ==========================================================
# Get Trend Icon
# ==========================================================

def trend_icon(trend):

    return TREND_ICONS.get(

        trend,

        "➖"

    )


# ==========================================================
# Trend Color
# ==========================================================

def trend_color(trend):

    return TREND_COLORS.get(

        trend,

        "gray"

    )


# ==========================================================
# Dashboard Metric
# ==========================================================

def metric(label, value, unit=""):

    if value is None:

        return "N/A"

    return f"{value} {unit}".strip()


# ==========================================================
# Percentage Formatter
# ==========================================================

def percentage(value):

    if value is None:

        return "N/A"

    return f"{value:.1f}%"


# ==========================================================
# Round Float
# ==========================================================

def number(value, decimals=2):

    if value is None:

        return "N/A"

    return round(value, decimals)


# ==========================================================
# Patient Name
# ==========================================================

def patient_title(patient):

    return f"Patient {patient['patient_id'][:8]}"


# ==========================================================
# Age
# ==========================================================

def patient_age(patient):

    return f"{patient['age']} years"


# ==========================================================
# Gender
# ==========================================================

def gender(patient):

    g = patient["gender"]

    if g == 1:

        return "Male"

    elif g == 2:

        return "Female"

    return "Unknown"


# ==========================================================
# Summary Card
# ==========================================================

def analytics_summary(analytics):

    icon = trend_icon(

        analytics["trend"]

    )

    return (

        f"{icon} "

        f"{analytics['trend'].capitalize()} "

        f"| Risk: {analytics['risk_band']}"

    )


# ==========================================================
# Status Badge
# ==========================================================

def status_badge(status):

    if status:

        return "🟢 Connected"

    return "🔴 Offline"


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    patient = {

        "patient_id": "123456789",

        "age": 42,

        "gender": 1

    }

    analytics = {

        "trend": "falling",

        "risk_band": "Low"

    }

    print()

    print(patient_title(patient))

    print(patient_age(patient))

    print(gender(patient))

    print(metric(123, 85.4, "mg/dL"))

    print(number(22.567))

    print(risk_color("High"))

    print(trend_icon("falling"))

    print(analytics_summary(analytics))

    print(status_badge(True))