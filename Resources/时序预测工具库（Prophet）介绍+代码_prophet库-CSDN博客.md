---
created: 2025-04-10-Thursday-16:17:23
source: https://blog.csdn.net/SeafyLiang/article/details/121780934
---
#### 时序预测工具库（Prophet）

-   -   [一、Prophet 简介](https://blog.csdn.net/SeafyLiang/article/details/121780934#Prophet__6)
    -   [二、Prophet 适用场景](https://blog.csdn.net/SeafyLiang/article/details/121780934#Prophet__12)
    -   [三、Prophet 算法的输入输出](https://blog.csdn.net/SeafyLiang/article/details/121780934#Prophet__21)
    -   [四、Prophet 算法原理](https://blog.csdn.net/SeafyLiang/article/details/121780934#Prophet__43)
    -   [五、与机器学习算法的对比](https://blog.csdn.net/SeafyLiang/article/details/121780934#_58)
    -   [六、代码](https://blog.csdn.net/SeafyLiang/article/details/121780934#_65)
    -   -   [6.1 依赖安装](https://blog.csdn.net/SeafyLiang/article/details/121780934#61__67)
        -   [6.2 预测demo](https://blog.csdn.net/SeafyLiang/article/details/121780934#62_demo_80)
        -   [6.3 效果图](https://blog.csdn.net/SeafyLiang/article/details/121780934#63__110)
    -   [七、参考资料](https://blog.csdn.net/SeafyLiang/article/details/121780934#_113)
    -   [八、官方链接：](https://blog.csdn.net/SeafyLiang/article/details/121780934#_120)
    -   [九、案例链接：](https://blog.csdn.net/SeafyLiang/article/details/121780934#_125)

**参考内容**：  
[时间序列模型Prophet使用详细讲解](https://blog.csdn.net/anshuai_aw1/article/details/83412058)  
[初识Prophet模型（一）-- 理论篇](https://www.jianshu.com/p/218757bee516)

### 一、Prophet 简介

Prophet是**Facebook开源**的时间序列预测算法，可以**有效处理节假日信息**，并**按周、月、年对时间序列数据的变化趋势进行拟合**。根据官网介绍，Prophet对具有强烈周期性特征的历史数据拟合效果很好，不仅可以处理[时间序列](https://so.csdn.net/so/search?q=%E6%97%B6%E9%97%B4%E5%BA%8F%E5%88%97&spm=1001.2101.3001.7020)存在一些异常值的情况，也可以处理部分缺失值的情形。算法提供了**基于Python和R**的两种实现方式。

从论文上的描述来看，这个 prophet 算法是基于时间序列分解和机器学习的拟合来做的，其中在拟合模型的时候使用了 **pyStan** 这个开源工具，因此能够在较快的时间内得到需要预测的结果。

### 二、Prophet 适用场景

Prophet适用于具有明显的内在规律的商业行为数据,例如：有如下特征的业务问题：  
● 有至少几个月（最好是一年）的每小时、每天或每周观察的历史数据；  
● 有多种人类规模级别的较强的季节性趋势：每周的一些天和每年的一些时间；  
● 有事先知道的以不定期的间隔发生的重要节假日（比如国庆节）；  
● 缺失的历史数据或较大的异常数据的数量在合理范围内；  
● 有历史趋势的变化（比如因为产品发布）；  
● 对于数据中蕴含的非线性增长的趋势都有一个自然极限或饱和状态。

### 三、Prophet 算法的输入输出

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6cd1de760221e634aab271a719258069.png)  
上图为一个时间序列场景：  
● 黑色表示原始的时间序列离散点  
● 深蓝色的线表示使用时间序列来拟合所得到的取值  
● 浅蓝色的线表示时间序列的一个置信区间，也就是所谓的合理的上界和下界  
● prophet 所做的事情就是：

-   输入已知的时间序列的时间戳和相应的值；
-   输入需要预测的时间序列的长度；
-   输出未来的时间序列走势。
-   输出结果可以提供必要的统计指标，包括拟合曲线，上界和下界等。  
    传入prophet的数据分为两列 ds 和 y ,ds表示时间序列的时间戳，y表示时间序列的取值

其中：  
● ds是pandas的日期格式，样式类似与YYYY-MM-DD for a date or YYYY-MM-DD HH:MM:SS；  
● y列必须是数值型，代表着我们希望预测的值。

通过 prophet 的计算，可以计算出：  
● yhat，表示时间序列的预测值  
● yhat\_lower，表示预测值的下界  
● yhat\_upper，表示预测值的上界

### 四、Prophet 算法原理

算法模型：  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1d8c7775f867deb18d4e35773f8a63c7.png)

模型整体由三部分组成：  
● growth(增长趋势)  
● seasonality(季节趋势)  
● holidays(节假日对预测值的影响)  
其中:  
● g(t) 表示趋势项，它表示时间序列在非周期上面的变化趋势；  
● s(t) 表示周期项，或者称为季节项，一般来说是以周或者年为单位；  
● h(t) 表示节假日项，表示时间序列中那些潜在的具有非固定周期的节假日对预测值造成的影响；  
● 即误差项或者称为剩余项，表示模型未预测到的波动， 服从高斯分布；  
Prophet 算法就是通过拟合这几项，然后最后把它们累加起来就得到了时间序列的预测值。

### 五、与机器学习算法的对比

与先进的机器学习算法如LGBM相比，Prophet作为一个时间序列的工具。  
**优点**就是不需要特征工程就可以得到趋势，季节因素和节假日因素。  
但是这同时也是它的**缺点**之一，它无法利用更多的信息，如在预测商品的销量时，无法利用商品的信息，门店的信息，促销的信息等。

因此，寻找一种融合的方法是一个迫切的需求。

### 六、代码

#### 6.1 依赖安装

```powershell
# 安装pystan
conda install pystan

# 安装plotly
conda install plotly -y

# 安装prophet
sudo pip install fbprophet

```

#### 6.2 预测demo

测试数据集  
[example\_wp\_log\_peyton\_manning.csv](https://lark-assets-prod-aliyun.oss-cn-hangzhou.aliyuncs.com/yuque/0/2021/csv/2524844/1632895831068-8ec8e160-11cc-44f1-96c6-2075ac3873a3.csv?OSSAccessKeyId=LTAI4GGhPJmQ4HWCmhDAn4F5&Expires=1638891242&Signature=VsndxJ5gQ8yKoV3i5m/yNG9K2sI=&response-content-disposition=attachment;filename*=UTF-8%27%27example_wp_log_peyton_manning.csv)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/2579eb3a70988d92507b40b8808f023e.png)

```python
import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt

# 读入数据集
df = pd.read_csv('data/example_wp_log_peyton_manning.csv')
print(df.head())
# 拟合模型
m = Prophet()
m.fit(df)

# 构建待预测日期数据框，periods = 365 代表除历史数据的日期外再往后推 365 天
future = m.make_future_dataframe(periods=365)
future.tail()
# 预测数据集
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
# 展示预测结果
m.plot(forecast)
# 预测的成分分析绘图，展示预测中的趋势、周效应和年度效应
m.plot_components(forecast)
plt.show()
```

#### 6.3 效果图

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/36391d2e2415305b8f4e9ed814d03329.png)  
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/78cedb84b2395c82f2a90351bf0d0648.png)

### 七、参考资料

● [时间序列模型Prophet使用详细讲解](https://blog.csdn.net/anshuai_aw1/article/details/83412058)  
● [Prophet官网](https://facebook.github.io/prophet/)  
● [github项目](https://github.com/facebook/prophet)  
● [论文：Forecasting at scale](https://link.zhihu.com/?target=https://peerj.com/preprints/3190/)  
● [Facebook 时间序列预测算法 Prophet 的研究](https://zhuanlan.zhihu.com/p/52330017)

### 八、官方链接：

● 论文：《Forecasting at scale》,https://peerj.com/preprints/3190/  
● github：https://github.com/facebook/prophet  
● 官网：https://facebook.github.io/prophet/

### 九、案例链接：

● 预测股价并进行多策略交易：https://mp.weixin.qq.com/s/bf\_CHcoZMjqP6Is4ebD58g  
● 预测Medium每天发表的文章数：https://mp.weixin.qq.com/s/1wujYYDP\_P2uerZzZBaspg  
● 预测网站流量：https://pbpython.com/prophet-overview.html  
● 预测空气质量：https://mp.weixin.qq.com/s/S-NNG7BmviitBmMBJRJSRQ  
● 预测客运量：https://www.analyticsvidhya.com/blog/2018/05/generate-accurate-forecasts-facebook-prophet-python-r/  
● 疫情预测分析：https://mp.weixin.qq.com/s/fZpsy1bQ3Olhng1P5p5WAg  
● 原理讲解：https://mp.weixin.qq.com/s/675ASxDSVH\_8BX6W8WRRqg  
● 知乎专栏：https://zhuanlan.zhihu.com/p/52330017  
● 股票价格预测：https://mp.weixin.qq.com/s/78xpmsbC2N1oZ3UIMm29hg  
● 高致病性传染病的传播趋势预测——时间序列预测算法Prophet：https://aistudio.baidu.com/aistudio/projectdetail/525311?channelType=0&channel=0
