

# Bitcoin: send tx
send a tx on Bitcoin testnet, and parse the tx data down to every bit, better write script yourself.

# 项目完成人
李晨漪20.3班

github：orthokikanium
# 代码说明
requests-html 模块安装使用 pip install requests-html 即可。

对于该库的简单使用，代码如下所示：

from requests_html import HTMLSession

session = HTMLSession()

r = session.get('https://python.org/')

print(dir(r.html))

首先从 requests_html 库导入 HTMLSession 类，然后将其实例化之后，调用其 get 方法，发送请求，得到的 r 输出为 <Response [200]>，后续即可使用内置的解析库对数据进行解析。并通过 dir 函数查阅。

由于该库是解析 html 对象，所以可以查看对应的 html 对象包含哪些方法与与属性。
# 运行指导
安装模块后可直接运行。
# 运行截图
<img width="416" alt="image" src="https://user-images.githubusercontent.com/91087648/181791279-b2f3f62a-2ca3-4752-88f9-ee2e013fbed3.png">

# 参考文献
https://blog.csdn.net
