from matplotlib import pyplot as plt
from matplotlib import animation

import numpy as np


class Animation:
    window_length_minutes = 30
    time_shift_minutes = 1

    def __init__(self, reference, result, precision):
        self.ref = reference
        self.result = result
        self.precision = precision
        self._set_parameters()

        # Animation parameters
        self.window_length = None
        self.time_shift = None
        self._set_parameters()

    def _set_parameters(self):
        if self.precision == 's':
            self.window_length = int(Animation.window_length_minutes * 60)
            self.time_shift = int(Animation.time_shift_minutes * 60)
        else:
            self.window_length = int(Animation.window_length_minutes * 60 * 1000)
            self.time_shift = int(Animation.time_shift_minutes * 60 * 1000)

    def create_animation(self, save=False, debug=False):

        print('Running animation')

        # Plotting
        # https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/
        fig = plt.figure(figsize=(20, 4))
        ax = plt.axes(xlim=(0, self.window_length), ylim=(-8, 6))
        ax.set_xlabel('Time window in ' + self.precision)
        ax.set_ylabel('Status')
        ref, = ax.plot([], [], lw=1, color='k')
        result, = ax.plot([], [], lw=1, color='b')
        fp, = ax.plot([], [], lw=1, color='r')
        fn, = ax.plot([], [], lw=1, color='y')
        label = ax.text(2, 4, '', ha='left', va='center', fontsize=10, color="Black")
        ax.legend([ref, result, fp, fn], ['Reference', 'Result', 'FP', 'FN'])

        # initialization function: plot the background of each frame
        def init():
            ref.set_data([], [])
            result.set_data([], [])
            fp.set_data([], [])
            fn.set_data([], [])
            label.set_text('')
            return ref, result, fp, fn, label

        # Trim the timelines to valid range
        min_index = max(self.ref.time_delta[0], self.result.time_delta[0])
        max_index = min(self.ref.time_delta[-1], self.result.time_delta[-1])

        false_positives = np.maximum(self.result.sampled_status[0: max_index] - self.ref.sampled_status[0: max_index], 0)
        false_negatives = np.minimum(self.result.sampled_status[0: max_index] - self.ref.sampled_status[0: max_index], 0)

        def animate(i):
            t_begin = int(i * self.time_shift)
            t_end = min(int(i * self.time_shift + self.window_length), max_index-1)

            if debug:
                print(t_begin, t_end)

            y_ref = self.ref.sampled_status[t_begin:t_end]
            y_res = self.result.sampled_status[t_begin:t_end] - 2
            y_fp = false_positives[t_begin:t_end] - 4
            y_fn = false_negatives[t_begin:t_end] - 6

            xref = np.arange(0, y_ref.size)

            ref.set_data(xref, y_ref)
            result.set_data(xref, y_res)
            fp.set_data(xref, y_fp)
            fn.set_data(xref, y_fn)
            label.set_text('Time range = '+str(t_begin)+str(' - ')+str(t_end))
            return ref, result, fp, fn, label

        anim = animation.FuncAnimation(fig=fig, func=animate,
                                       frames=int(self.ref.sampled_timeline.size / self.time_shift),
                                       init_func=init, interval=200, blit=True)

        if save:
            anim.save('./timeline.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
        else:
            plt.show()