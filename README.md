# Weather CLI

一个简单的命令行天气查询工具，使用 wttr.in API 获取全球天气信息。

## 功能特点

- 获取全球任何位置的实时天气信息
- 默认查询北京天气
- 支持中文天气描述
- 显示详细天气信息（温度、湿度、风速等）
- 无需 API 密钥

## 安装

```bash
# 克隆仓库
git clone https://github.com/your-username/weather-cli.git
cd weather-cli

# 使用 uv 安装（推荐）
uv pip install -e .

# 或使用 pip 安装
pip install -e .
```

## 使用方法

### 查询北京天气（默认）

```bash
weather-cli forecast
```

### 查询指定位置天气

```bash
# 查询上海天气
weather-cli forecast --latitude 31.2304 --longitude 121.4737

# 查询广州天气
weather-cli forecast --latitude 23.1291 --longitude 113.2644
```

## 常用城市经纬度

- 北京：39.9042, 116.4074（默认）
- 上海：31.2304, 121.4737
- 广州：23.1291, 113.2644
- 深圳：22.5431, 114.0579

## 开发

### 要求

- Python 3.8 或更高版本
- httpx
- mcp[cli]

### 项目结构

```
weather-cli/
├── weather/
│   ├── __init__.py  # 主要实现
│   └── cli.py       # 命令行界面
├── run_server.py    # 服务器启动脚本
├── pyproject.toml   # 项目配置
├── .gitignore      # Git 忽略配置
└── README.md       # 本文件
```

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 许可证

MIT License

## 致谢

- [wttr.in](https://wttr.in) - 提供天气数据
- [httpx](https://www.python-httpx.org/) - 异步 HTTP 客户端
- [mcp](https://github.com/lablup/mcp) - Model Control Protocol 实现
