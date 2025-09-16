# Markdown Converter

一个高效的文档转Markdown工具，针对Vercel部署进行优化。

## 功能特点

- 🚀 **极简设计** - 拖拽上传，一键转换
- 📄 **核心格式支持** - PDF、Word (.docx)、Excel (.xlsx)、HTML、CSV、TXT
- ⚡ **即时预览** - 转换完成后立即预览Markdown内容
- 💾 **一键下载** - 支持直接下载转换后的.md文件
- 🌙 **暗黑模式** - 自适应明暗主题
- ☁️ **Vercel优化** - 专为云部署优化，符合250MB限制
- 🔄 **智能回退** - 自动处理不支持的格式

## 技术栈

- **前端**: Next.js 15 + TypeScript + Tailwind CSS
- **后端**: Python + Microsoft MarkItDown
- **部署**: Vercel

## 支持的文件格式

**优化版本 (Vercel部署)**:
- 📄 PDF文档 (.pdf) - 使用markitdown库
- 📄 Microsoft Word (.docx) - Office文档支持
- 📊 Microsoft Excel (.xlsx) - 电子表格转换
- 📄 HTML文件 (.html, .htm) - 基本标签转换
- 📄 文本文件 (.txt) - 多编码支持
- 📋 CSV文件 (.csv) - 表格格式转换

**不支持的格式** (为减小函数大小):
- PowerPoint (.pptx) - 超过Vercel限制
- 图片文件 (.jpg, .png) - 需要额外依赖
- 音频文件 - 需要额外依赖

> **优化说明**: 为了符合Vercel 250MB函数大小限制，我们精简了依赖，保留了最重要的PDF、Word、Excel支持。

## 本地开发

### 前置要求

- Node.js 18+
- Python 3.9+

### 安装依赖

```bash
# 安装Node.js依赖
npm install

# 安装Python依赖
pip install -r requirements.txt
```

### 运行开发服务器

```bash
npm run dev
```

应用将在 [http://localhost:3000](http://localhost:3000) 启动。

## 部署选项

### Vercel部署

1. 将代码推送到GitHub仓库
2. 在Vercel中导入项目
3. 自动部署完成

Vercel会自动识别Next.js项目和Python API路由。

> **注意**: Vercel serverless函数有大小限制，如果`markitdown[all]`及其依赖超过限制，系统会自动使用轻量级模式。

### 本地部署 (推荐完整功能)

如需完整PDF、Office文档支持，建议本地部署：

```bash
# 安装完整依赖（包括二进制库）
pip install markitdown[all]

# 启动应用
npm run dev
```

### 其他云平台

可部署到任何支持Next.js和Python的云平台，如Railway、Render、DigitalOcean等。

## 使用方法

1. 访问应用首页
2. 拖拽文件到上传区域，或点击选择文件
3. 等待转换完成
4. 预览转换结果
5. 点击下载按钮获取.md文件

## 开源协议

MIT License

## 致谢

- [Microsoft MarkItDown](https://github.com/microsoft/markitdown) - 强大的文档转换库
- [Next.js](https://nextjs.org/) - React全栈框架
- [Vercel](https://vercel.com/) - 部署平台
