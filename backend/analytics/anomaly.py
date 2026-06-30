"""
Anomaly Detection
"""

import numpy as np


class AnomalyDetector:

    @staticmethod
    def detect(values):

        if len(values) < 2:

            return []

        mean = np.mean(values)

        std = np.std(values)

        upper = mean + (2 * std)

        lower = mean - (2 * std)

        anomalies = [

            value

            for value in values

            if value > upper or value < lower

        ]

        return anomalies