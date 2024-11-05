# ODScan

![License](https://img.shields.io/github/license/zhijing123/ODScan)
![Stars](https://img.shields.io/github/stars/zhijing123/ODScan)
![Issues](https://img.shields.io/github/issues/zhijing123/ODScan)

ODScan是一个对开放目录进行扫描的工具，帮助你在海量文件中，迅速扫描存活文件，下载文件（文件较多时不建议）  
仅支持python3，仅适用于开放目录
![图片](https://github.com/user-attachments/assets/bde42eea-1351-42ad-a4cd-38430973b0df)


## ✨ 核心功能

  -h, --help           show this help message and exit  
  -u URL, --url=URL    指定url，例如http(s)://xxxx/  
  --thread=THREAD_NUM  线程默认为5  
  --alive              进行文件访问，访问后的结果自动保存./export下，以域名或ip为文件名的.txt文件  
  --dump               下载文件至download下  

## 📚 详细功能说明

### 1. -u 仅进行网页目录文件名获取，速度较快，适合进行统计文件数量和文件快速浏览

![图片](https://github.com/user-attachments/assets/5949a8e7-7408-4950-9d65-e96f947d7ea5)

### 2. -u --alive 对文件进行存活扫描，能够进行访问的文件会储存在./export/(域名).txt文件中

![图片](https://github.com/user-attachments/assets/04060a65-3d8a-413b-b22e-3aed8739c7b5)
![图片](https://github.com/user-attachments/assets/232cdcd0-7370-403e-94f9-79204f56b29b)

## 🔍 -u --alive --dump 对文件进行下载，并下载至./download中，文件较大时不建议

![图片](https://github.com/user-attachments/assets/d7932f91-b4e1-4be2-809d-5d45c97562fe)
![图片](https://github.com/user-attachments/assets/40caf8e1-d6be-423f-b77b-1b868daadf77)


## 🤝 参与贡献

我非常欢迎各种形式的贡献：
- 🎨 提交新功能建议
- 🐛 报告 Bug
- 📝 改进文档
- 🔧 提交代码优化

> 如果您有好的想法，请提交 Issue，我会认真考虑并尽力实现！

## 📋 待办事项

- [ ] 功能优化和 Bug 修复
- [ ] 新功能开发
- [ ] 性能优化
- [ ] 文档完善

## ⚠️ 免责声明

本工具仅用于授权的安全测试，请勿用于非法用途。使用本工具造成的任何后果由使用者承担。

## 📄 License

[MIT License](LICENSE)

---
如果觉得这个项目对您有帮助，请给个 Star ⭐️ 支持一下！
