# coding:utf-8

import sys
import scrapy
from scrapy.http.request import Request
from JobSpider.utils.common import A
reload(sys)
sys.setdefaultencoding("utf-8")

job_type_list_producet_tech = ["产品经理", "产品专员", "产品设计", "新媒体运营", "文案编辑", "内容运营", "交互设计", "UI设计师",

                               "网页设计", "大数据工程师", "系统设计", "数据分析师", "研发工程师", "软件工程师", "测试工程师", "前端工程师",

                               "硬件工程师", "移动开发", "人工智能", "数据库工程师", "运维工程师", "游戏开发", "通信工程师", "项目管理",

                               "售前工程师", "售后工程师", "技术支持"]
job_type_list_eco = ["银行柜员", "通用岗位", "投资经理", "理财顾问", "银行客户经理", "精算师", "信托业务", "证券经纪人",

                     "保险顾问", "理赔专员", "个人业务", "公司业务", "信用卡业务"]

job_type_list_manufa = ["工业工程师", "制造工程师", "生产经理", "电子工程师", "电气工程师", "自动化工程师", "半导体技术", "机械工程师",

                        "机电工程师", "维修工程师", "汽车设计", "汽车制造", "汽车维修、保养", "模具工程师", "化工工程师", "化学分析师",

                        "实验室技术员", "生物制药", "医药技术研发", "服装设计", "纺织工程师"]

job_type_list_archi = ["房地产销售", "房地产项目管理", "合同管理", "建筑工程师", "土建工程师", "结构工程师", "造价工程师", "市政工程师",

                       "给排水工程师", "制冷工程师", "暖通工程师", "建筑设计师", "项目工程师", "景观设计", "室内设计", "装潢设计师",

                       "环保工程师", "地质工程师"]

job_type_list_market = ["销售代表", "电话销售", "网络销售", "大客户销售", "销售业务跟单", "招商专员", "销售管理", "销售支持",

                        "售前支持", "售后支持", "客服专员", "网络客服", "市场专员", "活动策划", "活动执行", "市场推广",

                        "品牌专员", "品牌公关"]

job_type_list_adm = ["行政专员", "前台", "文秘", "人力资源专员", "人事助理", "招聘专员", "绩效考核专员", "薪酬福利专员",

                     "出纳", "会计师", "财务专员", "审计专员", "税务", "法务专员", "合规专员"]

job_type_list_other = ["实习生", "管培生", "储备干部", "公务员", "咨询顾问", "教师", "翻译", "兼职",

                       "其他"]

job_type_list = job_type_list_producet_tech + job_type_list_adm + job_type_list_archi + job_type_list_eco + job_type_list_manufa + job_type_list_market + job_type_list_other

headers = {"Host": "cimg.zhaopin.cn",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0",
           "Referer": "https://xiaoyuan.zhaopin.com/full/0/0_0_0_0_0_-1_%E9%93%B6%E8%A1%8C%E6%9F%9C%E5%91%98_1_0"}


class ZhilianSpiderItem(scrapy.Item):
    job_name = scrapy.Field()  # 职位名
    company_name = scrapy.Field()  # 公司名
    company_domain = scrapy.Field()  # 公司领域
    company_scale = scrapy.Field()  # 公司规模
    company_type = scrapy.Field()  # 公司类型
    job_location = scrapy.Field()  # 工作地点
    job_type = scrapy.Field()  # 职位类别
    job_hc = scrapy.Field()  # 招聘人数
    job_pub_time = scrapy.Field()  # 发布时间
    job_attribute = scrapy.Field()  # 职位性质:全职，实习，兼职
    job_education = scrapy.Field()  # 学历要求
    job_description = scrapy.Field()  # 职位描述


class ZhilianSpider(scrapy.Spider):
    name = "zhilian"  # 爬虫名称
    allowed_domains = ["xiaoyuan.zhaopin.com"]  # 允许的域名
    start_urls = ["https://xiaoyuan.zhaopin.com/full/0/0_0_0_0_0_-1_银行柜员_1_0"]

    # ["https://xiaoyuan.zhaopin.com/full/0/0_0_0_0_0_-1_" + type + "_1_0" for type in job_type_list]

    def parse(self, response):
        # urls = response.xpath(
        #     "//a[@class='searchResultSeemore __ga__fullResultcampuspostmore_clickfullresultcampuspostmore_001']@href")\
        #     .extract()

        urls = response.xpath("//div[@class='searchResultJobinfo fr']/p[1]/a/@href").extract()

        for url in urls:
            yield Request(url="https:" + url, callback=self.parse_job)

    def parse_job(self, response):
        job_name = response.xpath(".//h1[@id='JobName']/text()").extract()[0] if response.xpath(".//h1[@id='JobName']/text()").extract() else None
        company_name = response.xpath(".//li[@id='jobCompany']/a/text()").extract()[0] if response.xpath(".//li[@id='jobCompany']/a/text()").extract() else None
        company_info = response.xpath(".//li[@class='cJobDetailInforWd2']")
        company_domain = company_info[0].xpath("@title").extract()[0] if len(company_info) > 1 else None
        company_scale = company_info[1].xpath("text()").extract()[0] if len(company_info) > 1 else None

        company_type = response.xpath(".//ul[@class='cJobDetailInforTopWrap clearfix c3']/li[last()]/text()").extract()[
            0] if response.xpath(".//ul[@class='cJobDetailInforTopWrap clearfix c3']/li[last()]/text()").extract() else None
        job_info = response.xpath(
            ".//ul[@class='cJobDetailInforBotWrap clearfix c3']/li[@class='cJobDetailInforWd2 marb']")
        job_info_len = len(job_info)
        job_location = job_info[0].xpath("text()").extract()[0] if job_info_len > 0 else None
        job_type = job_info[1].xpath("text()").extract()[0] if job_info_len > 1 else None
        job_hc = job_info[2].xpath("text()").extract()[0] if job_info_len > 2 else None
        job_pub_time = job_info[3].xpath("text()").extract()[0] if job_info_len > 3 else None
        job_attribute = job_info[4].xpath("text()").extract()[0] if job_info_len > 4 else None
        job_education = job_info[5].xpath("text()").extract()[0] if job_info_len > 5 else None

        job_description = response.xpath(".//div[@class='cJob_Detail f14']/p[@class='mt20']/text()").extract()[0] \
            if response.xpath(".//div[@class='cJob_Detail f14']/p[@class='mt20']/text()").extract() else \
            response.xpath(".//div[@class='cJob_Detail f14']/p[2]/span/text()").extract()[0] \
                if response.xpath(".//div[@class='cJob_Detail f14']/p[2]/span/text()").extract() else None

        # print("job_name " + job_name)
        # print("job_company " + job_company)
        # print("job_hangye " + job_hangye)
        # print("job_scale " + job_scale)
        # print("company_type " + company_type)
        # print("job_location " + job_location)
        # print("job_type " + job_type)
        # print("job_numbers " + job_numbers)
        # print("job_pub_time " + job_pub_time)
        # print("job_attribute " + job_attribute)
        # print("job_education " + job_education)
        # print("job_description " + job_description)

        item = ZhilianSpiderItem(job_name=job_name, company_name=company_name, company_domain=company_domain,
                                 company_scale=company_scale, company_type=company_type, job_location=job_location,
                                 job_type=job_type, job_hc=job_hc, job_pub_time=job_pub_time,
                                 job_attribute=job_attribute, job_education=job_education,
                                 job_description=job_description)

        yield item
