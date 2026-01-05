+++
disableToc = false
title = "Agents Runner"
weight = 10
+++

![agent-runner-banner](https://tea-cup.midori-ai.xyz/download/logo_color1.png)

## Agents Runner: A GUI for AI Coding Agents

Agents Runner is a PySide6-based desktop application for orchestrating AI coding agents inside Docker containers. It provides a unified interface for managing workspaces, configuring environments, launching interactive terminal sessions, and handling GitHub branch/PR workflows—all without touching the command line.

Built on Python 3.13+ with a modern async architecture, Agents Runner streamlines the process of running AI agents like OpenAI Codex, Claude Code, GitHub Copilot, and Google Gemini in consistent, isolated containerized environments.

## Key Features

- **Multi-Agent Support** - Run OpenAI Codex, Claude Code, GitHub Copilot, or Google Gemini from a single interface
- **Docker Integration** - Executes agents inside `lunamidori5/pixelarch:emerald` containers for consistent environments
- **Interactive Mode** - Launch TTY sessions in your terminal emulator (Linux/macOS) for direct agent TUI access
- **Environment Management** - Configure multiple workspaces with custom settings, mounts, and environment variables
- **GitHub Workflow** - Automatic branch creation, task ID tracking, and PR management via `gh` CLI integration
- **Preflight Scripts** - Run custom setup commands before each container launch
- **Task Dashboard** - Track running agents, view logs, and manage task queues from a central dashboard
- **Capacity Control** - Limit concurrent agent runs with configurable max-agent settings
- **Persistent State** - Saves window size, environment configs, and task history across sessions

## Supported Agents

| Agent | CLI Tool | Status |
|-------|----------|--------|
| **OpenAI Codex** | `codex` | ✅ Fully Supported |
| **Claude Code** | `claude` | ⚠️ Beta - [Report Issues](https://github.com/Midori-AI-OSS/Midori-AI/issues) |
| **GitHub Copilot** | `github-copilot-cli` | ⚠️ Beta - [Report Issues](https://github.com/Midori-AI-OSS/Midori-AI/issues) |
| **Google Gemini** | `gemini` | ⚠️ Beta - [Report Issues](https://github.com/Midori-AI-OSS/Midori-AI/issues) |

## Getting Started

### Prerequisites

- Python 3.13+
- Docker installed and running
- `uv` package manager ([install uv](https://docs.astral.sh/uv/getting-started/installation/))
- Agent CLI tools installed (Codex, Claude, Copilot, or Gemini)

### Run the Application

```bash
git clone https://github.com/Midori-AI-OSS/Agents-Runner.git
cd Agents-Runner
uv run main.py
```

The GUI will launch and you can immediately start configuring environments and running agents.

Agent configs are mounted from host directories (`~/.codex`, `~/.claude`, `~/.copilot`, `~/.gemini`) into the container at `/home/midori-ai/.{agent}`.

## Usage

### Creating a New Task

1. Click **"New Task"** from the dashboard
2. Enter your prompt describing what you want the agent to do
3. Select the target environment from the dropdown
4. Choose your preferred agent (Codex, Claude, Copilot, Gemini)
5. Click **"Run Agent"** to start in background mode, or **"Run Interactive"** for TTY access

### Interactive Mode

Use **"Run Interactive"** to launch a TTY session that opens your terminal emulator with direct access to the agent's TUI. This is useful for:

- Real-time conversation with the agent
- Reviewing and approving changes interactively
- Debugging agent behavior

### Container Arguments

You can pass additional CLI flags to the agent by entering them in the **Container Args** field:

- Flags starting with `-` are passed directly to the agent CLI
- Other strings (like `bash`) are executed as shell commands inside the container

## Configuration

### File Locations

| File | Purpose |
|------|---------|
| `~/.midoriai/agents-runner/state.json` | Application state (window size, settings) |
| `~/.midoriai/agents-runner/environment-*.json` | Environment configurations |
| `~/.codex`, `~/.claude`, `~/.copilot`, `~/.gemini` | Agent config directories (mounted into containers) |

### Environment Variables

- `AGENTS_RUNNER_STATE_PATH` - Override the default state file location
- `CODEX_HOST_WORKDIR` - Default working directory for new environments
- `CODEX_HOST_CODEX_DIR` - Custom path for Codex config directory

### Environment Settings

Each environment can be configured with:

- **Workspace Path** - Local directory to mount as the agent's working directory
- **GitHub Repo** - Optional GitHub repository for automatic branch/PR management
- **Custom Mounts** - Additional volume mounts for the container
- **Environment Variables** - Custom env vars passed to the agent
- **Preflight Script** - Shell commands to run before launching the agent

## Architecture

Agents Runner uses a modular architecture with clear separation of concerns:

```
agents_runner/
├── app.py              # Application entry point
├── ui/                 # PySide6 UI components
│   ├── main_window.py  # Main application window
│   ├── pages/          # Dashboard, Settings, Task pages
│   └── widgets/        # Reusable UI components
├── docker/             # Docker container management
├── environments/       # Environment configuration models
├── gh/                 # GitHub CLI integration
└── preflights/         # Preflight script execution
```

## Links & Resources

- **Repository:** https://github.com/Midori-AI-OSS/Agents-Runner
- **Issues:** https://github.com/Midori-AI-OSS/Agents-Runner/issues
- **Discord:** https://discord.gg/xdgCx3VyHU
