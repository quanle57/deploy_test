from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivy.app import App
import hashlib
from layout.Connection import ConnectionDB
from kivy.storage.jsonstore import JsonStore

store = JsonStore('storage.json')


class LoginLayout(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.db = ConnectionDB()
        self.db.openConnect()
        self.remember = False

    #####################################################################################################################################
    def checkbox(self,instance,value):
        self.remember = value
 
    #####################################################################################################################################
    def loginAction(self):
        phone = str(self.app.screen_manager.get_screen('login_layout').ids['phone'].text)
        password = str(self.app.screen_manager.get_screen('login_layout').ids['password'].text)
        sql = "SELECT id FROM admin where phone = '"+phone+"' and password='"+hashlib.md5(password.encode()).hexdigest()+"'"
        result = self.db.loadRecord(sql)
        if phone == '' or password == '':
            toast('Account missing information')
        elif result is None: 
            toast('Your password incorrect')
        else:
            phone = str(self.app.screen_manager.get_screen('login_layout').ids['phone'].text)
            password = str(self.app.screen_manager.get_screen('login_layout').ids['password'].text)

            if self.remember:
                store.put('UserInfo', ID=result.get('id'), Phone=phone, Password=password)
            elif not self.remember:
                store.put('UserInfo', ID='', Phone='', Password='')

            # self.manager.current = 'inform_layout'
            self.manager.current = 'statistic_layout'
            self.manager.get_screen('statistic_layout').ID = result.get('id')
            self.manager.get_screen('inform_layout').ID = result.get('id')
            # self.manager.get_screen('inform_layout').load_shop()
            # self.manager.get_screen('inform_layout').loaddata()
            self.manager.get_screen('statistic_layout').load_spin()
            
            toast("Login Successfully")
    
