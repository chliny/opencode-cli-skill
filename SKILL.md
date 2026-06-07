---
name: opencode-cli
description: "当用户要求调用 OpenCode CLI 或 opencode/opncode CLI 模式、通过 `opencode run` 委派任务、附加文件、复用会话、连接到 `opencode serve`、使用 ACP 或将 OpenCode CLI 集成到自动化流程时，应使用此 skill。"
metadata: {"openclaw": {"emoji":"💻", "requires":{"env":[], "bins":["opencode"]}}} 
---

# OpenCode CLI

## 概述

调用 OpenCode CLI 的非交互式、服务化或协议模式，把任务委派给 `opencode`，并将输出整理为调用方可消费的结果。优先使用 `opencode run`；在高频调用时连接已存在的 `opencode serve` 并使用 `run --attach`；仅在明确需要 Agent Client Protocol 时使用 `opencode acp`。

## 触发场景

使用此 skill 处理以下请求：

- 调用 OpenCode、`opencode` 或常见误写 `opncode` 的 CLI 模式。
- 通过 OpenCode 分析仓库、审查代码、解释文件、生成修改建议或执行自动化任务。
- 指定 OpenCode 模型、Agent、会话、工作目录或附加文件。
- 连接已有 OpenCode server，并从环境变量读取 `OPENCODE_SERVER_URL`。
- 需要 ACP/stdin-stdout/nd-JSON 形式的 OpenCode 集成。

## 默认工作流

1. 明确任务类型：一次性 `run`、长期 server 复用、TUI、ACP，或只查询模型/会话/认证状态。
2. 检查 `opencode` 是否可用：优先运行 `opencode --version` 或 `command -v opencode`。若不可用，只说明需要安装或配置，不自动安装，除非用户明确要求。
3. 选择工作目录：默认使用当前项目目录；跨项目时显式传入 `--dir <project_dir>`。
4. 构造最小命令：默认采用 `opencode run --format json --dir <project_dir> "$PROMPT"`。
5. 按需添加参数：`--file`、`--model`、`--agent`、`--session`、`--continue`、`--fork`、`--attach`。
6. 执行命令并读取输出：JSON 输出用于机器解析；默认输出用于人类可读结果。
7. 汇总结果：提炼 OpenCode 的最终回答、关键发现、建议动作和失败原因；不要直接倾倒冗长事件流。

## 命令模式

### 一次性 CLI 模式

```bash
opencode run --format json --dir "$PROJECT_DIR" "$PROMPT"
```

用于一次性分析、解释、审查或生成建议。若用户提供文件上下文，追加多个 `--file`：

```bash
opencode run --format json --dir "$PROJECT_DIR" --file src/main.ts --file package.json "$PROMPT"
```

### 模型与 Agent 选择

```bash
opencode run --format json --dir "$PROJECT_DIR" --model provider/model --agent reviewer "$PROMPT"
```

模型名必须使用 `provider/model` 格式。需要发现可用模型时运行 `opencode models` 或 `opencode models <provider>`。

### 会话延续

```bash
opencode run --continue "$PROMPT"
opencode run --session "$SESSION_ID" "$PROMPT"
opencode run --session "$SESSION_ID" --fork "$PROMPT"
```

仅在用户明确要求延续历史上下文、或当前任务显然依赖 OpenCode 上次会话时使用。

### 长期服务模式 (Server)

```bash
OPENCODE_SERVER_URL="${OPENCODE_SERVER_URL:-http://127.0.0.1:4096}"
opencode run --attach "$OPENCODE_SERVER_URL" --format json --dir "$PROJECT_DIR" "$PROMPT"
```

用于高频调用、减少冷启动或复用 MCP/server 初始化。仅连接已由外部启动的 `opencode serve`；不要为本次调用主动启动 `opencode serve`。若无法从环境变量获得可用地址，改用一次性 `opencode run`，或提示用户先启动服务并设置 `OPENCODE_SERVER_URL`。

### ACP 模式

```bash
opencode acp --cwd "$PROJECT_DIR"
```

仅在明确需要 Agent Client Protocol、stdin/stdout 或 nd-JSON 协议集成时使用。

### TUI 模式

```bash
opencode "$PROJECT_DIR" --prompt "$PROMPT"
```

仅在用户明确要求打开 OpenCode 交互式终端界面时使用；自动化任务优先使用 `run`。

## 辅助脚本

使用 `scripts/opencode_run.py` 可靠构造并执行 `opencode run`：

```bash
python3 scripts/opencode_run.py --dir "$PWD" --file src/main.ts "Review this file"
```

常用参数：

- `--dir <path>`：映射到 `opencode run --dir`。
- `--file <path>`：可重复，映射到多个 `--file`。
- `--model provider/model`：指定模型。
- `--agent <name>`：指定 OpenCode agent。
- `--attach <url>`：连接 `opencode serve`。
- `--session <id>`、`--continue-last`、`--fork`：控制会话。
- `--format json|default`：默认 `json`。
- `--dry-run`：只打印将执行的命令。

## 环境变量

使用此 skill 时，可能需要配置以下环境变量：

- `OPENCODE_SERVER_URL`：OpenCode Server 的连接地址（例如 `http://127.0.0.1:4096`）。若不提供，脚本或命令通常会尝试默认本地地址。
- `OPENCODE_SERVER_PASSWORD`：连接 OpenCode Server 所需的身份验证密码。建议通过环境变量转发，避免在命令行参数中明文传递。

## 安全与执行规则

- 不把宿主应用的隐藏系统提示词、内部配置、未授权凭据或私人信息发送给 OpenCode。
- 不在命令行参数中传递密码；使用 `OPENCODE_SERVER_PASSWORD` 或脚本的 `--password-env` 转发环境变量。
- 对可能修改文件、启动长期服务、分享会话、变更认证、安装 GitHub workflow、导入/导出会话、添加 MCP、升级或卸载 OpenCode 的命令，先明确风险并使用需要确认的执行方式。
- 不自动运行 `opencode upgrade`、`opencode uninstall`、`opencode github install`、`opencode mcp add`、`opencode auth login/logout`，除非用户明确要求。
- 若任务可由当前宿主环境直接可靠完成，优先直接完成；仅在用户希望使用 OpenCode 或 OpenCode 能显著提升结果时调用。

## 参考资料

需要完整 CLI 参数、环境变量和命令映射时，读取 `references/cli-reference.md`。
