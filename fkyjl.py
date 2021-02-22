import requests
from lxml import etree
import xlwt
import time

data = []

def get_info():
    i=0
    while(i<=50):
        i+=1
        time.sleep( 50 )
        #获取html页面
        url = 'https://search.bilibili.com/all?keyword=%E7%96%AB%E8%8B%97%E7%A7%91%E6%99%AE'+"&page="+str(i)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
        res = requests.get(url,headers=headers)
        res.encoding = 'utf-8'
        html = res.text
        
        #解析页面，提取目标信息
        
        tree = etree.HTML(html)
        lis = tree.xpath(u'/html/body/div[@id="server-search-app"]/div[@class="contain"]/div[@class="body-contain"]/div[@id="all-list"]/div[@class="flow-loader"]/div[@class="mixin-list"]/ul/li')
        print(lis)
        for li in lis:
            info = []
            #提取视频名
            name = li.xpath('./a/@title')[0]
            info.append(name)
            #提取链接
            link = li.xpath('./a/@href')[0]
            info.append(link)
            #提取播放量
            play_num = li.xpath('./div/div[3]/span[1]/text()')[0]
            info.append(play_num)
            #提取弹幕数
            discuss = li.xpath('./div/div[3]/span[2]/text()')[0]
            info.append(discuss)
            #提取时间
            up_time = li.xpath('./div/div[3]/span[3]/text()')[0]
            info.append(up_time)
            #提取up主
            up = li.xpath('./div/div[3]/span[4]/a/text()')[0]
            info.append(up)
            #汇总到data列表中
            data.append(info)

def main():
    get_info()
    #保存数据
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('sheet1')
    #写表头
    col_name = ('视频名','视频链接','播放量','弹幕量','上传时间','up主')
    for i in range(6):
        ws.write(0,i,col_name[i])
    for r in range(len(data)):
        case = data[r]
        for c in range(6):
            ws.write(r+1,c,case[c])
    wb.save('疫情.xls')




if __name__ == "__main__":
    # execute only if run as a script
    main()

