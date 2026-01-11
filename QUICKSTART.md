# 🚀 Quick Start Guide

## 快速开始指南

### 1. 安装依赖（第一次运行）

```bash
# 激活虚拟环境（如果有的话）
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 安装所有依赖
pip install -r requirements.txt
```

### 2. 配置 API 密钥

确保 `.env` 文件包含你的 API 密钥：

```bash
FOOTBALL_DATA_API_KEY=your_football_api_key_here
SCOREBAT_API_KEY=your_scorebat_api_key_here
```

**获取 API 密钥：**
- Football Data API: https://www.football-data.org/client/register
- ScoreBat API: https://www.scorebat.com/video-api/

### 3. 运行应用

```bash
streamlit run app.py
```

应用将自动在浏览器打开：`http://localhost:8501`

---

## 📱 功能概览

### 主页面 (/)
- 查看平台介绍
- 导航到统计数据或视频页面

### 统计数据页面 (/search)
- ☁️ 生成联赛词云
- 🌍 查看各国竞赛分布（交互式图表）
- 🌏 按大洲浏览联赛
- 🏳️ 按国家浏览联赛
- 👥 查看球队详细信息
- 🎯 查看射手榜（带交互式图表）
- 📈 查看积分榜（带交互式图表）
- 📁 导出数据为 CSV/Excel

### 视频页面 (/watch)
- 🎥 观看最新比赛集锦
- 🎬 查看比赛视频和亮点
- 📅 按日期浏览比赛

---

## 🎨 新功能亮点

### v2.0 现代化更新
✅ **交互式图表**：使用 Plotly 替代静态图表
✅ **加载动画**：所有数据加载都有进度提示
✅ **现代化 UI**：渐变色、阴影、卡片式设计
✅ **友好提示**：Emoji + 清晰的错误/成功消息
✅ **安全升级**：HTTPS + API v4
✅ **更好的导出**：成功提示 + 文件路径显示

---

## 🛠️ 常见问题

### Q: 安装依赖时出错
```bash
# 尝试升级 pip
pip install --upgrade pip
pip install -r requirements.txt
```

### Q: API 请求失败
1. 检查 `.env` 文件是否存在
2. 确认 API 密钥是否有效
3. 检查网络连接

### Q: 页面加载慢
- 首次加载会缓存数据（1小时）
- 后续访问会更快
- 确保网络连接稳定

### Q: 图表不显示
```bash
# 确保安装了 Plotly
pip install plotly>=5.18.0
```

---

## 📊 数据来源

- **Football Data API**: 竞赛、球队、射手、积分榜数据
- **ScoreBat API**: 比赛视频和集锦

---

## 💡 使用技巧

1. **多选国家对比**：在统计页面可以选择多个国家进行对比
2. **导出数据**：查看射手榜或积分榜后可以导出为 CSV 或 Excel
3. **交互式图表**：鼠标悬停查看详细数据，可以缩放和平移
4. **快速导航**：使用侧边栏按钮快速切换页面

---

## 🚀 部署到云端

### Streamlit Cloud（推荐）
1. 将代码推送到 GitHub
2. 访问 https://streamlit.io/cloud
3. 连接你的仓库
4. 在 Streamlit Cloud 设置中添加 API 密钥（Secrets）
5. 部署！

### 其他平台
- Heroku
- Railway
- Render
- AWS/GCP/Azure

---

## 📝 开发者说明

### 项目结构
```
Streamlit-Soccer-Plantform/
├── app.py                 # 主入口
├── pages/
│   ├── search.py         # 统计数据页面
│   └── watch.py          # 视频页面
├── models/
│   ├── data.py          # Football Data API
│   ├── video.py         # ScoreBat Video API
│   └── produce.py       # 数据导出工具
├── requirements.txt      # 依赖包
├── .env                 # API 密钥（需要创建）
└── README.md            # 项目说明
```

### 修改代码
- 主页样式：编辑 `app.py` 中的 CSS
- 图表配置：修改 `pages/search.py` 中的 Plotly 参数
- API 设置：调整 `models/` 中的重试、延迟等参数

---

## 🎯 下一步

1. ✅ 运行应用并探索功能
2. ⭐ 如果喜欢请给仓库加星
3. 🐛 发现 bug？提交 Issue
4. 💡 有建议？提交 Pull Request

---

**祝你使用愉快！⚽**
