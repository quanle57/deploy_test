from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from layout.Connection import ConnectionDB


class Popup1Layout(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id_shop = 0

    def update_baemin(self):  # id: baemin
        conn = ConnectionDB()
        conn.openConnect()
        user_baemin = str(self.ids.user_baemin.text)
        pass_baemin = str(self.ids.pass_baemin.text)
        sql = "update site set username = '"+str(user_baemin)+"', password = '"+str(pass_baemin)+"' " \
              "where site_id =1 and shop_id = '"+str(self.id_shop)+"'"
        print(sql)
        conn.updateRecord(sql)
        toast("Data baemin has been updated")
