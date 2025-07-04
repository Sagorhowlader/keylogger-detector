from threading import Timer

import psutil


class PerformanceMonitor:
    def __init__(self, interval):
        self.running = True
        self.interval = interval

    def start(self):
        if self.running:
            self.schedule_performance()

    def stop(self):
        self.running = False

    def performance_collect(self):
        cpu = psutil.cpu_percent(interval=self.interval)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_io_counters().write_bytes
        net_io = psutil.net_io_counters()
        net_sent = net_io.bytes_sent
        net_recv = net_io.bytes_recv
        process_count = len(psutil.pids())

        return [cpu, ram, disk, net_sent, net_recv, process_count]

    def schedule_performance(self):
        Timer(self.interval, self.performance_collect).start()
