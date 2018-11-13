# DoubanAssessScrapy 豆瓣评论爬虫抓取历程
> 初学者请多多指教。使用python抓取豆瓣霸王别姬影评，并对抓回的网页进行内容提取


	这段时间学习了一下python，刚好上的一门课要用到爬虫，所以就安装了一个scrapy。安装scrapy也很心酸，不过后来很简单的就解决了，就不说了。我跟着网上的教程，还有老师给的一些案例，决定爬一下豆瓣电影里面 《霸王别姬》 的影评，分为一下几步：

- 找到爬取的起始页面，我选择了这个https://movie.douban.com/subject/1291546/reviews?start=0
- 分析网页结构，使用xpath找个每个影评的链接位置
- 将网页内容爬取到本地
- 对保存到本地的文件进行内容提取，提取出标题，作者名，以及影评内容，保存为txt格式，并格式化命名。

---

- 在爬取过程中遇到了一些问题。在爬豆瓣影评怕了七百多条的时候就访问不了豆瓣，搜索后发现原来时访问频率太快导致ip被封了,所以爬数据时要注意控制速度，或是使用代理ip。
- 在提取内容的过程中也遇到了很多问题，都通过百度和google解决了。
  - 第一个就是beautifulsoup的问题，一直用不了select函数，google后发现原来是beautifulsoup版本导致的，
  解决方法：将它的import语句写成
    try:
    from bs4 import BeautifulSoup
    except ImportError:
    from BeautifulSoup import BeautifulSoup
  - 第二个问题就是文件的路径问题。我想用每个网页中的title标签中的内容作为文件名，但是确总是出现错误。发现了两个原因：
    1. 路径中包含换行或者空格等非法字符。
    2. 路径太长
    通过格式化字符串后，问题得以解决。


