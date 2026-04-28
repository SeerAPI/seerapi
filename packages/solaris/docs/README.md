# Solaris 文档中心

欢迎来到 Solaris 项目文档！这里提供开发 Parser 和 Analyzer 所需的所有指南。

## 📚 核心文档

### [Parser 开发指南](PARSER_GUIDE.md)
学习如何将游戏二进制配置文件解析为 JSON 数据。

**适合人群：** 想要添加新 Parser 的开发者

**内容包括：**
- BytesReader API 参考
- 开发步骤详解
- 3 个实战示例
- 常见问题解答

### [Analyzer 开发指南](ANALYZER_GUIDE.md)
学习如何将 JSON 数据转换为标准化的 API 模型。

**适合人群：** 想要添加新 Analyzer 的开发者

**内容包括：**
- 3 种 Analyzer 类型选择
- 数据加载和依赖管理
- 3 个实战示例
- 常见问题解答

### [专有名词表](专有名词.md)
赛尔号游戏术语和项目专有名词解释。

**适合人群：** 所有开发者

**内容包括：**
- 游戏术语（赛尔豆、米币、胶囊等）
- 精灵属性和技能系统
- 战斗效果和状态
- 道具分类说明

## 🚀 快速开始

### 我想添加新的 Parser

1. 阅读 [Parser 开发指南](PARSER_GUIDE.md)
2. 查看 [现有 Parser 代码](../solaris/parse/parsers/)
3. 参考 [专有名词表](专有名词.md) 理解术语
4. 开始编写你的 Parser

### 我想添加新的 Analyzer

1. 阅读 [Analyzer 开发指南](ANALYZER_GUIDE.md)
2. 了解 [seerapi-models](https://github.com/SeerAPI/seerapi-models)
3. 查看 [现有 Analyzer 代码](../solaris/analyze/analyzers/)
4. 开始编写你的 Analyzer

### 我想了解项目

1. 阅读 [项目 README](../README.md)
2. 查看 [专有名词表](专有名词.md)
3. 浏览现有代码示例

## 📖 学习路径

### 路径 1：Parser 开发者

```
1. 阅读 Parser 开发指南
2. 查看 BytesReader API
3. 学习 3 个实战示例
4. 查看现有 Parser 代码
5. 开发你的第一个 Parser
```

### 路径 2：Analyzer 开发者

```
1. 阅读 Analyzer 开发指南
2. 了解 3 种 Analyzer 类型
3. 学习数据加载和依赖管理
4. 查看现有 Analyzer 代码
5. 开发你的第一个 Analyzer
```

### 路径 3：完整流程

```
1. 了解项目概览（README）
2. 学习 Parser 开发
3. 学习 Analyzer 开发
4. 理解数据流转过程
5. 贡献代码
```

## 🔍 快速查找

### 概念和术语
- 什么是 Parser？ → [Parser 开发指南](PARSER_GUIDE.md#什么是-parser)
- 什么是 Analyzer？ → [Analyzer 开发指南](ANALYZER_GUIDE.md#什么是-analyzer)
- 赛尔号术语 → [专有名词表](专有名词.md)

### API 参考
- BytesReader 方法 → [Parser 开发指南 - BytesReader API](PARSER_GUIDE.md#bytesreader-api)
- Analyzer 类型 → [Analyzer 开发指南 - Analyzer 类型](ANALYZER_GUIDE.md#analyzer-类型)
- 数据加载 → [Analyzer 开发指南 - 数据加载](ANALYZER_GUIDE.md#数据加载)

### 示例代码
- Parser 示例 → [Parser 开发指南 - 实战示例](PARSER_GUIDE.md#实战示例)
- Analyzer 示例 → [Analyzer 开发指南 - 实战示例](ANALYZER_GUIDE.md#实战示例)
- 现有代码 → [solaris/parse/parsers/](../solaris/parse/parsers/) 和 [solaris/analyze/analyzers/](../solaris/analyze/analyzers/)

### 问题解决
- Parser 常见问题 → [Parser 开发指南 - 常见问题](PARSER_GUIDE.md#常见问题)
- Analyzer 常见问题 → [Analyzer 开发指南 - 常见问题](ANALYZER_GUIDE.md#常见问题)

## 🤝 获取帮助

遇到问题？

1. 查看对应指南的"常见问题"部分
2. 搜索 [GitHub Issues](https://github.com/SeerAPI/solaris/issues)
3. 查看现有代码示例
4. 创建新的 Issue 提问

## 📝 贡献文档

发现文档问题或有改进建议？

1. 在 [GitHub Issues](https://github.com/SeerAPI/solaris/issues) 中报告
2. 提交 Pull Request 改进文档
3. 在 Discussions 中讨论

## 🔗 相关资源

- [Solaris 项目主页](https://github.com/SeerAPI/solaris)
- [seerapi-models 仓库](https://github.com/SeerAPI/seerapi-models)
- [Python 官方文档](https://docs.python.org/3/)
- [Pydantic 文档](https://docs.pydantic.dev/)

---

**祝你开发愉快！** 🚀
