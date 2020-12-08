import math
import matplotlib.pyplot as plt
from LoRaSim.SimIntervals import Interval


class Plotter:
    def __init__(self, intervals):
        assert isinstance(intervals, list)
        assert isinstance(intervals[0], tuple)
        assert isinstance(intervals[0][0], Interval)
        assert isinstance(intervals[0][1], list)
        self.intervals = intervals

    def show_plots(self):
        plt.show()

    def plot_rcv_prob(self):
        plt.figure()
        x_vals = []
        p_succ_y = []
        ci_min, ci_max = [], []
        intervals_plot_info = []
        succ, tot = 0, 0

        for interval in self.intervals:
            metadata = interval[0]
            data = interval[1]
            model = metadata.model

            if len(self.intervals) > 1:
                intervals_plot_info.append((metadata.start_time, model.title))

            for sample in data:
                if sample[1]:
                    succ += 1
                tot += 1

                p = succ/tot
                p_succ_y.append(p)
                ci = 1.96*math.sqrt(succ*(tot-succ))/(tot*math.sqrt(tot))
                ci_max.append(p+ci)
                ci_min.append(p-ci)

            x_vals.extend(i[0] for i in data)
            self._plot_recv_rate(data)

        self._plot_interval_lines(intervals_plot_info, max(max(ci_max), max(p_succ_y)))
        plt.fill_between(x_vals, ci_min, ci_max, color='orange', alpha=0.4, label='95% CI')
        plt.plot(x_vals, p_succ_y, label='Success probability')

        plt.title("Reception Probability")
        plt.xlabel("Time (ms)")
        plt.ylabel("Success probability")
        plt.legend()
        plt.tight_layout()
        # plt.ylim([0, 1])
        plt.show()

    def _plot_recv_rate(self, data):
        colors = ['lime' if i[1] else 'r' for i in data]
        plt.scatter(list(i[0] for i in data), [0]*len(data), c=colors, marker='|')

    def _plot_interval_lines(self, intervals, height):
        for time, title in intervals:
            plt.vlines(time, 0, height, linestyle=':', color='gray', linewidth=2)
            plt.text(time, height, title, fontsize=12, color='gray')

    def plot_throughput(self):
        plt.figure()
        x_vals = []
        y_vals = []
        intervals_plot_info = []

        for interval in self.intervals:
            metadata = interval[0]
            data = interval[1]
            model = metadata.model

            if len(self.intervals) > 1:
                intervals_plot_info.append((metadata.start_time, model.title))

            for sample in data:
                if sample[1]:
                    y_vals.append(16/model.tx_time*1000) # !!! TODO !!! use actual packet size
                else:
                    y_vals.append(0)

            x_vals.extend(i[0] for i in data)
            self._plot_recv_rate(data)

        means = []
        for i, y in enumerate(y_vals):
            if i == 0:
                means.append(y)
            else:
                new_m = (means[-1]*i + y)/(i+1)
                means.append(new_m)

        self._plot_interval_lines(intervals_plot_info, max(y_vals))
        plt.scatter(x_vals, y_vals, marker='+', alpha=0.4, label="Istantaneous throughput", c='blue')
        plt.plot(x_vals, means, label="Average Throughput", c='red')

        plt.title("Throughput")
        plt.xlabel("Time (ms)")
        plt.ylabel("Throughput (byte/s)")
        plt.legend()
        plt.tight_layout()
        plt.show()