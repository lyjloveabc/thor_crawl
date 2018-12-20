    """
    算算你再杭州的租房成本
    """
    
    from thor_crawl.utils.db.daoUtil import DaoUtils
    from thor_crawl.utils.db.mysql.mySQLConfig import MySQLConfig
    
    
    class RentInHz:
        def __init__(self, *args, **kwargs):
            # ============ 工具 ============
            self.dao = DaoUtils(**{'dbType': 'MySQL', 'config': MySQLConfig.localhost()})
    
        def calc(self):
            hz_data = self.dao.get_all('SELECT area_name, area, unit_price FROM sou_fang_renting')
    
            temp = dict()
            for row in hz_data:
                if row['area_name'] in temp:
                    temp[row['area_name']].append(row)
                else:
                    temp[row['area_name']] = list()
                    temp[row['area_name']].append(row)
    
            result = list()
            for x, y in temp.items():
                total = 0
                num = 0
                for row in y:
                    try:
                        # print(float(row['unit_price']))
                        # print(float(str(row['area']).replace('㎡', '')))
                        total += float(row['unit_price']) / float(str(row['area']).replace('㎡', ''))
                        num += 1
                    except ValueError as e:
                        print(e, x, row)
                result.append({'城市': x, '平均数': total / num})
            print(result)
    
        def feature(self):
            hz_data = self.dao.get_all('SELECT feature FROM sou_fang_renting')
    
            feature_list = list()
            for row in hz_data:
                if row['feature'] is not None and row['feature'] != '':
                    for x in str(row['feature']).split(","):
                        feature_list.append(x)
    
            temp = dict()
            for row in feature_list:
                if row in temp:
                    temp[row] = temp[row] + 1
                else:
                    temp[row] = 1
            print(temp)
    
    
    if __name__ == '__main__':
        tj = RentInHz()
        tj.feature()
