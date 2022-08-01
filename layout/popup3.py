from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from layout.Connection import ConnectionDB


class Popup3Layout(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id_shop = 0

    def update_yogiyo(self):  # id: yogiyo
        conn = ConnectionDB()
        conn.openConnect()
        
        user_yogiyo = str(self.ids.user_yogiyo.text)
        pass_yogiyo = str(self.ids.pass_yogiyo.text)

        sql = "update site set username = '"+str(user_yogiyo)+"', password = '"+str(pass_yogiyo)+"' " \
              "where site_id =3 and shop_id = '"+str(self.id_shop)+"'"
        print(sql)
        conn.updateRecord(sql)
        toast("Data yogiyo has been updated")
    