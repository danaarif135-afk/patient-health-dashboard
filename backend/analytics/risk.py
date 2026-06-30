"""
Risk Classification
"""


class RiskCalculator:

    @staticmethod
    def calculate(anomaly_count):

        if anomaly_count >= 3:

            return "High"

        elif anomaly_count >= 1:

            return "Moderate"

        return "Low"