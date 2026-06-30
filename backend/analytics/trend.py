"""
Trend Analysis
"""

import numpy as np


class TrendAnalyzer:

    @staticmethod
    def detect(values):

        if len(values) < 2:
            return "stable"

        x = np.arange(len(values))

        slope = np.polyfit(x, values, 1)[0]

        if slope > 0.5:
            return "rising"

        elif slope < -0.5:
            return "falling"

        return "stable"