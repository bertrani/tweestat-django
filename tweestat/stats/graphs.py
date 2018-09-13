import configparser
import pygal
from influxdb import InfluxDBClient
from datetime import datetime, timedelta

class Graph:
    def __init__(self, field, start, end):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.client = InfluxDBClient(config["INFLUXDB"]["IP"], 8086, config["INFLUXDB"]["user"],
                                config["INFLUXDB"]["password"], 'tweestat')
        self.field = field

        self.start = datetime.strptime(start, '%Y-%m-%dT%H:%M') - timedelta(hours=2)
        self.end = datetime.strptime(end, '%Y-%m-%dT%H:%M') - timedelta(hours=2)

        self.interval = int((self.end-self.start)/timedelta(minutes=1))/20


    def get_graph(self):
        data = self.get_data()
        max_value = max([value[1] for value in data if value[1] is not None])
        print(max_value)
        graph = pygal.DateTimeLine(
            x_label_rotation=35,
            truncate_label=-1,
            x_value_formatter=lambda dt: dt.strftime('%d.%m.%Y, %H:%M:%S'),
            range=(0, max_value*2),
            title="Mean {} per Tweet".format(self.field))
        graph.add(self.field, data)
        return graph.render_django_response()


    def get_data(self):
        response_data = self.client.query(self.build_query())
        data = [(datetime.strptime(d['time'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=2), d['count']) for d in list(response_data)[0]]
        return data


    def build_query(self):
        query = 'select mean({}) as count from tweestat.autogen.tweet where time > \'{}Z\' and time < \'{}Z\' group by time({}m);'.format(
            self.field, self.start.isoformat(), self.end.isoformat(), int(self.interval))
        return query
