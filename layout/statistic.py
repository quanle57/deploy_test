from cProfile import label
import os

from matplotlib import font_manager
import matplotlib as mpl
from layout.inform import InformLayout
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.screen import Screen
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.storage.jsonstore import JsonStore
from layout.Connection import ConnectionDB
import matplotlib.pyplot as plt
from kivy.app import App
import datetime
from datetime import timedelta

# depend on pandas and plotly
# import plotly.express as px

os.environ['KIVY_IMAGE'] = 'sdl2, gif'


class StatisticsLayout(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.ID = ""
        self.len_shop = 0
        self.today = datetime.date.today()
        # self.today = datetime.datetime.strptime('2022-07-21', "%Y-%m-%d").date()
        self.app = App.get_running_app()
        self.store = JsonStore('storage.json')
        self.db = ConnectionDB()
        # self.db.openConnect()
        self.inform_layout = InformLayout()
        
        self.dataa = [{"count":0, "total":0, "amount":0, "site_id":1},  # Baemin
                      {"count":0, "total":0, "amount":0, "site_id":2},  # Coupang Eats
                      {"count":0, "total":0, "amount":0, "site_id":3}]  # Yogi Yo
        
        self.datab = [{"total": 0, "count": 0, "amount": 0},            # Previous month
                      {"total": 0, "count": 0, "amount": 0}]            # This month
        
        self.shopId = None
        
        ################## T A B L E ######################
        self.table = MDDataTable(
            size_hint=(1, 1),
            use_pagination=False,
            pos_hint={'center_x': 0.2, 'center_y': 0.4},

            # column_data=[
            #     (' ', dp(20)),
            #     ('Number of orders', dp(20)),
            #     ('Sales', dp(20)),
            #     ('Settlement amount', dp(20)),
            column_data=[
                (' ', dp(20)),
                ('주문수', dp(20)),
                ('매출', dp(20)),
                ('정산액 ', dp(20)),

            ],
            row_data=[
                ('합계', '', '', ''),
                ('배민', '', '', ''),
                ('쿠팡이츠', '', '', ''),
                ('요기요', '', '', '')

            ])

        self.setdatatable(self.dataa, table = 'Table A')

        self.prev_month = (self.today.replace(day=1) - timedelta(days=1)).month
        self.year = (self.today.replace(day=1) - timedelta(days=1)).year
        self.month = self.today.month

        self.table2 = MDDataTable(
            size_hint=(1, 1),
            use_pagination=False,
            pos_hint={'center_x': 0.2, 'center_y': 0.4},
            column_data=[
                ('구분', dp(20)),
                (str(self.year) + '.' + str(self.prev_month), dp(20)),
                (str(self.year) + '.' + str(self.month) + '(F)', dp(20)),
                ('전월대비%', dp(20))
            ],
            row_data=[
                ('매출', '10,765,700 won', '22,645,742 won', 'up 110,4%'),
                ('주문수', '440 case', '934 case', 'up 112,2%'),
                ('정산액', '3,748,140 won', '6,269,038 won', 'up 67,3%')
            ])
        
        self.setdatatable(self.datab, table = 'Table B')

        self.ids.table1.add_widget(self.table)
        self.ids.table2.add_widget(self.table2)

        ################## C H A R T ######################
        x1 = [4, 8, 12, 16, 20, 24]
        y1 = [200.000, 150.000, 100.000, 150.000, 100.00, 200.0]
        plt.figure(1)
        # plt.plot(x1, y1, color='orange', marker='o', label='won')
        default_x_ticks = range(len(x1))
        plt.plot(default_x_ticks, y1, color='orange', marker='o', label='won')
        plt.xticks(default_x_ticks, x1)
        plt.xlabel('', fontsize=14)
        plt.ylabel('', fontsize=14)
        
        plt.legend(loc = 'upper center')
        plt.grid(True)
        self.ids.chart1.add_widget(FigureCanvasKivyAgg(plt.gcf()))

        ################## T A B L E 2 #####################
        self.table3 = MDDataTable(
            size_hint=(1, 0.7),
            use_pagination=False,
            pos_hint={'center_x': 0.2, 'center_y': 0.4},
            # column_data=[
            #     ('Sum', dp(15)),
            #     (' ', dp(15)),
            #     (' ', dp(15)),
            #     ('4.5/5 points', dp(15))
            # ],
            column_data=[
                ('Sum', dp(15)),
                (' ', dp(15)),
                (' ', dp(15)),
                ('4.5/5 points', dp(15))
            ],
            row_data=[
                ('Baemin', ' ', ' ', '4.8/5 points'),
                ('Coupang Eats', ' ', ' ', '4.8/5 points'),
                ('Yogi Yo', ' ', ' ', '4.8/5 points')
            ])

        self.ids.table3.add_widget(self.table3)

        ################## P I E C H A R T ######################

        # labels = ['Baemin', 'Coupang Eats', "Yogi Yo"]
        labels = ['Seoul', 'Busan', "GangNam"]
        sizes = [40, 35, 25]
        explode = [0.1, 0, 0]
        plt.figure(2)
        plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        plt.grid(True)
        
        self.ids.chart2.add_widget(FigureCanvasKivyAgg(plt.gcf()))

        #########################################################

    def load_inform(self):
        self.app.root.current = 'inform_layout'
        self.manager.get_screen('inform_layout').loaddata()
        self.manager.get_screen('inform_layout').load_shop()

    # ----------------------------- LOAD SPIN ---------------------------- #

    def load_spin(self):
        """
            Change to other Shop
        """

        self.db.openConnect()
        sql = "select * from shop where user_id = '" + str(self.ID) + "'"
        shops = self.db.loadRecords(sql)

        self.name_shop = []
        self.shopIDs = []
        total = 0
        self.dataa = [{"count":0, "total":0, "amount":0, "site_id":1}, 
                      {"count":0, "total":0, "amount":0, "site_id":2}, 
                      {"count":0, "total":0, "amount":0, "site_id":3}]
        
        self.datab = [{"total": 0, "count": 0, "amount": 0},
                      {"total": 0, "count": 0, "amount": 0}]

        if len(shops) > 0:

            for index, shop in enumerate(shops):
                self.name_shop.append(str(shop.get('name')) + "." + ' ' * index)
                self.shopIDs.append(shop.get('id'))

            self.ids.spin_shop.values = self.name_shop

            text = self.ids.spin_shop.text.split('.')[-1]
            self.shopId = str(self.shopIDs[text.count(' ')])

            # list_index = self.ids.spin_shop.values.index(self.name_shop[2])

            result = self.getsum_total(self.today, self.shopId)

            if result.get('total') != None:
                total = result.get('total')

            self.count_order(self.shopId, 1)
            
            # Get data of this month
            self.getDataByMonth(self.shopId, option= 2)
            # Get data of previuos month
            self.getDataByMonth(self.shopId, option= 1)
            
            self.setdatatable(self.datab, table= "Table B")
            self.show_sales()
            self.show_review()
            self.show_orderbycity()
            
            self.ids.total.text = "{:,}".format(int(total)) + ' 원'
        
        else: 
            self.load_inform()

    # ------------------------------------------------------------ GETSUM_TOTAL ------------------------------------------------------------ #

    def getsum_total(self, today, shopId):
        """
            Get Sum of sales in Today
        """
        
        sql = "SELECT SUM(`order`.total) as total " \
              "FROM `order` INNER JOIN `site` ON `order`.site_id = `site`.id " \
              "WHERE `order`.status =1 and DATE_FORMAT(`order`.date, '%Y-%m-%d') = '" + str(
            today) + "' and `site`.shop_id = '" + shopId + "'"

        result = self.db.loadRecord(sql)

        return result

    # ------------------------------------------------------------ COUNT_ORDER ------------------------------------------------------------ #

    def count_order(self, shopId, option=1):
        """
            Calculate Number of Order for each Web Site
        """
        
        sql1 = "SELECT COUNT(*) as counts, " \
               " SUM(`order`.total) as total, SUM(`order`.store_discount) as d, SUM(`order`.card_fee) as c, " \
               " SUM(`order`.vat) as v, SUM(`order`.payment) as p, SUM(`order`.order_fee) as o, SUM(`order`.min_fee) as m, SUM(`order`.ship_fee) as s, " \
               " (SELECT `site`.site_id FROM `site` WHERE `site`.id = `order`.site_id) as site_id " \
               " FROM `order` "

        w = self.today.strftime("%w")


        # --------------------------------------- hôm qua  id: yesterday ---------------------------------------- #

        if (option == 1):
            startTime = str(self.today - timedelta(days=1)) + ' 00:00:00'
            endTime = str(self.today - timedelta(days=1)) + ' 23:59:59'

        # --------------------------------------- tuần này  id: thisweek ---------------------------------------- #

        elif (option == 2):
            startTime = str(self.today - timedelta(days=int(w))) + ' 00:00:00'
            endTime = str(self.today) + ' 23:59:59'
            
            thisweek = self.table.row_data = [['Sum', '0', '0', '0'],
                                              ['Baemin', '131', '564545', '4655'],
                                              ['Coupang', '1', '1', '1'],
                                              ['YogiYo', '131', '564545', '4655']]

            self.ids.thisweek = thisweek


        # -------------------------------------- tuần trước   id: lastweek -------------------------------------- #

        elif (option == 3):
            startTime = str(self.today - timedelta(days=int(w) + 7)) + ' 00:00:00'
            endTime = str(self.today - timedelta(days=int(w) + 1)) + ' 23:59:59'
            
            lastweek = self.table.row_data = [['Sum', '1', '1', '0'],
                                              ['Baemin', '2', '4', '5'],
                                              ['Coupang', '1', '1', '1'],
                                              ['YogiYo', '3', '3', '3']]

            self.ids.lastweek = lastweek

        # -------------------------------------- tháng này   id: thismonth -------------------------------------- #

        elif (option == 4):
            first_day_of_month = self.today.replace(day=1)
            startTime = str(first_day_of_month) + ' 00:00:00'

            if (first_day_of_month == 1):
                endTime = str(first_day_of_month) + '00:00:00'
            else:
                endTime = str(self.today - timedelta(days=1)) + ' 23:59:59'
            
            thismonth = self.table.row_data = [['Sum', '4', '4', '4'],
                                               ['Baemin', '4', '4', '45'],
                                               ['Coupang', '4', '4', '4'],
                                               ['YogiYo', '4', '34', '34']]
            self.ids.thismonth = thismonth

        # -------------------------------------- tháng trước id: lastmonth -------------------------------------- #

        elif (option == 5):

            last_day_of_prev_month = self.today.replace(day=1) - timedelta(days=1)
            first_day_of_prev_month = self.today.replace(day=1) - timedelta(days=last_day_of_prev_month.day)

            startTime = str(first_day_of_prev_month) + ' 00:00:00'
            endTime = str(last_day_of_prev_month) + ' 23:59:59'
            
            lastmonth = self.table.row_data = [['Sum', '22', '22', '222'],
                                               ['Baemin', '42222', '422', '4225'],
                                               ['Coupang', '422', '422', '422'],
                                               ['YogiYo', '433', '344', '345']]
            self.ids.lastmonth = lastmonth
        else:
            startTime = str(option) + ' 00:00:00'
            endTime = str(option) + ' 23:59:59'

        sql1 += " WHERE `order`.status = 1 AND `order`.date BETWEEN '" + startTime + "' AND '" + endTime + "' "
        sql1 += " AND `order`.site_id IN (SELECT `site`.id FROM site WHERE `site`.shop_id = '" + shopId + "') "
        sql1 += " GROUP BY site_id ORDER BY site_id ASC "
        results = self.db.loadRecords(sql1)
        
        if results:
            for val in results:
                
                if val['site_id'] == 1:
                    self.dataa[0]["count"] = val['counts']
                    self.dataa[0]["total"] = val['total']
                elif val['site_id'] == 2:
                    self.dataa[1]["count"] = val['counts']
                    self.dataa[1]["total"] = val['total']
                else:
                    self.dataa[2]["count"] = val['counts']
                    self.dataa[2]["total"] = val['total']
            
        sql2 = " SELECT SUM(`settlement`.amount) as amount, (SELECT `site`.site_id FROM site WHERE `site`.id = `settlement`.site_id) AS site_id FROM `settlement` "
        sql2 += " WHERE `settlement`.status = 1 AND `settlement`.date BETWEEN '" + startTime + "' AND '" + endTime + "' "
        sql2 += " AND `settlement`.site_id IN (SELECT `site`.id FROM site where `site`.shop_id = '" + shopId + "') "
        sql2 += " AND `settlement`.settleCodeName!= '민포장주문' AND `settlement`.settleCodeName != '배달의민족' "
        sql2 += " GROUP BY site_id ORDER BY site_id ASC"

        result1 = self.db.loadRecords(sql2)
        
        if result1:
            for val in result1:
                
                if val['site_id'] == 1:
                    self.dataa[0]["amount"] = val['amount']
                elif val['site_id'] == 2:
                    self.dataa[1]["amount"] = val['amount']
                else:
                    self.dataa[2]["amount"] = val['amount']
        
        self.setdatatable(self.dataa, table = 'Table A')

    # ------------------------------------- Y E S T E R D A Y ------------------------------------- #

    def show_yesterday(self):
        if self.shopId != None:
            self.count_order(self.shopId, 1)

    # -------------------------------------- T H I S W E E K -------------------------------------- #

    def show_thisweek(self):
        if self.shopId != None:
            self.count_order(self.shopId, 2)

    # -------------------------------------- L A S T W E E K -------------------------------------- #

    def show_lastweek(self):
        if self.shopId != None:
            self.count_order(self.shopId, 3)

    # ------------------------------------- T H I S M O N T H ------------------------------------- #

    def show_thismonth(self):
        if self.shopId != None:
            self.count_order(self.shopId, 4)

    # ------------------------------------- T H I S M O N T H ------------------------------------- #

    def show_lastmonth(self):
        if self.shopId != None:
            self.count_order(self.shopId, 5)

    # ----------------------------------------- S A L E S ----------------------------------------- #

    def show_sales(self):
        """
            Create Sale Chart
        """
        
        y1 = [0, 0, 0, 0, 0, 0]
        y1[0] = self.totalMoneyByTimeYesterday('00','04')
        y1[1] = self.totalMoneyByTimeYesterday('04','08')
        y1[2] = self.totalMoneyByTimeYesterday('08','12')
        y1[3] = self.totalMoneyByTimeYesterday('12','16')
        y1[4] = self.totalMoneyByTimeYesterday('16','20')
        y1[5] = self.totalMoneyByTimeYesterday('20','24')
        
        # Remove old chart
        self.ids.chart1.clear_widgets()
        x1 = [4, 8, 12, 16, 20, 24]
        
        plt.figure(1).clear()
        plt.figure(1)
        # plt.plot(x1, y1, color='darkblue', marker='o')
        
        default_x_ticks = range(len(x1))
        plt.plot(default_x_ticks, y1, color='orange', marker='o', label='원')
        plt.xticks(default_x_ticks, x1)
        plt.xlabel('', fontsize=14)
        plt.ylabel('', fontsize=14)
        plt.legend(loc = 'upper center')
        plt.grid(True)

        self.sale_chart = self.ids.chart1.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def show_order(self):
        """
            Create Order Chart
        """
        
        y1 = [0, 0, 0, 0, 0, 0]
        # Get number of orders from database
        y1[0] = self.countOrderByTimeYesterday('00','04')
        y1[1] = self.countOrderByTimeYesterday('04','08')
        y1[2] = self.countOrderByTimeYesterday('08','12')
        y1[3] = self.countOrderByTimeYesterday('12','16')
        y1[4] = self.countOrderByTimeYesterday('16','20')
        y1[5] = self.countOrderByTimeYesterday('20','24')
        
        # Remove old chart
        self.ids.chart1.clear_widgets()
        
        x1 = [4, 8, 12, 16, 20, 24]
        
        plt.figure(1).clear()
        plt.figure(1)
        default_x_ticks = range(len(x1))
        plt.plot(default_x_ticks, y1, color='darkblue', marker='o', label='건')
        plt.xticks(default_x_ticks, x1)
        plt.xlabel('', fontsize=14)
        plt.ylabel('', fontsize=14)
        plt.legend(loc = 'upper center')
        plt.grid(True)

        self.ids.chart1.add_widget(FigureCanvasKivyAgg(plt.gcf()))
    
    def show_review(self):
        """
            Show Result of Review
        """
        
        sql = "SELECT (SELECT `site_id` "\
                        " FROM `site` WHERE `site`.id = `review`.site_id) as `site_id`, "\
				        " AVG(`star`) as total "\
				        " FROM `review` "\
				        " WHERE `status` = '1' AND site_id IN (SELECT id FROM site WHERE shop_id = '" + self.shopId + "') "\
				        " GROUP BY `site_id` "\
				        " ORDER BY `datetime` DESC, `site_id` ASC "\
				        " LIMIT 100;"
        result = self.db.loadRecords(sql)
        
        rowdata = [('배민', ' ', ' ', '0 점 / 5 점'),
                ('쿠팡이츠', ' ', ' ', '0 / 5 점'),
                ('요기요', ' ', ' ', '0 점 / 5 점')]
        columndata=[
                ('합계', dp(15)),
                (' ', dp(15)),
                (' ', dp(15)),
                ('0 점/5 점', dp(15))
            ]
        if result:
            baemin_point = 0
            coupang_point = 0
            yogiyo_point = 0
            for value in result:
                if value['site_id'] == 1:
                    rowdata[0] = ['배민', ' ', ' ', '{0:.1f} 점 / 5 점'.format(value['total'])]
                    baemin_point = value['total']
                if value['site_id'] == 2:
                    rowdata[1] = ['쿠팡이츠', ' ', ' ', '{0:.1f} 점 / 5 점'.format(value['total'])]
                    coupang_point = value['total']
                if value['site_id'] == 3:
                    rowdata[2] = ['요기요', ' ', ' ', '{0:.1f} 점 / 5 점'.format(value['total'])]
                    yogiyo_point = value['total']
            
            columndata[-1] = ('{0:.1f} 점 / 5 점'.format((baemin_point + coupang_point + yogiyo_point)/3), dp(15))
        
        # self.table3.column_data = column_data
        # self.table3.row_data = rowdata
        self.table3 = MDDataTable(
            size_hint=(1, 0.7),
            use_pagination=False,
            pos_hint={'center_x': 0.2, 'center_y': 0.4},
            column_data = columndata,
            row_data=rowdata)

        self.ids.table3.clear_widgets()
        self.ids.table3.add_widget(self.table3)
    
    def show_orderbycity(self):
        """
            Show Number of Order by District
        """
        
        self.ids.chart2.clear_widgets()
        # Get Number of Order by City from database
        sql = " SELECT o.*, SUBSTRING_INDEX(o.address,' ',1) AS city , "\
			    " SUBSTRING_INDEX(o.address,' ',2) AS district, "\
			    " count(*) AS total2 "\
                " FROM `order` AS o  "\
			    " WHERE o.status=1  AND `address` IS NOT NULL  AND  "\
                " site_id IN (SELECT id FROM `site` WHERE shop_id = '"+ self.shopId +"') GROUP BY district;"
        result = self.db.loadRecords(sql)
        
        #{'id': 52353, 'user_id': 1, 'order_code': 'F2203091419JTE31', 'site_id': 305, 'total': 19800.0, 'store_discount': 0.0, 
        # 'order_fee': 0.0, 'card_fee': 0.0, 'vat': 0.0, 'payment': 17800.0, 'payment_type': '온라인 결제', 'ship_fee': 2000.0, 
        # 'min_fee': 0.0, 'deliveryTip': 0.0, 'deliveryType': '온라인 결제', 'date': datetime.datetime(2022, 3, 9, 14, 19), 
        # 'note': '서울특별시 관악구 신림동 (신사동) ***-** ****\n0504-****-4523', 'status': 1, 'address': '서울특별시 관악구 신림동
        # (신사동) ***-** ****\n0504-****-4523', 'city': '서울특별시', 'district': '서울특별시 관악구', 'total2': 353}
        
        labels = ['Seoul', 'Busan', "GangNam"]
        sizes = [40, 35, 25]
        explode = [0.1, 0, 0]
        orders = []
        if result:
            labels = []
            sizes = []
            explode = []
            orders = []
            for value in result:
                labels.append(value['district'].split(' ')[-1])
                orders.append(value['total2'])
                explode.append(0)
        
        for thing in orders:
            sizes.append(thing*100/sum(orders))
        
        plt.figure(2).clear()
        plt.figure(2)
        plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        plt.grid(True)
        
        self.ids.chart2.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
    def loading(self):
        from kivy.uix.image import Image
        load_img = Image(source='picture/fbloader.gif')
        self.ids.loading.clear_widgets()
        self.ids.loading.add_widget(load_img)
        self.ids.update_label.text = '[i](최근업데이트 : {})[/i]'.format(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def setdatatable(self, rowdata, table):
        
        # Pass data fo data table
        if table == 'Table A':

            sum_data = ['합계', 
                        "{:,}".format(rowdata[0]['count'] + rowdata[1]['count'] + rowdata[2]['count'])+ ' 건',
                        "{:,}".format(int(rowdata[0]['total'] + rowdata[1]['total'] + rowdata[2]['total']))+ " 원",
                        "{:,}".format(int(rowdata[0]['amount'] + rowdata[1]['amount'] + rowdata[2]['amount']))+ " 원"]

            baemin_data = ['배민', 
                        "{:,}".format(rowdata[0]['count'])+ ' 건',
                        "{:,}".format(int(rowdata[0]['total']))+ " 원", 
                         "{:,}".format(int(rowdata[0]['amount']))+ " 원"]

            coupang_data = ['쿠팡이츠', 
                        "{:,}".format(rowdata[1]['count'])+ ' 건',
                        "{:,}".format(int(rowdata[1]['total']))+ " 원", 
                        "{:,}".format(int(rowdata[1]['amount']))+ " 원"]

            yogiyo_data = ['요기요', 
                        "{:,}".format(rowdata[2]['count'])+ ' 건',
                        "{:,}".format(int(rowdata[2]['total']))+ " 원", 
                        "{:,}".format(int(rowdata[2]['total']))+ " 원"]
            
            self.table.row_data =[sum_data,
                                baemin_data,
                                coupang_data,
                                yogiyo_data]
        
        if table == "Table B":
            
            # Calculate sale percent
            try:
                sale_percent = float((rowdata[1]["total"] - rowdata[0]["total"])*100/rowdata[0]["total"])
            except:
                sale_percent = 100.0
                
            if sale_percent > 0:
                sale_result = "up {0:.2f}%".format(sale_percent)
            elif sale_percent < 0:
                sale_result = "down {0:.2f}%".format(sale_percent)
            else:
                sale_result = "{0:.2f}%".format(sale_percent)
            
            # Calculate Number of Orders percent
            try:
                NoOrders_percent = float((rowdata[1]["count"] - rowdata[0]["count"])*100/rowdata[0]["count"])
            except:
                NoOrders_percent = 100.0
                
            if NoOrders_percent > 0:
                NoOrders_result = "up {0:.2f}%".format(NoOrders_percent)
            elif NoOrders_percent < 0:
                NoOrders_result = "down {0:.2f}%".format(NoOrders_percent)
            else:
                NoOrders_result = "{0:.2f}%".format(NoOrders_percent)
            
            # Calculate Settlement Amount percent
            try:
                settlement_percent = float((rowdata[1]["amount"] - rowdata[0]["amount"])*100/rowdata[0]["amount"])
            except:
                settlement_percent = 100.0
            if settlement_percent > 0:
                settlement_result = "up {0:.2f}%".format(settlement_percent)
            elif settlement_percent < 0:
                settlement_result = "down {0:.2f}%".format(settlement_percent)
            else:
                settlement_result = "{0:.2f}%".format(settlement_percent)
            
            sale_row = ['매출', "{:,}".format(int(rowdata[0]["total"]))+ " 원", "{:,}".format(int(rowdata[1]["total"]))+ " 원", sale_result]
            NoOrders_row = ['주문수', "{:,}".format(rowdata[0]["count"])+ ' 건', "{:,}".format(rowdata[1]["count"])+ ' 건', NoOrders_result]
            settlement_row = ['정산액', "{:,}".format(int(rowdata[0]["amount"]))+ " 원", "{:,}".format(int(rowdata[1]["amount"]))+ " 원", settlement_result]
            
            self.table2.row_data =[sale_row,
                                NoOrders_row,
                                settlement_row]
            
    def getDataByMonth(self, shopid, option = 2):
        
        # Last Month
        if option == 1:
            last_day_of_prev_month = self.today.replace(day=1) - timedelta(days=1)
            first_day_of_prev_month = self.today.replace(day=1) - timedelta(days=last_day_of_prev_month.day)

            startTime = str(first_day_of_prev_month) + ' 00:00:00'
            endTime = str(last_day_of_prev_month) + ' 23:59:59'
        
        # This Month
        else:
            first_day_of_month = self.today.replace(day=1)
            startTime = str(first_day_of_month) + ' 00:00:00'

            if (first_day_of_month == 1):
                endTime = str(first_day_of_month) + '00:00:00'
            else:
                endTime = str(self.today - timedelta(days=1)) + ' 23:59:59'
        
        # Get count and total from database
        sql = "SELECT COUNT(*) as counts, " \
                "SUM(`total`) as total FROM `order`" \
                " WHERE `status` = '1' AND `date` BETWEEN '" + startTime + "' AND '" + endTime + "'" \
                " AND site_id IN (SELECT id FROM site WHERE shop_id = '" + shopid + "')"
        result = self.db.loadRecords(sql)
        
        if result:
            for value in result:
                if option == 1:
                    if value["total"] != None:
                        self.datab[0]["total"] = value["total"]
                    if value["counts"] != None:
                        self.datab[0]["count"] = value["counts"]
                elif option == 2:
                    if value["total"] != None:
                        self.datab[1]["total"] = value["total"]
                    if value["counts"] != None:
                        self.datab[1]["count"] = value["counts"]
        
        # Get Settlement Amount from database
        sql = "SELECT SUM(`amount`) as amount FROM `settlement`" \
                " WHERE `status` = '1' AND `date` BETWEEN '" + startTime + "' AND '" + endTime + "'" \
                " AND site_id IN (SELECT id FROM site WHERE shop_id = '" + shopid + "') " \
                " AND settleCodeName!='민포장주문' AND settleCodeName!='배달의민족'"
        result = self.db.loadRecords(sql)
        
        if result:
            for value in result:
                if option == 1:
                    if value["amount"] != None:
                        self.datab[0]["amount"] = value["amount"]
                elif option == 2:
                    if value["amount"] != None:
                        self.datab[1]["amount"] = value["amount"]
                    
    def totalMoneyByTimeYesterday(self, begin_time, end_time):
        
        yesterday = self.today - timedelta(days=1)
        
        startTime = str(yesterday) + ' {}:00:00'.format(begin_time)
        
        if end_time == '24':
            endTime = str(yesterday) + ' 23:59:59'
        else: 
            endTime = str(yesterday) + ' {}:00:00'.format(end_time)
            
        
        sql = "SELECT SUM(total) as total FROM `order`" \
                " WHERE `status` = '1' AND  `date` BETWEEN '" + startTime + "' AND '" + endTime + "' " \
                " AND site_id IN (SELECT id FROM site WHERE shop_id = '" + self.shopId + "') "
        result = self.db.loadRecords(sql)
        
        if result:
            for value in result:
                if value['total'] != None:
                    return value['total']
                else:
                    return 0          
    
    def countOrderByTimeYesterday(self, begin_time, end_time):
        
        yesterday = self.today - timedelta(days=1)
        
        startTime = str(yesterday) + ' {}:00:00'.format(begin_time)
        
        if end_time == '24':
            endTime = str(yesterday) + ' 23:59:59'
        else: 
            endTime = str(yesterday) + ' {}:00:00'.format(end_time)
            
        
        sql = "SELECT COUNT(*) as counts FROM `order` " \
                " WHERE `date` BETWEEN '" + startTime + "' AND '" + endTime + "' " \
                " AND site_id IN (SELECT id FROM site WHERE shop_id = '" + self.shopId + "')"
        result = self.db.loadRecords(sql)
        
        if result:
            for value in result:
                if value['counts'] != None:
                    return value['counts']
                else:
                    return 0  