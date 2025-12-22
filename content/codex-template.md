+++
disableToc = false
title = "Codex Contributor Template"
weight = 11
+++

![codex-template-banner](https://tea-cup.midori-ai.xyz/download/logo_color1.png)

## LRM-Native Collaboration Framework

The **Codex Contributor Template** is a standardized framework for establishing structured, LRM-assisted collaboration workflows in software development repositories. It provides a reusable foundation for implementing role-based contributor coordination systems using a `.codex/` directory structure.

Designed from the ground up for LRM-assisted development, this template enables teams to leverage tools like GitHub Copilot, Claude, and other LRM assistants with clear, structured context while maintaining human oversight and accountability.

{{% notice style="info" title="Template in Action" %}}
This template is actively used across all Midori AI projects including Carly-AGI, Endless Autofighter, and this website itself. See the real-world implementation in our [GitHub repositories](https://github.com/Midori-AI-OSS).
{{% /notice %}}

## Key Features

- **9 Specialized Contributor Modes** - Clear role definitions with explicit boundaries (Task Master, Coder, Reviewer, Auditor, Manager, Blogger, Brainstormer, Prompter, Storyteller)
- **Protocol-Based Workflow** - Structured handoff mechanisms like TMT (Task Master Ticket) system
- **LRM-Native Design** - Optimized for LRM assistant consumption while remaining human-readable
- **Framework-Agnostic** - No project-specific tooling requirements, works with any tech stack
- **Audit Trail Emphasis** - Comprehensive documentation of decisions, reviews, and process evolution
- **Hash-Prefixed File Naming** - Unique trackable filenames using `openssl rand -hex 4`
- **Role Separation** - Clear boundaries prevent scope creep (e.g., Task Masters never edit code)
- **Cheat Sheet Culture** - Quick-reference guides maintained by each role

## What's Included

### Core Documentation

- **`AGENTS.md`** - Root-level contributor guide defining workflow practices, communication protocols, and mode selection rules
- **`.codex/modes/`** - Directory containing 9 specialized contributor mode guides with detailed role-specific guidelines

### Directory Structure

The template defines a comprehensive `.codex/` hierarchy:

```
.codex/
├── modes/              # Contributor role definitions
├── tasks/              # Active work items with unique hash-prefixed filenames
├── notes/              # Process notes and service-level conventions
├── implementation/     # Technical documentation accompanying code
├── reviews/            # Review notes and audit findings
├── audit/              # Comprehensive audit reports
├── ideas/              # Ideation session outputs
├── prompts/            # Reusable prompt templates
├── lore/               # Narrative context and storytelling materials
├── tools/              # Contributor cheat sheets and quick references
└── blog/               # Staged blog posts and announcements
```

## The Nine Contributor Modes

### **Task Master Mode**
Coordinates work backlog, translates requirements into actionable tasks, maintains task health and priority. Creates hash-prefixed task files and never directly edits code.

### **Manager Mode**
Maintains contributor instructions, updates mode documentation, aligns process updates with stakeholders. Ensures `.codex/` documentation stays synchronized with project reality.

### **Coder Mode**
Implements features, writes tests, maintains code quality and technical documentation. Focuses on implementation without managing work backlog.

### **Reviewer Mode**
Audits documentation for accuracy, identifies outdated guidance, creates actionable follow-up tasks. Analysis-only mode that creates TMT tickets for Task Masters.

### **Auditor Mode**
Performs comprehensive code/documentation reviews, verifies compliance, security, and quality standards. More thorough than Reviewer mode.

### **Blogger Mode**
Communicates repository changes to community, creates platform-specific content with consistent voice. Drafts posts in `.codex/blog/` before publication.

### **Brainstormer Mode**
Drives collaborative ideation, explores solution alternatives, captures design trade-offs. Documents ideas in `.codex/ideas/`.

### **Prompter Mode**
Crafts high-quality prompts for LRM models, documents effective patterns, maintains prompt libraries in `.codex/prompts/`.

### **Storyteller Mode**
Maintains narrative consistency, organizes world lore/product storytelling, clarifies stakeholder vision. Manages `.codex/lore/`.

## Use Cases

- **Multi-repository consistency** - Standardizing collaboration practices across project portfolios
- **LRM-assisted development** - Providing structured context for LRM coding assistants
- **Open source projects** - Onboarding contributors with clear role definitions
- **Team coordination** - Establishing clear boundaries between contributor responsibilities
- **Documentation-driven development** - Maintaining synchronized code and documentation
- **Distributed teams** - Enabling asynchronous collaboration with well-defined workflows

## Getting Started

{{< tabs >}}
{{% tab title="Quick Setup" %}}

### 1. Clone the Template

```bash
git clone https://github.com/Midori-AI-OSS/codex_template_repo.git /tmp/codex-template
```

### 2. Copy Core Files

```bash
# Copy to your repository root
cp /tmp/codex-template/AGENTS.md ./
cp -r /tmp/codex-template/.codex ./
```

### 3. Customize for Your Project

- Replace placeholder text in `AGENTS.md` with project-specific instructions
- Update communication protocols and team channels
- Adjust mode definitions to match your workflow
- Create initial task examples in `.codex/tasks/`
- Document tooling in `.codex/tools/`

### 4. Commit and Share

```bash
git add AGENTS.md .codex/
git commit -m "[DOCS] Add Codex Contributor Template"
git push
```

{{% /tab %}}
{{% tab title="LRM Assistant Setup" %}}

### Using with GitHub Copilot

The template is designed to work seamlessly with GitHub Copilot. Once installed, you can invoke modes directly:

```markdown
@workspace Task Master, please review task priorities in .codex/tasks/
```

### Mode Invocation Pattern

When requesting a specific mode, start with the role name:

- "**Task Master**, what are the current priorities?"
- "**Reviewer**, please audit the authentication documentation"
- "**Coder**, implement the login feature from task abc123def"

{{% /tab %}}
{{% tab title="Customization Guide" %}}

### Essential Customizations

**1. Update Team Communication Channels**
In `AGENTS.md`, replace placeholders with your team's channels:
- Discord server/channels
- Slack workspaces
- Email contacts
- Issue tracker URLs

**2. Document Environment Setup**
Add project-specific setup instructions:
- Language/runtime versions
- Package managers
- Build tools
- IDE recommendations

**3. Create Initial Cheat Sheets**
In `.codex/tools/`, create quick-reference guides:
- Common commands
- Testing procedures
- Deployment steps
- Code style conventions

**4. Configure Active Modes**
Remove unused mode files or add custom ones:
- Delete modes your team won't use
- Create project-specific modes if needed
- Update mode guidelines for your workflow

**5. Synchronize Documentation**
Ensure consistency across:
- `.codex/tasks/` - Active work items
- `.codex/implementation/` - Technical docs
- `.codex/notes/` - Process conventions

{{% /tab %}}
{{< /tabs >}}

## File Naming Convention

The template uses a unique hash-prefix system for trackability:

```bash
# Generate unique prefix
openssl rand -hex 4
# Example output: abc123def

# Create task file
touch .codex/tasks/abc123def-implement-login-feature.md
```

This ensures:
- Unique identifiers across all tasks
- Easy cross-referencing in discussions
- Simple conflict resolution in version control
- Clear audit trail

## Workflow Examples

### Task Master Creating Tasks

1. Draft new task files in `.codex/tasks/`
2. Use hash-prefixed filenames: `<hash>-<description>.md`
3. Include: purpose, acceptance criteria, priority
4. Archive completed tasks to `.codex/tasks/archive/`
5. Update priorities and metadata regularly

### Reviewer Creating TMT Tickets

1. Audit existing documentation
2. Identify issues or outdated content
3. Create `TMT-<hash>-<description>.md` in `.codex/tasks/`
4. Hand off to Task Master for prioritization
5. Task Master schedules work for Coders

### Blogger Publishing Updates

1. Gather changes from last 5-10 commits
2. Draft platform-specific posts (Twitter, Discord, blog)
3. Stage content in `.codex/blog/`
4. Review with team
5. Publish and remove temporary files

## Why Use This Template?

- **Reduces onboarding friction** - Clear role definitions help new contributors start quickly
- **Prevents scope creep** - Mode boundaries limit unintended work expansion
- **Facilitates code review** - Structured documentation trails make reviews thorough
- **Enables async collaboration** - Well-documented context reduces synchronous communication needs
- **Scales across projects** - Single template applies to multiple repositories
- **Future-proof** - Framework-agnostic design adapts to evolving toolchains
- **LRM-compatible** - Structured context dramatically improves LRM assistant performance

## Support and Assistance

- **GitHub Repository**: [Midori-AI-OSS/codex_template_repo](https://github.com/Midori-AI-OSS/codex_template_repo)
- **Documentation**: Comprehensive guides included in template
- **Community Support**: [Join our Discord](https://discord.gg/xdgCx3VyHU)
- **Email**: [contact@midori-ai.xyz](mailto:contact@midori-ai.xyz)