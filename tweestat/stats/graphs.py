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

        self.start = datetime.strptime(start, '%Y-%m-%dT%H:%M')
        self.end = datetime.strptime(end, '%Y-%m-%dT%H:%M')

        self.interval = int((self.end-self.start)/timedelta(minutes=1))/20


    def get_graph(self):
        data = self.get_data()
        if data:
            max_value = max([value[1] for value in data if value[1] is not None])
        else:
            max_value = 0.5
        print(max_value)
        graph = pygal.DateTimeLine(
            x_label_rotation=35,
            truncate_label=-1,
            x_value_formatter=lambda dt: dt.strftime('%d.%m.%Y, %H:%M:%S'),
            range=(0, max_value*2),
            title="Share of Tweets for which \"{}\" is true or average for properties with counts".format(self.field))
        graph.add(self.field, data)
        return graph.render_django_response()


    def get_data(self):
        response_data = self.client.query(self.build_query())
        if list(response_data):
            data = [(datetime.strptime(d['time'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=2), d['count']) for d in list(response_data)[0]]
        else:
            data = None
        return data


    def build_query(self):
        start = self.start - timedelta(hours=2)
        end = self.end - timedelta(hours=2)
        query = 'select mean({}) as count from tweestat.autogen.tweet where time > \'{}Z\' and time < \'{}Z\' group by time({}m);'.format(
            self.field, start.isoformat(), end.isoformat(), int(self.interval))
        return query
