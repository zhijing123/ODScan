# ODScan
ODScan is a tool for scanning open directories

ODScan是一个对开放目录进行扫描的工具，帮助你在海量文件中，迅速扫描存活文件，获得最大文件，下载文件（文件较多时不建议），程序支持文件内容正则匹配，程序执行完成后会在当前目录生成result.txt

-h 查找帮助
-u 指定需要扫描的路径
--thread 线程数量，默认为5
--reg 需要匹配的内容
--deep 扫描深度，默认无限递归
--dump 下载文件，文件较多时谨慎使用，下载在download/目录下
