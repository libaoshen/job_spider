# coding:utf-8

import sys
import scrapy
from scrapy.http.request import Request
from JobSpider.utils.common import get_first_element
from JobSpider.utils.redis import insert_into_job_spider
from scrapy_redis.spiders import RedisSpider

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


class ZhilianSpider(RedisSpider):
    name = "zhilian"  # 爬虫名称
    allowed_domains = ["xiaoyuan.zhaopin.com"]  # 允许的域名
    start_urls = ["https://xiaoyuan.zhaopin.com/full/0/0_0_0_0_0_-1_" + job_type + "_1_0" for job_type in job_type_list]
    redis_key = 'job_spider_start_urls_zl'

    def parse(self, response):
        print(self.start_urls)
        # 获取下一页的url
        next_url = get_first_element(response.xpath(".//span[@class='font12 pageNext']/parent::*/@href").extract())
        # 获取详情页的url
        details_urls = response.xpath("//div[@class='searchResultJobinfo fr']/p[1]/a/@href").extract()

        # 下一页插入到redis的start_url list中
        if next_url:
            if details_urls:
                insert_into_job_spider("https://" + self.allowed_domains[0] + next_url, 1)
        # 详情页插入到redis的request list中
        for url in details_urls:
            insert_into_job_spider(url if url.startswith('http') else "https:" + url, 2)
