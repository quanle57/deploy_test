from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from layout.Connection import ConnectionDB


class Popup2Layout(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.id_shop = 0

    def update_coupang(self):  # id: coupang
        conn = ConnectionDB()
        conn.openConnect()
        user_coupang = str(self.ids.user_coupang.text)
        pass_coupang = str(self.ids.pass_coupang.text)
        sql = "update site set username = '"+str(user_coupang)+"', password = '"+str(pass_coupang)+"' " \
              "where site_id =2 and shop_id = '"+str(self.id_shop)+"'"
        print(sql)
        conn.updateRecord(sql)
        toast("Data coupang has been updated")
