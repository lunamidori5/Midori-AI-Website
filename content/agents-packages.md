+++
disableToc = false
title = "Midori AI Agents Packages"
weight = 10
+++

![agents-packages-banner](https://tea-cup.midori-ai.xyz/download/logo_color1.png)

## Large Reasoning Model Agents Ecosystem

**Midori AI Agents Packages** is a comprehensive Python ecosystem for building Large Reasoning Model (LRM) agent systems. This modular collection provides everything needed to create sophisticated LRM agents with memory, reasoning, emotion, and security capabilities.

Built with a protocol-based architecture, the packages offer interchangeable backends, encrypted media handling, sophisticated mood systems, and advanced context management—all designed to work together seamlessly while remaining independently usable.

## Key Features

- **Multi-Backend Support** - Choose from OpenAI, Langchain, or fully local HuggingFace inference
- **Persistent Memory** - Context management with time-based decay and intelligent trimming
- **Emotion Simulation** - 28+ hormone system with PyTorch-based self-retraining
- **Encrypted Media** - Layered encryption with lifecycle management
- **Vector Storage** - Semantic search with ChromaDB and multimodal support
- **Advanced Reranking** - Filter-first architecture with LLM-optional reranking
- **Multi-Model Reasoning** - Consolidate outputs from multiple reasoning models
- **100% Async** - All I/O operations are async-compatible
- **Protocol-Based Design** - ABC interfaces enable plug-and-play component switching

## Package Overview

### Core Agent Infrastructure

#### **midori-ai-agent-base**
Foundation package providing common protocols and data models for all agent backends.

**Features:**
- `MidoriAiAgentProtocol` abstract base class
- Standardized `AgentPayload` and `AgentResponse` models
- Factory function for backend selection
- TOML-based configuration support
- Memory integration with `MemoryEntryData`

#### **midori-ai-agent-langchain**
Langchain-based agent implementation with tool binding support.

**Features:**
- Uses `langchain-openai` for model invocation
- 100% async with `ainvoke()`
- Configurable temperature and context window (up to 128K tokens)
- Tool execution capabilities

#### **midori-ai-agent-openai**
OpenAI Agents SDK implementation for official OpenAI integration.

**Features:**
- Uses `openai-agents` library with `Agent` and `Runner`
- Full async support with `Runner.run_async()`
- Compatible with OpenAI-style APIs
- Tool execution support

#### **midori-ai-agent-huggingface**
Fully local LLM inference without external servers—complete privacy.

**Features:**
- **No server required** - Unlike Ollama/vLLM/LocalAI
- **Offline capable** after initial model download
- **Streaming support** for real-time generation
- **Lazy loading** with reference counting
- **Quantization support** (8-bit/4-bit via bitsandbytes)
- **Recommended models**: TinyLlama (testing), Phi-2 (dev), Llama-2/Mistral (production)

#### **midori-ai-agent-context-manager**
Context management and conversation history persistence.

**Features:**
- In-RAM conversation tracking with disk persistence
- Tool call tracking with `ToolCallEntry`
- Memory limits with automatic trimming
- Conversation summaries for long sessions
- JSON serialization via Pydantic
- Entry-level and store-level metadata

### Intelligence & Processing

#### **midori-ai-compactor**
Multi-model reasoning consolidation using agent-powered merging.

**Features:**
- Accepts any number of reasoning model outputs
- Language-agnostic consolidation
- Customizable consolidation prompts
- Returns single, easy-to-parse message string

#### **midori-ai-context-bridge**
Persistent thinking cache with time-based memory decay simulation.

**Features:**
- Uses `midori-ai-vector-manager` with ChromaDB backend
- Two memory types with different decay rates:
  - **PREPROCESSING**: 30 min decay → 90 min removal
  - **WORKING_AWARENESS**: 12 hour decay → 36 hour removal
- Progressive character-level corruption simulation (simulates natural forgetting)
- Session-based memory management
- Automatic cleanup of expired entries

#### **midori-ai-mood-engine**
Comprehensive mood management with hormone simulation and self-retraining.

**Features:**
- **28+ hormones** across 4 categories (reproductive, stress, mood, metabolism)
- **28-day menstrual cycle** support with phase tracking
- **Loneliness tracking** with social need accumulation
- **Energy modeling** with circadian rhythm
- **PyTorch-based self-retraining** from user feedback
- **Impact API**: stress, relaxation, exercise, meals, sleep, social interaction
- **Three resolution modes**:
  - DAY: 28 steps (once per day)
  - PULSE: 448 steps (16 per day)
  - FULL: 80,640 steps (30-second intervals)
- **Encrypted model persistence** via media-vault

#### **midori-ai-reranker**
LangChain-powered document reranking and filtering system.

**Features:**
- **Filter-first architecture** using LangChain transformers (fast)
- **Redundancy removal** via `EmbeddingsRedundantFilter`
- **Relevance filtering** with configurable thresholds
- **Threshold modifiers** for per-query tuning
- **Sender prioritization** (user vs model content)
- **Optional LLM reranking** (heavyweight, more accurate)
- **Multiple embedding providers**: OpenAI, LocalAI, Ollama

#### **midori-ai-vector-manager**
Protocol-based vector storage abstraction with ChromaDB backend.

**Features:**
- `VectorStoreProtocol` ABC for future backend support
- ChromaDB implementation with persistence
- **Multimodal support** (text + images via OpenCLIP)
- `SenderType` enum for reranking integration
- Default persistence: `~/.midoriai/vectorstore/`
- Time-gating option for permanent knowledge storage
- Custom embedding function support

### Media Management

#### **midori-ai-media-vault**
Encrypted media storage with Pydantic models and layered security.

**Features:**
- **Per-file random Fernet encryption keys**
- **Onion/layered encryption** with system-stats-derived keys
- **SHA-256 integrity verification**
- **Supports**: photos, videos, audio, text
- **Type-organized folder structure**
- **Fast `list_by_type()`** without decryption
- **12 iterations** for key derivation

#### **midori-ai-media-lifecycle**
Time-based media lifecycle management with probabilistic parsing.

**Features:**
- **Parsing probability decay** (default: 35 min full → 90 min zero)
- Configurable `DecayConfig` at manager level
- Automatic cleanup scheduler
- Lifecycle tracking (saved/loaded/parsed timestamps)
- Probabilistic parse decisions based on age

#### **midori-ai-media-request**
Type-safe media request/response protocol with priority queuing.

**Features:**
- Type validation (requested vs stored type)
- **Priority-based queuing**: LOW, NORMAL, HIGH, CRITICAL
- Decay-aware responses
- **Status tracking**: PENDING, APPROVED, DENIED, PROCESSING, COMPLETED, EXPIRED
- Integration with lifecycle manager

### Utilities & Meta-Packages

#### **midori-ai-agents-all**
Meta-package bundling ALL packages with embedded documentation.

**Features:**
- Single installation command for entire ecosystem
- Programmatic documentation access via constants
- `list_all_docs()` function for exploration
- Enables offline doc browsing
- Useful for building doc search tools

#### **midori-ai-agents-demo**
Complete LRM pipeline demonstration (NOT production-ready).

**Features:**
- Stage-based architecture: Preprocessing → Working Awareness → Compaction → Reranking → Final Response
- Integration blueprint for all packages
- Observable with metrics and tracing
- Configuration-driven behavior
- Multiple examples: simple, full, parallel, custom stages

## Getting Started

{{< tabs >}}
{{% tab title="Install All Packages" %}}

### Using UV (Recommended)

```bash
uv add "git+https://github.com/Midori-AI-OSS/agents-packages.git#subdirectory=midori-ai-agents-all"
```

### Using Pip

```bash
pip install "git+https://github.com/Midori-AI-OSS/agents-packages.git#subdirectory=midori-ai-agents-all"
```

This installs the entire ecosystem in one command, including all dependencies and embedded documentation.

{{% /tab %}}
{{% tab title="Install Individual Packages" %}}

### Install Only What You Need

Each package can be installed independently:

```bash
# Install just the compactor
uv add "git+https://github.com/Midori-AI-OSS/agents-packages.git#subdirectory=midori-ai-compactor"

# Install just the mood engine
uv add "git+https://github.com/Midori-AI-OSS/agents-packages.git#subdirectory=midori-ai-mood-engine"

# Install context manager
uv add "git+https://github.com/Midori-AI-OSS/agents-packages.git#subdirectory=midori-ai-agent-context-manager"
```

Replace the subdirectory path with any package name from the overview above.

{{% /tab %}}
{{% tab title="Basic Usage" %}}

### Simple Agent Example

```python
from midori_ai_agent_base import create_agent, AgentPayload

# Create agent (auto-selects backend from config.toml)
agent = create_agent()

# Prepare payload
payload = AgentPayload(
    messages=[{"role": "user", "content": "Hello, world!"}],
    model="gpt-4",
    temperature=0.7
)

# Invoke agent
response = await agent.ainvoke(payload)
print(response.content)
```

### With Memory and Context

```python
from midori_ai_agent_context_manager import ContextManager

# Initialize context manager
context = ContextManager(max_entries=100)

# Add user message
context.add_entry(role="user", content="What's 2+2?")

# Get messages for agent
messages = context.get_messages()

# Create payload with context
payload = AgentPayload(messages=messages, model="gpt-4")
response = await agent.ainvoke(payload)

# Save assistant response to context
context.add_entry(role="assistant", content=response.content)
```

### Full Example with Demo Package

```python
# See midori-ai-agents-demo for complete examples
from midori_ai_agents_demo import run_simple_pipeline

# Run complete LRM pipeline
result = await run_simple_pipeline(
    user_input="Explain quantum computing",
    config_path="config.toml"
)
```

{{% /tab %}}
{{< /tabs >}}

## Requirements

- **Python**: 3.11 - 3.14 (not 3.15+)
- **Package Manager**: UV (recommended) or Pip
- **Optional**: PyTorch (mood engine), bitsandbytes (quantization), ChromaDB (vector storage)

## Configuration

Most packages support TOML configuration files (`config.toml`):

```toml
[agent]
backend = "openai"  # or "langchain", "huggingface"
model = "gpt-4"
temperature = 0.7

[context]
max_entries = 100
trim_on_limit = true

[vector_store]
persist_directory = "~/.midoriai/vectorstore/"

[mood_engine]
resolution = "PULSE"  # or "DAY", "FULL"
```

Environment variables for API keys:
- `OPENAI_API_KEY` - For OpenAI backend
- `HF_TOKEN` - For HuggingFace downloads

## Use Cases

- **LRM System Development** - Building Large Reasoning Model applications
- **Conversational AI** - Chatbots/assistants with persistent memory
- **Local AI Inference** - Running AI agents completely offline
- **Emotion-Aware Systems** - Applications requiring mood/emotion tracking
- **Secure Media Handling** - Encrypted storage and lifecycle management
- **RAG Systems** - Retrieval-augmented generation with vector storage
- **Multi-Model Reasoning** - Combining outputs from multiple reasoning models
- **Discord Bots** - Sophisticated conversational bots (see Carly-AGI project)

## Architecture Highlights

### Protocol-Based Design
All components implement standardized ABC interfaces, enabling plug-and-play backend switching without code changes.

### Monorepo with Independent Packages
All packages live in one repository but are independently installable via Git subdirectory syntax.

### Memory Decay Simulation
The context bridge simulates natural forgetting with progressive character-level corruption over time.

### Filter-First Performance
The reranker prioritizes fast embedding-based filters over slow LLM-based reranking for optimal performance.

### Lazy Loading
HuggingFace models load on first use, not initialization, reducing memory footprint.

### Onion Encryption
Media vault uses layered encryption: per-file random keys + system-stats-derived keys with 12 key derivation iterations.

## Real-World Application

The Midori AI Agents Packages ecosystem powers **Carly-AGI**, a sophisticated Discord bot featuring:
- Multi-model reasoning consolidation
- Persistent conversational memory
- Advanced mood and emotion simulation
- Secure encrypted media handling
- Vector-based context retrieval
- Time-based memory decay

See the [Carly-AGI project]({{< relref "about-us/carly-api.md" >}}) for a production implementation.

## Documentation

Comprehensive documentation is included with every package:

- **Package READMEs** - 200-500+ lines per package
- **USAGE.md** - Step-by-step scenarios and tutorials
- **AGENTS.md** - Contributor guide with mode documentation
- **Embedded Docs** - All documentation accessible programmatically via `midori-ai-agents-all`
- **Demo Examples** - 6+ working examples in demo package

### Accessing Embedded Documentation

```python
from midori_ai_agents_all import list_all_docs

# List all available documentation
docs = list_all_docs()
for name, content in docs.items():
    print(f"=== {name} ===")
    print(content[:200])  # Preview first 200 chars
```

## Performance Characteristics

- **Context Window**: Up to 128K tokens (model-dependent)
- **Memory Decay**: Configurable from minutes to days
- **Vector Storage**: Default persistence to `~/.midoriai/vectorstore/`
- **Encryption**: 12 iterations for key derivation
- **Mood Resolution**: Up to 80,640 steps (30-second intervals over 28 days)

## Support and Assistance

- **GitHub Repository**: [Midori-AI-OSS/agents-packages](https://github.com/Midori-AI-OSS/agents-packages)
- **Comprehensive Documentation**: Included in every package
- **Community Support**: [Join our Discord](https://discord.gg/xdgCx3VyHU)
- **Email**: [contact@midori-ai.xyz](mailto:contact@midori-ai.xyz)

{{% notice style="warning" title="Production Note" %}}
The **midori-ai-agents-demo** package is explicitly marked as **NOT production-ready**. It's a showcase and integration blueprint. For production use, integrate the core packages (agent-base, context-manager, vector-manager, etc.) directly into your application.
{{% /notice %}}

{{% notice style="info" title="Modern Python Tooling" %}}
This project uses **UV** as the primary package manager for faster, more reliable dependency management. While pip is supported, we strongly recommend UV for the best development experience.
{{% /notice %}}
