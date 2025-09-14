# Markdown Converter

一个极简的文档转Markdown工具，基于Microsoft MarkItDown库构建。

## 功能特点

- 🚀 **极简设计** - 拖拽上传，一键转换
- 📄 **多格式支持** - PDF、Word、Excel、PowerPoint、图片等
- ⚡ **即时预览** - 转换完成后立即预览Markdown内容
- 💾 **一键下载** - 支持直接下载转换后的.md文件
- 🌙 **暗黑模式** - 自适应明暗主题
- ☁️ **云端部署** - 基于Vercel的无服务器架构

## 技术栈

- **前端**: Next.js 15 + TypeScript + Tailwind CSS
- **后端**: Python + Microsoft MarkItDown
- **部署**: Vercel

## 支持的文件格式

**轻量级版本 (Vercel部署)**:
- 文本文件 (.txt)
- HTML文件 (.html, .htm)
- CSV文件 (.csv)

**完整版本 (本地部署)**:
- PDF文档
- Microsoft Word (.docx)
- Microsoft Excel (.xlsx)
- Microsoft PowerPoint (.pptx)
- 文本文件 (.txt)
- HTML文件 (.html)
- RTF文档 (.rtf)
- 图片文件 (.jpg, .jpeg, .png)

> **注意**: 由于Vercel serverless函数大小限制，在线版本使用轻量级转换器。如需完整功能支持，请本地部署并安装 `markitdown[all]`。

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

## 部署到Vercel

1. 将代码推送到GitHub仓库
2. 在Vercel中导入项目
3. 自动部署完成

Vercel会自动识别Next.js项目和Python API路由。

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
