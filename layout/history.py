from kivy.uix.screenmanager import Screen
import datetime
from kivy.uix.button import Button


class HistoryLayout(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        # 2022-06-16 (목) 보고서
        str_date = self.ids.history.children[-1].text.split("(목)")[0]
        datem = datetime.datetime.strptime(str_date, "%Y-%m-%d ")

        # for i in range((datetime.datetime.today() - datem).days):
        for i in range(39):
            datem += datetime.timedelta(days=1)

            button = Button(text=str(datem.strftime('%Y-%m-%d')) + " (목) 보고서",
                            font_name='font\IBMPlexSansKR-Bold.ttf',
                            color=(1, 1, 1, 1),
                            background_color=(51 / 255, 119 / 255, 106 / 255, 1),
                            background_normal='',
                            size_hint=(0.9, 0.2),
                            pos_hint={'center_x': 0.5})

            # self.ids.history.add_widget(button, len(self.ids.history.children))

    def check(self):
        print("checkkkkkkkkkkkkkkkkk")
