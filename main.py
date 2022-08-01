from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore

from layout.login import LoginLayout
from layout.statistic import StatisticsLayout
from layout.inform import InformLayout
from layout.history import HistoryLayout
from layout.popup import ShopLayout

from layout.popup1 import Popup1Layout
from layout.popup2 import Popup2Layout
from layout.popup3 import Popup3Layout

Builder.load_file('ui/login.kv')
Builder.load_file('ui/statistic.kv')
Builder.load_file('ui/inform.kv')
Builder.load_file('ui/history.kv')
Builder.load_file('ui/popup.kv')

Builder.load_file('ui/pop1.kv')
Builder.load_file('ui/pop2.kv')
Builder.load_file('ui/pop3.kv')


class KAKAOApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.popupBaemin = Popup1Layout(name='popupBaemin_layout')
        self.popupCoupang = Popup2Layout(name='popupCoupang_layout')
        self.popupYogiyo = Popup3Layout(name='popupYogiyo_layout')

        self.login = LoginLayout(name='login_layout')
        self.statistic = StatisticsLayout(name='statistic_layout')
        self.information = InformLayout(name='inform_layout')
        self.history = HistoryLayout(name='history_layout')
        self.shop_layout = ShopLayout(name='shop_layout')

        self.screen_manager = ScreenManager()
        store = JsonStore('storage.json')
        profile = store.get('UserInfo')

        if profile['Phone'] == "" and profile["Password"] == "":
            self.screen_manager.add_widget(self.login)
            self.screen_manager.add_widget(self.statistic)
            self.screen_manager.add_widget(self.information)
            self.screen_manager.add_widget(self.shop_layout)
            self.screen_manager.add_widget(self.history)

            self.screen_manager.add_widget(self.popupBaemin)
            self.screen_manager.add_widget(self.popupCoupang)
            self.screen_manager.add_widget(self.popupYogiyo)

        else:
            self.information.ID = profile['ID']
            self.statistic.ID = profile['ID']
            self.history.ID = profile['ID']

            self.screen_manager.add_widget(self.statistic)
            self.screen_manager.add_widget(self.information)
            self.screen_manager.add_widget(self.shop_layout)
            self.screen_manager.add_widget(self.login)
            # self.screen_manager.add_widget(self.statistic)
            self.screen_manager.add_widget(self.history)

            self.screen_manager.add_widget(self.popupBaemin)
            self.screen_manager.add_widget(self.popupCoupang)
            self.screen_manager.add_widget(self.popupYogiyo)

            # self.information.loaddata()
            # self.information.load_shop()
            self.statistic.load_spin()

    def build(self):
        self.icon = 'picture\icon.jpg'
        return self.screen_manager


if __name__ == '__main__':
    # Window.size = (1080/2,2400/2)
    # Window.size = (360, 800)

    KAKAOApp().run()
