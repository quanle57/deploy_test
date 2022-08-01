from logging import root
from kivy.uix.screenmanager import Screen
from layout.Connection import ConnectionDB
from kivy.app import App
from kivymd.toast import toast


class ShopLayout(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.root = root
        self.name_shop = ""
        self.id_shop = 0

        self.sitename_baemin = ""
        self.sitepassword_baemin = ""

        self.sitename_coupang = ""
        self.sitepassword_coupang = ""

        self.sitename_yogiyo = ""
        self.sitepassword_yogiyo = ""

        self.pop1_layout = None
        self.pop2_layout = None
        self.pop3_layout = None

        self.baemin = None
        self.coupang = None
        self.yogiyo = None

        self.app = App.get_running_app()
        self.db = ConnectionDB()
        self.db.openConnect()

    # -------------------------------------------------------- UPDATE DATA -------------------------------------------------------- #
    def updatedata(self):

        if self.ids.update.text == "완료":
            sql = "select * from shop where id = '" + str(self.id_shop) + "'"
            # print(sql)
            dataset = self.db.loadRecords(sql)
            for data in dataset:
                if data.get('id') == self.id_shop:
                    shop_name = self.ids.shop.text
                    conn = "update shop set name = '" + str(shop_name) + "' where id = '" + str(self.id_shop) + "'"
                    self.db.updateRecord(conn)
                    toast('Update Successfully')

        else:
            self.ids.update.text = "완료"

    # -------------------------------------------------------- DELETE DATA -------------------------------------------------------- #
    def deletedata(self):
        sql = "delete from shop where id = '" + str(self.id_shop) + "'"
        self.db.deleteRecord(sql)

        sql = "delete from site where shop_id = '" + str(self.id_shop) + "'"
        self.db.deleteRecord(sql)

        toast('Data has been deleted')
        self.app.screen_manager.get_screen('inform_layout').remove_shop(self)

    # -------------------------------------------------------- BAEMIN -------------------------------------------------------- #
    def load_site_baemin(self):

        sql = "select username, password from site where site_id = 1 and shop_id = '" + str(self.id_shop) + "'"
        dataset = self.db.loadRecords(sql)
        if dataset[0].get("username") is not None and dataset[0].get("password") is not None:
            for data in dataset:
                self.pop1_layout.ids.user_baemin.text = data.get("username")
                self.pop1_layout.ids.pass_baemin.text = data.get("password")

        self.baemin.open()

    # -------------------------------------------------------- COUPANG -------------------------------------------------------- #
    def load_site_coupang(self):
        sql = "select username, password from site where site_id = 2 and shop_id = '" + str(self.id_shop) + "'"
        dataset = self.db.loadRecords(sql)
        if dataset[0].get("username") is not None and dataset[0].get("password") is not None:
            for data in dataset:
                self.pop2_layout.ids.user_coupang.text = data.get("username")
                self.pop2_layout.ids.pass_coupang.text = data.get("password")
        self.coupang.open()

    # -------------------------------------------------------- YOGIYO -------------------------------------------------------- #
    def load_site_yogiyo(self):
        sql = "select username, password from site where site_id = 3 and shop_id = '" + str(self.id_shop) + "'"
        dataset = self.db.loadRecords(sql)
        if dataset[0].get("username") is not None and dataset[0].get("password") is not None:
            for data in dataset:
                self.pop3_layout.ids.user_yogiyo.text = data.get("username")
                self.pop3_layout.ids.pass_yogiyo.text = data.get("password")
        self.yogiyo.open()

    def dismiss_yogiyo(self):
        self.app.screen_manager.get_screen('popupYogiyo_layout').ids['popup3'].clear_widgets()
        self.yogiyo.dismiss()
