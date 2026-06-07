# OpenCode CLI Skill

💻 一个用于在各类自动化流程或 AI 助手中调用 **OpenCode CLI** 的通用 Skill。

## 🚀 主要功能

- **任务委派**：通过 `opencode run` 将复杂的代码分析、重构和解释任务委派给 OpenCode。
- **服务化接入**：支持连接已有的 `opencode serve` 后端（通过 `OPENCODE_SERVER_URL`），降低冷启动延迟。
- **会话管理**：支持会话延续（`--continue`）、分支（`--fork`）以及指定历史 Session。
- **协议集成**：提供 ACP (Agent Client Protocol) 模式支持，便于 nd-JSON 流式集成。
- **便捷脚本**：内置 `scripts/opencode_run.py` 辅助脚本，简化命令构造和 JSON 输出解析。

## 📦 目录结构

- `SKILL.md`: Skill 的主定义文件，包含元数据、触发场景和工作流指令。
- `references/`: 包含 OpenCode CLI 的详细命令参考。
- `scripts/`: 包含可执行的辅助脚本，用于在非交互环境下调用 OpenCode。

## ⚙️ 依赖要求

- **二进制文件**: [opencode](https://opencode.ai) (需安装并添加到 PATH)
- **环境变量**:
  - `OPENCODE_SERVER_URL`: (可选) OpenCode Server 地址，默认 `http://127.0.0.1:4096`。
  - `OPENCODE_SERVER_PASSWORD`: (可选) 连接 Server 的身份验证令牌。

## 🛠️ 快速开始

### 1. 安装 Skill

将本仓库作为一个 Skill 包安装到你的 AI 助手或自动化运行环境中。常见方式是复制整个目录。

```bash
# 示例：将源码目录复制到宿主的 skills 目录
cp -R opencode-cli /path/to/your/skills/
```

安装后，确保宿主能够读取 `SKILL.md`，并且 `opencode` 已安装且在 `PATH` 中。

### 2. 使用 Skill

在宿主对话或自动化任务中直接描述 OpenCode CLI 相关需求，例如：

```text
使用 opencode 分析当前项目的代码结构
```

```text
调用 opencode run 审查 src/main.ts，并输出关键问题和修改建议
```

```text
连接已有的 opencode serve，复用 OPENCODE_SERVER_URL 执行本次分析
```