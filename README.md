# Weather CLI

一个基于 MCP (Model Control Protocol) 的天气查询工具，支持命令行和服务器模式，使用 wttr.in API 获取全球天气信息。

## 功能特点

- 获取全球任何位置的实时天气信息
- 默认查询北京天气
- 支持中文天气描述
- 显示详细天气信息（温度、湿度、风速等）
- 无需 API 密钥
- 支持命令行和 MCP 服务器两种使用模式

## 什么是 MCP？

MCP (Model Control Protocol) 是一个轻量级的服务协议，用于构建和部署机器学习模型服务。在本项目中，我们使用 MCP：

- 提供标准化的服务接口
- 支持异步操作
- 便于集成到其他系统
- 支持多种传输协议（stdio、TCP、WebSocket 等）

## 安装

```bash
# 克隆仓库
git clone https://github.com/liye71023326/weather-cli.git
cd weather-cli

# 使用 uv 安装（推荐）
uv pip install -e .

# 或使用 pip 安装
pip install -e .
```

## 使用方法

### 1. 命令行模式

直接使用 `weather-cli` 命令：

```bash
# 查询北京天气（默认）
weather-cli forecast

# 查询上海天气
weather-cli forecast --latitude 31.2304 --longitude 121.4737

# 查询广州天气
weather-cli forecast --latitude 23.1291 --longitude 113.2644
```

### 2. MCP 服务器模式

#### 启动服务器

```bash
# 方式 1：使用 Python 直接运行
python run_server.py

# 方式 2：使用 MCP CLI 工具运行
mcp run weather
```

#### 使用 MCP 客户端查询天气

在另一个终端中：

```bash
# 查询北京天气（默认经纬度）
mcp call weather get_forecast

# 查询指定位置天气
mcp call weather get_forecast --latitude 31.2304 --longitude 121.4737
```

#### 服务器 API 说明

1. `get_forecast` 接口
   - 功能：获取指定位置的天气预报
   - 参数：
     - latitude: 纬度，范围 -90 到 90（默认：39.9042，北京）
     - longitude: 经度，范围 -180 到 180（默认：116.4074，北京）
   - 返回：天气信息字符串，包含：
     - 城市名称
     - 当前天气状况
     - 温度和体感温度
     - 湿度和气压
     - 风向和风速
     - 能见度和云量
     - 降水量

2. `get_alerts` 接口
   - 功能：获取天气预警信息（暂未实现）
   - 参数：
     - state: 地区代码
   - 返回：提示信息

## 常用城市经纬度

- 北京：39.9042, 116.4074（默认）
- 上海：31.2304, 121.4737
- 广州：23.1291, 113.2644
- 深圳：22.5431, 114.0579
- 成都：30.5728, 104.0668
- 武汉：30.5928, 114.3055
- 西安：34.3416, 108.9398
- 杭州：30.2741, 120.1551

## 开发

### 系统要求

- Python 3.13 或更高版本
- httpx：用于异步 HTTP 请求
- mcp[cli]：MCP 协议实现

### 项目结构

```
weather-cli/
├── weather/
│   ├── __init__.py  # MCP 服务器实现和天气 API 集成
│   └── cli.py       # 命令行界面实现
├── run_server.py    # MCP 服务器启动脚本
├── pyproject.toml   # 项目配置
├── .gitignore      # Git 忽略配置
└── README.md       # 本文件
```

### 扩展开发

如果你想扩展这个项目，可以：

1. 添加新的天气数据源
2. 实现更多天气相关功能（如未来天气预报）
3. 添加其他传输协议支持
4. 实现数据缓存机制
5. 实现天气预警功能
6. 添加更多城市的默认经纬度

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 许可证

MIT License

## 致谢

- [wttr.in](https://wttr.in) - 提供天气数据
- [httpx](https://www.python-httpx.org/) - 异步 HTTP 客户端
- [mcp](https://github.com/lablup/mcp) - Model Control Protocol 实现
- [FastMCP](https://github.com/lablup/fastmcp) - MCP 的快速实现框架
