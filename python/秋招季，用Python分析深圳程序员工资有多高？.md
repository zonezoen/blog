# 概述
- 前言
- 统计结果
- 爬虫技术分析
- 爬虫代码实现
- 爬虫分析实现
- 后记
- 预告
## 前言
**多图预警、多图预警、多图预警。**秋招季，毕业也多，跳槽也多。我们的职业发展还是要顺应市场需求，那么各门编程语言在深圳的需求怎么呢？工资待遇怎么样呢？zone 在上次写了这篇文章之后【[用Python告诉你深圳房租有多高]([https://mp.weixin.qq.com/s/qnTzMpQPfWrfyNB41Bugnw](https://mp.weixin.qq.com/s/qnTzMpQPfWrfyNB41Bugnw)
)】，想继续用 Python 分析一下，当前深圳的求职市场怎么样？于是便爬取了某钩招聘数据。以下是本次爬虫的样本数据：
![样本](https://upload-images.jianshu.io/upload_images/2470773-8208be5b0e187648.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

本次统计数据量为 4658 ，其中某拉钩最多能显示 30 页数据，每页 15 条招聘信息，则总为：
> 30 x 15 = 450 

首页爬取跳过一页，则为 435 条，故数据基本爬完。其余不够数量的语言为该语言在深圳只有这么多条招聘信息。
## 统计结果
**各语言平均工资**
其中
- 精准推荐
- 自然语言
- 机器学习
- Go 语言
- 图像识别

<<<<<<< HEAD
独领风骚啊！！！平均工资都挺高的。区块链炒得挺火的，好像平均薪资并没有那么高。我统计完之后，感觉自己拖后腿了，
ma 的！！！要删库跑路了！
=======
独领风骚啊！！！平均工资都挺高的。区块链炒得挺火的，好像平均薪资并没有那么高。我统计完之后，感觉自己拖后腿了，ma 的！！！要删库跑路了！
>>>>>>> f9717758343bc2a2d35317701fd372ac9c8b6af5

![各语言平均薪资](https://upload-images.jianshu.io/upload_images/2470773-832c64d1d3dba4d4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

平均工资计算方式：
![某钩 item](https://upload-images.jianshu.io/upload_images/2470773-448c8f87453ee00e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
最高值与最低值，求平均数，如图薪资则为：
> (10k + 20k)/2 = **15k** 

最后，再总体求平均数。
**公司福利词云**
看福利还是挺丰富的，带薪休假、下午茶、零食、节假日。
![福利词云](https://upload-images.jianshu.io/upload_images/2470773-b9c4221463bda26e.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**公司发展级别排行**
总体由 A 轮向 D 轮缩减，大部分公司不需要融资，嗯，估计是拿不到资本融资，但是自家人又有钱的。
![公司发展级别](https://upload-images.jianshu.io/upload_images/2470773-a4b212c67250a468.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**各语言工作年限要求与学历要求**
看看你的本命语言的市场需求怎么样？你达标了吗？其中三至五年的攻城狮职位挺多的，不怕找不到工作。还有一个趋势是，薪资越高，学历要求越高高。看来学历还是挺重要的。
#### Java
<<<<<<< HEAD
Java 作为一门老牌编程语言，有些要求还是挺高的。为数不多的，有要求 5 - 10 年的。从总体来看，基本与学历没有太大的关联，只要技术到家就行。
=======
>>>>>>> f9717758343bc2a2d35317701fd372ac9c8b6af5
![Java 工作年限要求](https://upload-images.jianshu.io/upload_images/2470773-ab67d7f47cd02f4f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![Java 学历要求](https://upload-images.jianshu.io/upload_images/2470773-6b9675627ee208af.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### Python
<<<<<<< HEAD
Python 作为近年来被追捧的语言，主要是其发展方向众多，AI 、web 后端、运维、爬虫等。其入门要求也不是特别高，基本上本科学历就能胜任多数工作，AI 就要另当别论了。
=======
>>>>>>> f9717758343bc2a2d35317701fd372ac9c8b6af5
![Python 工作年限要求](https://upload-images.jianshu.io/upload_images/2470773-14c5d4b68fb04657.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![Python 学历要求](https://upload-images.jianshu.io/upload_images/2470773-30f7bbaaf255b98a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### C 语言
<<<<<<< HEAD
C 语言，也作为一门老牌编程语言。嗯，怎么感觉新一届的程序员越来越少学 C 语言了呢？
=======
>>>>>>> f9717758343bc2a2d35317701fd372ac9c8b6af5
![C 语言工作年限要求](https://upload-images.jianshu.io/upload_images/2470773-62dcedb8a736bc6c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![C 语言学历要求](https://upload-images.jianshu.io/upload_images/2470773-ff6441c89e8ab2bc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#### 机器学习
<<<<<<< HEAD
是的，这一次感受到了学历的重要性了，硕士要求占了一大半呢！！我这个渣渣二本是入不了这行了。但工作年限要求没有非常高。
=======
>>>>>>> f9717758343bc2a2d35317701fd372ac9c8b6af5
![机器学习工作年限要求](https://upload-images.jianshu.io/upload_images/2470773-15bad75430bc51f1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![机器学习学历要求](https://upload-images.jianshu.io/upload_images/2470773-e780590411aec2a7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 图像识别
<<<<<<< HEAD
图像识别薪资也高，学历要求也相对高一点。
=======
>>>>>>> f9717758343bc2a2d35317701fd372ac9c8b6af5
![图像识别工作年限要求](https://upload-images.jianshu.io/upload_images/2470773-7beba289bbfbd4b0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![图像识别学历要求](https://upload-images.jianshu.io/upload_images/2470773-dfb27a1c5eb51ff4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 自然语言
<<<<<<< HEAD
果然，稀缺人才薪资都高，但这次它还是伴有学历门槛的，所以说要时刻都抱着学习的心态呀。
=======
>>>>>>> f9717758343bc2a2d35317701fd372ac9c8b6af5
![自然语言工作年限要求](https://upload-images.jianshu.io/upload_images/2470773-39f07d1a58d0b25a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![自然语言学历要求](https://upload-images.jianshu.io/upload_images/2470773-67eb0025e475c6b6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#### 区块链
<<<<<<< HEAD
区块链概念刚火爆的时候，感觉大街小巷都在讨论区块链啊？公众号随处都能看到区块链的字眼，随着一些区块链的暴雷，这概念好像有稍微平静下来的感觉。不过从薪资来看，好像也没有非常高。但是为学历还是有点要求的。
=======
>>>>>>> f9717758343bc2a2d35317701fd372ac9c8b6af5
![区块链工作年限要求](https://upload-images.jianshu.io/upload_images/2470773-34414623efddd56c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![区块链学历要求](https://upload-images.jianshu.io/upload_images/2470773-3af651fdb2c04b58.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#### Go 语言
<<<<<<< HEAD
Go 语言的需求量还是挺大的，为学历号位有那么点要求。
=======
>>>>>>> f9717758343bc2a2d35317701fd372ac9c8b6af5
![Go 语言工作年限要求](https://upload-images.jianshu.io/upload_images/2470773-41ac1af479e4e997.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![Go](https://upload-images.jianshu.io/upload_images/2470773-9493457fd5a5d605.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### PHP
<<<<<<< HEAD
PHP 是世界上最好的编程语言，不解释！！！
=======
>>>>>>> f9717758343bc2a2d35317701fd372ac9c8b6af5
![PHP 工作年限要求](https://upload-images.jianshu.io/upload_images/2470773-19bb06e2aade370b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![PHP 学历要求](https://upload-images.jianshu.io/upload_images/2470773-4d2413df2f8b7463.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#### Android
<<<<<<< HEAD
这两年 Android 趋于饱和，在加上小程序与 H5 的冲击，稍微平稳下来了。不过在视频、音频处理方面厉害的话，还是很吃香的。对学历基本没什么要求。
=======
>>>>>>> f9717758343bc2a2d35317701fd372ac9c8b6af5
![Android 工作年限要求](https://upload-images.jianshu.io/upload_images/2470773-2e7d3ca135374c30.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![Android 学历要求](https://upload-images.jianshu.io/upload_images/2470773-dfe1108400863851.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#### iOS
<<<<<<< HEAD
同 Android 类似，不过比 Android 先饱和了。学历方面，基本没什么要求。
=======
>>>>>>> f9717758343bc2a2d35317701fd372ac9c8b6af5
![iOS 工作年限要求](https://upload-images.jianshu.io/upload_images/2470773-f2637e15eeb9e6de.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![iOS 学历要求](https://upload-images.jianshu.io/upload_images/2470773-dd818e36ee5937cc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#### web 前端
<<<<<<< HEAD
web 前端平均工资，比我预期的少了。看来会数据分析还是有好处的，其职位基本本科就能胜任。
=======
>>>>>>> f9717758343bc2a2d35317701fd372ac9c8b6af5
![web 前端工作年限要求](https://upload-images.jianshu.io/upload_images/2470773-7b0bab44b5477c3f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![web 前端学历要求](https://upload-images.jianshu.io/upload_images/2470773-e90b7d762143bc58.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#### 精准推荐
<<<<<<< HEAD
精准推荐薪资贼高啊，可能是和推荐商品有关，商品推荐出去了，买到钱了，你说薪资能不高吗？但是，这行业对学历还是有一定要求的。
=======
>>>>>>> f9717758343bc2a2d35317701fd372ac9c8b6af5
![精准推荐工作年限要求](https://upload-images.jianshu.io/upload_images/2470773-7b1ea9385c4841c6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![精准推荐学历要求](https://upload-images.jianshu.io/upload_images/2470773-3a65ba2eb18fb413.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


<<<<<<< HEAD
=======
#### Node.js
![Node.js 工作年限要求](https://upload-images.jianshu.io/upload_images/2470773-c1738219ecbfbf52.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![Node.js 学历要求](https://upload-images.jianshu.io/upload_images/2470773-ee72ffaddc04fcc3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#### Hadoop
![Hadoop 工作年限要求](https://upload-images.jianshu.io/upload_images/2470773-352f68e18fe60180.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![Hadoop 学历要求](https://upload-images.jianshu.io/upload_images/2470773-5a62b8260236a035.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>>>>>>> f9717758343bc2a2d35317701fd372ac9c8b6af5

## 爬虫技术分析
- 请求库：selenium
- HTML 解析：BeautifulSoup、xpath
- 词云：wordcloud
- 数据可视化：pyecharts
- 数据库：MongoDB
- 数据库连接：pymongo

## 爬虫代码实现
看完统计结果之后，有没有跃跃欲试？想要自己也实现以下代码？以下为代码实现。
对网页右击，点击检查，找到一条 item 的数据：
![网页源码](https://upload-images.jianshu.io/upload_images/2470773-d0d29bf7730923ae.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
数据库存储结构：
```
/* 1 */
{
    "_id" : ObjectId("5b8b89328ffaed60a308bacd"),
    "education" : "本科",# 学习要求
    "companySize" : "2000人以上",# 公司人数规模
    "name" : "python开发工程师",# 职位名称
    "welfare" : "“朝九晚五,公司平台大,发展机遇多,六险一金”",# 公司福利
    "salaryMid" : 12.5,# 工资上限与工资下限的平均数
    "companyType" : "移动互联网",# 公司类型
    "salaryMin" : "10",# 工资下限
    "salaryMax" : "15",# 工资上限
    "experience" : "经验3-5年",# 工作年限
    "companyLevel" : "不需要融资",# 公司级别
    "company" : "XXX技术有限公司"# 公司名称
}
```
由于篇幅原因，以下只展示主要代码：

```
# 获取网页源码数据
# language => 编程语言
# city => 城市
# collectionType => 值：True/False  True => 数据库表以编程语言命名   False => 以城市命名
def main(self, language, city, collectionType):
    print(" 当前爬取的语言为 => " + language + "  当前爬取的城市为 => " + city)
    url = self.getUrl(language, city)
    browser = webdriver.Chrome()
    browser.get(url)
    browser.implicitly_wait(10)
    for i in range(30):
        selector = etree.HTML(browser.page_source)  # 获取源码
        soup = BeautifulSoup(browser.page_source, "html.parser")
        span = soup.find("div", attrs={"class": "pager_container"}).find("span", attrs={"action": "next"})
        print(
            span)  # <span action="next" class="pager_next pager_next_disabled" hidefocus="hidefocus">下一页<strong class="pager_lgthen pager_lgthen_dis"></strong></span>
        classArr = span['class']
        print(classArr)  # 输出内容为 -> ['pager_next', 'pager_next_disabled']
        attr = list(classArr)[0]
        attr2 = list(classArr)[1]
        if attr2 == "pager_next_disabled":#分析发现 class 属性为  ['pager_next', 'pager_next_disabled'] 时，【下一页】按钮不可点击
            print("已经爬到最后一页，爬虫结束")
            break
        else:
            print("还有下一页，爬虫继续")
            browser.find_element_by_xpath('//*[@id="order"]/li/div[4]/div[2]').click()  # 点击下一页
        time.sleep(5)
        print('第{}页抓取完毕'.format(i + 1))
        self.getItemData(selector, language, city, collectionType)# 解析 item 数据，并存进数据库
    browser.close()
```

## 爬虫分析实现
```
# 获取各语言样本数量
def getLanguageNum(self):
    analycisList = []
    for index, language in enumerate(self.getLanguage()):
        collection = self.zfdb["z_" + language]
        totalNum = collection.aggregate([{'$group': {'_id': '', 'total_num': {'$sum': 1}}}])
        totalNum2 = list(totalNum)[0]["total_num"]
        analycisList.append(totalNum2)
    return (self.getLanguage(), analycisList)

# 获取各语言的平均工资
def getLanguageAvgSalary(self):
    analycisList = []
    for index, language in enumerate(self.getLanguage()):
        collection = self.zfdb["z_" + language]
        totalSalary = collection.aggregate([{'$group': {'_id': '', 'total_salary': {'$sum': '$salaryMid'}}}])
        totalNum = collection.aggregate([{'$group': {'_id': '', 'total_num': {'$sum': 1}}}])
        totalNum2 = list(totalNum)[0]["total_num"]
        totalSalary2 = list(totalSalary)[0]["total_salary"]
        analycisList.append(round(totalSalary2 / totalNum2, 2))
    return (self.getLanguage(), analycisList)

# 获取一门语言的学历要求（用于 pyecharts 的词云）
def getEducation(self, language):
    results = self.zfdb["z_" + language].aggregate([{'$group': {'_id': '$education', 'weight': {'$sum': 1}}}])
    educationList = []
    weightList = []
    for result in results:
        educationList.append(result["_id"])
        weightList.append(result["weight"])
    # print(list(result))
    return (educationList, weightList)

# 获取一门语言的工作年限要求（用于 pyecharts 的词云）
def getExperience(self, language):
    results = self.zfdb["z_" + language].aggregate([{'$group': {'_id': '$experience', 'weight': {'$sum': 1}}}])
    totalAvgPriceDirList = []
    for result in results:
        totalAvgPriceDirList.append(
            {"value": result["weight"], "name": result["_id"] + "  " + str(result["weight"])})
    return totalAvgPriceDirList

# 获取 welfare 数据，用于构建福利词云
def getWelfare(self):
    content = ''
    queryArgs = {}
    projectionFields = {'_id': False, 'welfare': True}  # 用字典指定
    for language in self.getLanguage():

        collection = self.zfdb["z_" + language]
        searchRes = collection.find(queryArgs, projection=projectionFields).limit(1000)
        for result in searchRes:
            print(result["welfare"])
            content += result["welfare"]
    return content

# 获取公司级别排行（用于条形图）
def getAllCompanyLevel(self):
    levelList = []
    weightList = []
    newWeightList = []
    attrList = ["A轮", "B轮", "C轮", "D轮及以上", "不需要融资", "上市公司"]
    for language in self.getLanguage():
        collection = self.zfdb["z_" + language]
        # searchRes = collection.find(queryArgs, projection=projectionFields).limit(1000)
        results = collection.aggregate([{'$group': {'_id': '$companyLevel', 'weight': {'$sum': 1}}}])
        for result in results:
            levelList.append(result["_id"])
            weightList.append(result["weight"])
    for index, attr in enumerate(attrList):
        newWeight = 0
        for index2, level in enumerate(levelList):
            if attr == level:
                newWeight += weightList[index2]
        newWeightList.append(newWeight)
    return (attrList, newWeightList)
```
## 后记
总体就分析到这里了，如果你也想看看你所在的城市的薪资标准与市场需求，欢迎后台骚扰。如果人数多，我就专门写下你所在的城市的分析。
## 预告
最近写了挺多关于 Python 的文章，但是这是一个后端公众号啊，所以接下来准备写写后端相关的。最近**微服务**概念炒得挺火的，但网络好像都没找到什么实实在在的项目来学习，刚好我前段时间用 Python 与 Node.js 写了下微服务，所以下面会写微服务相关的文章。敬请期待！


**本篇文章首发于公众号「zone7」，关注公众号获取最新推文，后台回复【深圳求职】获取源码。**



