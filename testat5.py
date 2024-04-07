import config
import sqlite3
import matplotlib.pyplot as plt

class SensorStatistic:
    def __init__(self,db:str)->None:
        self.db = db
        self.conn = sqlite3.connect(self.db, check_same_thread=False)
        self.cur = self.conn.cursor()


    def _get(self):
        self.conn.commit()
        self.cur.execute("SELECT strftime('%Y-%m-%d %H:%M:00', datetime(tstamp, 'unixepoch')) AS datum, COUNT(*) AS nachrichten_anzahl FROM sensor_data GROUP BY datum ORDER BY datum;")
        return self.cur.fetchall()
    

    def create_plot(self):
        data=self._get()
        x_values = [item[0] for item in data]
        y_values = [item[1] for item in data]
        plt.plot(x_values, y_values, marker='o', linestyle='-')
        plt.xlabel('Time')
        plt.ylabel('Count')
        plt.title('Data per hour')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    sensor = SensorStatistic(config.DB_NAME)
    sensor.create_plot()
    