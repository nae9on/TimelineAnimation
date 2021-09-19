from src.helper import count_consecutive

import numpy as np


class Performance:
    def __init__(self, reference, result):
        self.reference = reference
        self.result = result
        self.tp = None
        self.fp = None
        self.fn = None
        self.tn = None
        self.precision = None
        self.sensitivity = None
        self.accuracy = None
        self._calculate_performance()

    def _calculate_performance(self):
        # Trim the timelines to valid range
        min_index = max(self.reference.time_delta[0], self.result.time_delta[0])
        max_index = min(self.reference.time_delta[-1], self.result.time_delta[-1])

        reference_status = self.reference.sampled_status
        result_status = self.result.sampled_status

        self.tp = (reference_status[min_index: max_index] == 1) & (result_status[min_index: max_index] == 1)
        self.fp = (reference_status[min_index: max_index] == 0) & (result_status[min_index: max_index] == 1)
        self.fn = (reference_status[min_index: max_index] == 1) & (result_status[min_index: max_index] == 0)
        self.tn = (reference_status[min_index: max_index] == 0) & (result_status[min_index: max_index] == 0)

        consecutive_fp = count_consecutive(self.fp, 1)

        # Remove false positives longer than 3 minutes and smaller than 10 seconds
        clipped_fp = consecutive_fp[(consecutive_fp > 0) & (consecutive_fp < 1e+10)]

        self.precision = np.sum(self.tp) / (np.sum(self.tp) + np.sum(clipped_fp))
        self.sensitivity = np.sum(self.tp) / (np.sum(self.tp) + np.sum(self.fn))

        self.accuracy = np.sum(self.tp) + np.sum(self.tn)
        self.accuracy = self.accuracy / (np.sum(self.tp) + np.sum(clipped_fp) + np.sum(self.fn) + np.sum(self.tn))

    def print_results(self):
        print("Precision", self.precision)
        print("Sensitivity", self.sensitivity)
        print("Accuracy", self.accuracy)