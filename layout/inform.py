from kivymd.toast import toast
from kivy.uix.screenmanager import Screen
from kivy.app import App
from layout.Connection import ConnectionDB
from kivy.storage.jsonstore import JsonStore
from layout.popup import ShopLayout

from kivy.factory import Factory
from layout.popup1 import Popup1Layout
from layout.popup2 import Popup2Layout
from layout.popup3 import Popup3Layout


class InformLayout(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ID = ""
        self.len_shop = 0
        self.app = App.get_running_app()
        self.store = JsonStore('storage.json')

        self.db = ConnectionDB()
        self.db.openConnect()

    ########################################################## LOAD DATA ##########################################################
    def load_statistic(self):
        self.app.root.current = 'statistic_layout'
        self.manager.get_screen('statistic_layout').load_spin()

    def loaddata(self):
        if self.ID != "":
            self.db.openConnect()
            sql = "SELECT name,phone FROM admin where ID = '" + str(self.ID) + "'"
            self.result = self.db.loadRecord(sql)
            self.ids.name.text = self.result['name']
            self.ids.phone.text = self.result['phone']
        else:
            self.ids.name.text = self.result['name']
            self.ids.phone.text = self.result['phone']

    ############################################## BUTTON LOGOUT CLEAR INFORMATION LOGIN ##########################################

    def logout(self):
        self.store.put('UserInfo', ID='', Phone='', Password='')
        self.app.screen_manager.get_screen('login_layout').ids['phone'].text = ''
        self.app.screen_manager.get_screen('login_layout').ids['password'].text = ''
        self.ids.inform.clear_widgets()

    ################################################## BUTTON UPDATE DATA FROM MYSQL ##############################################

    def update(self):
        input_name = self.ids.name.text
        input_phone = self.ids.phone.text
        if input_name == '' or input_phone == '':
            toast("Please check information before changing")
        else:
            sql = "update admin set name = '" + input_name + "', phone = '" + input_phone + "' where id  = '" + str(
                self.ID) + "'"
            self.db.updateRecord(sql)
            toast('Your account has been updated !')

    ###################################################### LOAD SITE SHOP #########################################################
    def remove_shop(self, layout):
        self.ids.inform.remove_widget(layout)
        self.len_shop = self.len_shop - 1
        self.ids.sizebox.height = self.len_shop * 300 + 200  # 2*300 + 200 = 800
        self.ids.inform.height = self.len_shop * 300  # 2*300

    def add_shop(self):

        if self.ID != '':
            # ------------------------------------------------ INSERT INTO SHOP DATA ------------------------------------------- #

            sql = "insert into shop (user_id, name) values ('" + str(self.ID) + "', '스쿨푸드 신림')"  # user_id, site_id
            self.db.insertRecord(sql)

            data = "select MAX(id) as maxid from shop where user_id = '" + str(self.ID) + "'"
            id_shop = self.db.loadRecord(data).get('maxid')

            # ------------------------------------------------ INSERT INTO SITE DATA ------------------------------------------- #

            sql1 = "insert into site (user_id, shop_id, site_id, name, username, password) values ('" + str(
                self.ID) + "', '" + str(id_shop) + "', '1', '배민', '', '')"  # id_shop 1
            baemin_site = self.db.insertRecord(sql1)

            sql2 = "insert into site (user_id, shop_id, site_id, name, username, password) values ('" + str(
                self.ID) + "', '" + str(id_shop) + "', '2', '쿠팡이츠', '', '')"  # id_shop 2
            coupang_site = self.db.insertRecord(sql2)

            sql3 = "insert into site (user_id, shop_id, site_id, name, username, password) values ('" + str(
                self.ID) + "', '" + str(id_shop) + "', '3', '요기요', '', '')"  # id_shop 3
            yogiyo_site = self.db.insertRecord(sql3)

            shop_layout = ShopLayout()
            pop1_layout = Popup1Layout()
            pop2_layout = Popup2Layout()
            pop3_layout = Popup3Layout()

            pop1_layout.id_shop = id_shop
            pop2_layout.id_shop = id_shop
            pop3_layout.id_shop = id_shop

            shop = "SELECT * FROM shop ORDER BY id DESC LIMIT 0,1"
            shop1 = self.db.loadRecord(shop)

            shop_layout.ids.shop.text = shop1.get('name')
            shop_layout.id_shop = id_shop

            sql4 = "select * from site order by shop_id desc limit 3"
            sites = self.db.loadRecords(sql4)

            for site in sites:
                # print(site)
                if site.get('site_id') == 1:  # baemin
                    shop_layout.baemin = Factory.MyPopup1()

                    shop_layout.sitename_baemin = site.get('username')
                    shop_layout.sitepassword_baemin = site.get('password')
                    shop_layout.pop1_layout = pop1_layout

                    shop_layout.baemin.ids.float.add_widget(shop_layout.pop1_layout)  ######

                if site.get('site_id') == 2:  # coupang
                    shop_layout.coupang = Factory.MyPopup2()
                    shop_layout.sitename_coupang = site.get('username')
                    shop_layout.sitepassword_coupang = site.get('password')

                    shop_layout.pop2_layout = pop2_layout
                    shop_layout.coupang.ids.float2.add_widget(shop_layout.pop2_layout)  ########

                if site.get('site_id') == 3:  # yogiyo
                    shop_layout.yogiyo = Factory.MyPopup3()
                    shop_layout.sitename_yogiyo = site.get('username')
                    shop_layout.sitepassword_yogiyo = site.get('password')

                    shop_layout.pop3_layout = pop3_layout
                    shop_layout.yogiyo.ids.float3.add_widget(shop_layout.pop3_layout)  ######

            self.ids.inform.add_widget(shop_layout)

            self.len_shop = self.len_shop + 1
            self.ids.sizebox.height = self.len_shop * 300 + 200  # 2*300 + 200 = 800
            self.ids.inform.height = self.len_shop * 300  # 2*300
            toast('New data has been add')

    def load_shop(self):
        if self.ID != "":
            self.db.openConnect()
            sql1 = "SELECT id,name FROM shop where user_id = '" + str(self.ID) + "'"
            shops = self.db.loadRecords(sql1)
            print(str(len(shops)) + str(" shop has been founded"))  ### 2
            self.len_shop = len(shops)
            self.ids.sizebox.height = len(shops) * 300 + 200  # 2*300 + 200 = 800
            self.ids.inform.height = len(shops) * 300  # 2*300
            
            self.ids.inform.clear_widgets()

            for shop in shops:
                shop_layout = ShopLayout()

                pop1_layout = Popup1Layout()
                pop2_layout = Popup2Layout()
                pop3_layout = Popup3Layout()
                # shoplayout
                shop_layout.ids.shop.text = shop.get('name')
                shop_layout.id_shop = shop.get('id')
                # popup
                pop1_layout.id_shop = shop.get('id')
                pop2_layout.id_shop = shop.get('id')
                pop3_layout.id_shop = shop.get('id')

                shop_layout.name_shop = shop.get('name')

                sql = "select * from site where shop_id = '" + str(shop.get('id')) + "'"
                sites = self.db.loadRecords(sql)

                for site in sites:
                    # print(site)
                    if site.get('site_id') == 1:  # baemin
                        shop_layout.baemin = Factory.MyPopup1()

                        shop_layout.sitename_baemin = site.get('username')
                        shop_layout.sitepassword_baemin = site.get('password')
                        shop_layout.pop1_layout = pop1_layout

                        shop_layout.baemin.ids.float.add_widget(shop_layout.pop1_layout)

                    if site.get('site_id') == 2:  # coupang
                        shop_layout.coupang = Factory.MyPopup2()
                        shop_layout.sitename_coupang = site.get('username')
                        shop_layout.sitepassword_coupang = site.get('password')

                        shop_layout.pop2_layout = pop2_layout
                        shop_layout.coupang.ids.float2.add_widget(shop_layout.pop2_layout)

                    if site.get('site_id') == 3:  # yogiyo
                        shop_layout.yogiyo = Factory.MyPopup3()
                        shop_layout.sitename_yogiyo = site.get('username')
                        shop_layout.sitepassword_yogiyo = site.get('password')

                        shop_layout.pop3_layout = pop3_layout
                        shop_layout.yogiyo.ids.float3.add_widget(shop_layout.pop3_layout)
                self.ids.inform.add_widget(shop_layout)
