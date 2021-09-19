import numpy as np


class Timeline:
    ReferenceTime = np.datetime64('2021-08-18T00:00:00.000000000')
    precision = 's'

    def __init__(self, xls_data):
        Timeline.ReferenceTime = max(Timeline.ReferenceTime, xls_data.time[0])
        self.xls_data = xls_data
        self.sampled_timeline = None
        self.sampled_status = None
        self._create_timeline()

    def _create_timeline(self):
        # Get the time delta
        dt = (self.xls_data.time - Timeline.ReferenceTime)

        if Timeline.precision == 's':
            dt = dt.astype('timedelta64[s]')  # convert ns to s
            self.time_delta = dt
        else:
            dt = dt.astype('timedelta64[ms]')  # convert ns to ms
            self.time_delta = dt + self.millisecond

        self.time_delta = self.time_delta.astype(np.int64)

        self.sampled_timeline = np.arange(0, self.time_delta[-1] + 1, 1)
        self.sampled_status = np.zeros((self.sampled_timeline.size,), dtype=np.int64)
        self.sampled_status[0: self.time_delta[0]] = -1
        self.sampled_status[self.time_delta] = self.xls_data.status
        for itr in range(0, self.time_delta.size - 1, 1):
            self.sampled_status[self.time_delta[itr] + 1: self.time_delta[itr + 1]] = self.xls_data.status[itr]