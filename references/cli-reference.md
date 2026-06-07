# OpenCode CLI Reference

来源：`https://opencode.ai/docs/zh-cn/cli/`，用于在通用 skill 或自动化流程中调用 OpenCode CLI。

## Core Commands

### `opencode`

启动 TUI：

```bash
opencode [project]
```

常用选项：

- `--continue`, `-c`：继续上一个会话。
- `--session`, `-s`：指定会话 ID。
- `--fork`：继续时分叉会话。
- `--prompt`：指定提示词。
- `--model`, `-m`：指定模型，格式 `provider/model`。
- `--agent`：指定 Agent。
- `--port`、`--hostname`：监听端口和主机名。

### `opencode run [message..]`

非交互式调用，最适合 skill 和自动化：

```bash
opencode run --format json --dir /path/to/project "Analyze this repository"
```

重要选项：

- `--command`：运行指定命令，把 message 作为参数。
- `--continue`, `-c`：继续上一个会话。
- `--session`, `-s`：继续指定会话。
- `--fork`：继续时分叉会话。
- `--share`：分享会话；仅在用户明确要求时使用。
- `--model`, `-m`：模型，格式 `provider/model`。
- `--agent`：OpenCode Agent 名称。
- `--file`, `-f`：附加文件，可重复。
- `--format`：`default` 或 `json`。
- `--title`：设置会话标题。
- `--attach`：连接正在运行的 OpenCode server。
- `--password`, `-p`：Basic Auth 密码；优先使用环境变量 `OPENCODE_SERVER_PASSWORD`，避免命令行泄露。
- `--username`, `-u`：Basic Auth 用户名；默认 `opencode` 或环境变量 `OPENCODE_SERVER_USERNAME`。
- `--dir`：运行目录，或 attach 时远程服务器上的路径。
- `--variant`：模型变体。
- `--thinking`：显示 thinking 块；仅在明确需要调试原始 OpenCode 输出且不违反安全要求时使用。
- `--port`：本地服务器端口。

推荐调用：

```bash
opencode run --format json --dir "$PROJECT_DIR" "$PROMPT"
opencode run --format json --dir "$PROJECT_DIR" --file "$FILE" "$PROMPT"
opencode run --format json --dir "$PROJECT_DIR" --model anthropic/claude-sonnet-4 "$PROMPT"
opencode run --format json --dir "$PROJECT_DIR" --agent reviewer "$PROMPT"
opencode run --continue "$PROMPT"
opencode run --session "$SESSION_ID" "$PROMPT"
```

### `opencode serve`

启动无界面 HTTP API server。通用 skill 默认不要主动启动服务；仅在用户明确要求启动服务时，才从环境变量读取监听地址并运行：

```bash
OPENCODE_SERVER_HOSTNAME="${OPENCODE_SERVER_HOSTNAME:-127.0.0.1}"
OPENCODE_SERVER_PORT="${OPENCODE_SERVER_PORT:-4096}"
opencode serve --port "$OPENCODE_SERVER_PORT" --hostname "$OPENCODE_SERVER_HOSTNAME"
```

选项：

- `--port`：监听端口。
- `--hostname`：监听主机名。
- `--mdns`：启用 mDNS 发现。
- `--cors`：允许 CORS 的额外浏览器来源。

Basic Auth：

- `OPENCODE_SERVER_PASSWORD`：设置后启用认证。
- `OPENCODE_SERVER_USERNAME`：覆盖用户名，默认 `opencode`。

连接已存在的 server：

```bash
OPENCODE_SERVER_URL="${OPENCODE_SERVER_URL:-http://127.0.0.1:4096}"
opencode run --attach "$OPENCODE_SERVER_URL" --format json --dir "$PROJECT_DIR" "$PROMPT"
```

### `opencode attach [url]`

把 TUI 连接到 `serve` 或 `web` 启动的后端：

```bash
opencode attach http://10.20.30.40:4096
```

常用选项：`--dir`、`--continue`、`--session`、`--fork`、`--password`、`--username`。

### `opencode web`

启动带 Web 界面的无界面 server。适合浏览器 UI；纯 skill 集成通常优先使用 `serve` + `run --attach`。

### `opencode acp`

启动 Agent Client Protocol 服务，使用 stdin/stdout 与 nd-JSON：

```bash
opencode acp --cwd "$PROJECT_DIR"
```

选项：`--cwd`、`--port`、`--hostname`。

## Discovery and Management Commands

### Models

```bash
opencode models
opencode models anthropic
opencode models --refresh --verbose
```

用于发现可传给 `--model provider/model` 的模型名。

### Auth

```bash
opencode auth login
opencode auth list
opencode auth logout
```

凭据默认存储在 `~/.local/share/opencode/auth.json`。OpenCode 启动时读取凭据文件、环境变量和项目 `.env`。

### Agent

```bash
opencode agent create
opencode agent list
```

可通过 `--agent <name>` 在 `run` 中选择 Agent。

### MCP

```bash
opencode mcp add
opencode mcp list
opencode mcp auth <name>
opencode mcp logout <name>
opencode mcp debug <name>
```

只有在用户明确要求管理 OpenCode MCP 时使用。

### Sessions

```bash
opencode session list --format json --max-count 10
opencode export <sessionID>
opencode import session.json
opencode stats --project ""
```

导入、导出和分享会话可能包含隐私数据；执行前说明风险。

### Upgrade and uninstall

```bash
opencode upgrade
opencode uninstall --dry-run
```

升级或卸载只在用户明确要求时执行；卸载优先 `--dry-run`。

## Global Options

- `--help`, `-h`：显示帮助。
- `--version`, `-v`：打印版本。
- `--print-logs`：日志输出到 stderr。
- `--log-level DEBUG|INFO|WARN|ERROR`：设置日志级别。

## Environment Variables

常用变量：

- `OPENCODE_CONFIG`：配置文件路径。
- `OPENCODE_CONFIG_DIR`：配置目录路径。
- `OPENCODE_CONFIG_CONTENT`：内联 JSON 配置。
- `OPENCODE_PERMISSION`：内联 JSON 权限配置。
- `OPENCODE_CLIENT`：客户端标识，默认 `cli`。
- `OPENCODE_SERVER_PASSWORD`：为 `serve` / `web` 启用 Basic Auth。
- `OPENCODE_SERVER_USERNAME`：覆盖 Basic Auth 用户名。
- `OPENCODE_MODELS_URL`：自定义模型配置 URL。
- `OPENCODE_DISABLE_AUTOUPDATE`：禁用自动更新检查。
- `OPENCODE_DISABLE_PRUNE`：禁用旧数据清理。
- `OPENCODE_DISABLE_TERMINAL_TITLE`：禁用自动终端标题更新。
- `OPENCODE_DISABLE_DEFAULT_PLUGINS`：禁用默认插件。
- `OPENCODE_DISABLE_LSP_DOWNLOAD`：禁用 LSP 自动下载。
- `OPENCODE_DISABLE_MODELS_FETCH`：禁用远程模型获取。
- `OPENCODE_ENABLE_EXA`：启用 Exa 网络搜索工具。
- `OPENCODE_ENABLE_EXPERIMENTAL_MODELS`：启用实验性模型。
- `OPENCODE_DISABLE_AUTOCOMPACT`：禁用自动上下文压缩。

实验性变量可能变更，谨慎使用：

- `OPENCODE_EXPERIMENTAL`
- `OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX`
- `OPENCODE_EXPERIMENTAL_BASH_DEFAULT_TIMEOUT_MS`
- `OPENCODE_EXPERIMENTAL_LSP_TOOL`
- `OPENCODE_EXPERIMENTAL_PLAN_MODE`
- `OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS`
- `OPENCODE_EXPERIMENTAL_NATIVE_LLM`
- `OPENCODE_EXPERIMENTAL_PARALLEL`
- `OPENCODE_EXPERIMENTAL_WORKSPACES`

## Generic Parameter Mapping

| 通用概念 | OpenCode CLI 参数 |
|---|---|
| `projectPath` | `--dir` 或 ACP 的 `--cwd` |
| `prompt` | `opencode run [message..]` |
| `model` | `--model provider/model` |
| `agent` | `--agent` |
| `files` | 多个 `--file` |
| `sessionId` | `--session` |
| `continueLast` | `--continue` |
| `forkSession` | `--fork` |
| `jsonOutput` | `--format json` |
| `serverUrl` | `--attach` |
| `username` | `--username` 或 `OPENCODE_SERVER_USERNAME` |
| `password` | `OPENCODE_SERVER_PASSWORD` |
