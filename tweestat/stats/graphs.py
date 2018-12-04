import configparser
import pygal
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
from pygal.style import DefaultStyle


class Graph:
    def __init__(self, field, start, end):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.client = InfluxDBClient(config["INFLUXDB"]["IP"], 8086, config["INFLUXDB"]["user"],
                                config["INFLUXDB"]["password"], 'tweestat')
        self.field = field

        self.start = datetime.strptime(start, '%Y-%m-%dT%H:%M')
        self.end = datetime.strptime(end, '%Y-%m-%dT%H:%M')

        if self.end-self.start >= timedelta(minutes=120):
            self.interval = int((self.end-self.start)/timedelta(minutes=1))/40
        else:
            self.interval = 1

        self.field_name = self.get_variable()


    def get_graph(self):
        data = self.get_data()
        if data:
            max_value = max([value[1] for value in data if value[1] is not None])
        else:
            max_value = 0.5

        my_style = DefaultStyle()
        my_style.font_family = 'googlefont:Roboto'
        my_style.foreground = 'black'
        my_style.foreground_strong = 'white'
        my_style.title_font_size = 18
        my_style.background = "#4285f4"

        if max_value <= 1 and max_value >= 0.5:
            my_range = (0, 1)
        else:
            my_range = (0, max_value * 2)
        graph = pygal.DateTimeLine(
            #x_label_rotation=90,
            #truncate_label=11,
            x_value_formatter=lambda dt: dt.strftime('%d.%m.%Y, %H:%M:%S'),
            range=my_range,
            title="{} \n From {} to {}".format(self.field_name, self.start, self.end),
            style = my_style,
            show_legend = False,
            interpolate = 'cubic',
            dots_size=2
        )
        graph.add(self.field, data)
        return graph.render_django_response()

    def get_data(self):
        response_data = self.client.query(self.build_query())
        if list(response_data):
            data = [(datetime.strptime(d['time'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=1), d['count']) for d in list(response_data)[0]]
        else:
            data = None
        return data

    def build_query(self):
        start = self.start - timedelta(hours=2)
        end = self.end - timedelta(hours=2)
        query = 'select mean({}) as count from tweestat.autogen.tweet where time > \'{}Z\' and time < \'{}Z\' group by time({}m);'.format(
            self.field, start.isoformat(), end.isoformat(), int(self.interval))
        return query

    def get_variable(self):
        if self.field == "is_retweeted":
            return "Fraction of Tweets which are retweeted"
        if self.field == "is_quote":
            return "Fraction of Tweets which are quotes"
        elif self.field == "is_sensitive":
            return "Fraction of Tweets which are marked as senstive"
        elif self.field == "has_place":
            return "Fraction of Tweets with an associated place"
        elif self.field == "has_coordinates":
            return "Fraction of Tweets with associated coordinates"
        elif self.field == "no_hashtags":
            return "Average number of Hashtags per Tweet"
        elif self.field == "no_urls":
            return "Average number of URLs per Tweet"
        elif self.field == "no_characters":
            return "verage number of characters per Tweet"
        elif self.field == "lang_de":
            return "Fraction of german Tweets"
        elif self.field == "lang_en":
            return "Fraction of english Tweets"
        elif self.field == "lang_es":
            return "Fraction of spanish Tweets"
        elif self.field == "lang_fr":
            return "Fraction of french Tweets"
        elif self.field == "lang_ja":
            return "Fraction of japanese Tweets"
        elif self.field == "lang_ru":
            return "Fraction of russian Tweets"
        elif self.field == "source_android":
            return "Fraction of Tweets which are send from an Android device"
        elif self.field == "source_iphone":
            return "Fraction of Tweets which send from an iPhone"
        elif self.field == "source_ipad":
            return "Fraction of Tweets which send from an iPad"
        elif self.field == "source_web":
            return "Fraction of Tweets which are send from the web client"
        elif self.field == "usr_favourites":
            return "Average amount of Tweets an active user has favourited"
        elif self.field == "usr_followers":
            return "Average amount of followers an active user has"
        elif self.field == "usr_friends":
            return "Average amount of friends an active user has"
        elif self.field == "usr_statuses":
            return "Average amount of total Tweets an active user has tweeted"
        elif self.field == "usr_lang_de":
            return "Fraction of active users who have set german as their language"
        elif self.field == "usr_lang_en":
            return "Fraction of active users who have set english as their language"
        elif self.field == "usr_lang_es":
            return "Fraction of active users who have set spanish as their language"
        elif self.field == "usr_lang_fr":
            return "Fraction of active users who have set french as their language"
        elif self.field == "usr_lang_ja":
            return "Fraction of active users who have set japanese as their language"
        elif self.field == "usr_lang_ru":
            return "Fraction of active users who have set russian as their language"
        elif self.field == "total_tweets":
            return "Total amount of Tweets sampled from the Twitter API per minute"
        else:
            return "Unknown Variable"


