+++
disableToc = false
title = "Stained Glass Odyssey: Idle"
weight = 2
+++

![stained-glass-odyssey-idle-banner](https://tea-cup.midori-ai.xyz/download/logo_color1.png)

## Stained Glass Odyssey: Idle

Stained Glass Odyssey: Idle is a PySide6-based desktop idle game set in the shared Stained Glass Odyssey universe. Build your party of characters, deploy them to onsite and offsite positions, and watch them battle automatically while earning experience and progression rewards—even when you're not actively playing.

The game features the same beloved characters from Stained Glass Odyssey: Endless, including Luna, Carly, Becca, and many others, each with unique damage types, stats, and abilities. Built with Python 3.13+ and a stained-glass aesthetic UI theme, the game offers a relaxing but strategic idle experience.

## Key Features

- **Idle Progression System** - Characters gain experience and stats automatically over time
- **Party Management** - Organize characters across onsite (active combat), offsite (support), and standby slots
- **Merge Mechanics** - Combine duplicate characters to increase their power
- **Shared Universe** - Same characters and lore as Stained Glass Odyssey: Endless
- **Multiple Game Modes** - Switch between active battles and idle farming
- **Persistent Saves** - Progress is saved automatically with JSON-based save files
- **Death Stat Bonuses** - Characters that fall in battle return slightly stronger
- **Risk/Reward System** - Adjust idle difficulty for better rewards

## Character System

### Roster

The game features a diverse roster of characters from the Stained Glass Odyssey world, including:

| Character | Stars | Damage Type | Role |
|-----------|-------|-------------|------|
| Luna | ⭐⭐⭐⭐⭐⭐⭐ (7★) | Generic | Summoner with lunar swords |
| Lady Fire and Ice | ⭐⭐⭐⭐⭐⭐ (6★) | Fire/Ice | Dual-element attacker |
| Lady Storm | ⭐⭐⭐⭐⭐⭐ (6★) | Wind/Lightning | Storm controller |
| Carly | ⭐⭐⭐⭐⭐ (5★) | Light | Guardian with protective barriers |
| Becca | ⭐⭐⭐⭐⭐ (5★) | Light | Offsite support with menagerie bond |
| Lady Lightning | ⭐⭐⭐⭐⭐ (5★) | Lightning | Chain damage specialist |
| Lady Wind | ⭐⭐⭐⭐⭐ (5★) | Wind | Multi-hit attacker |
| *...and many more* | | | |

### Damage Types

Each character specializes in a damage type that affects their combat behavior:

- **Fire** - Scales with missing HP, applies burning damage over time
- **Lightning** - Pops DoTs on hit, applies charged decay with stun effects
- **Ice** - Reduces enemy actions, applies frozen wounds with stack caps
- **Wind** - Repeats hits, applies erosion that reduces mitigation
- **Light** - Healing and protective abilities
- **Dark** - HP drain and sacrifice mechanics
- **Generic** - Luna's unique balanced damage type

### Stat System

Characters have a comprehensive stat system including:

- **Max HP** - Total health pool
- **ATK** - Attack power
- **Defense** - Damage reduction
- **Crit Rate / Crit Damage** - Critical hit mechanics
- **SPD** - Action speed determining turn order
- **Effect Hit Rate** - Chance to apply status effects
- **Mitigation** - Additional damage reduction layer
- **Vitality** - HP regeneration rate

## Game Modes

### Idle Mode

Deploy your party and let them farm automatically:

- Characters gain experience over time
- Party HP regenerates when idle
- Adjustable risk/reward levels for faster progression
- Shared experience bonus distributes gains across your roster

### Battle Mode

Engage in active auto-battles:

- Watch your party fight enemy waves in real-time
- Win streaks increase rewards
- Characters that fall gain permanent stat bonuses on revival
- Progress through increasingly difficult fights

### Party Builder

Manage your roster between battles:

- **Onsite Slots (4)** - Active combat participants
- **Offsite Slots (6)** - Support characters that share stats
- **Standby Slots (10)** - Reserve characters
- **Bar Slots (6)** - Quick-access character deployment
- **Shop** - Purchase new characters and reroll options
- **Party Level** - Upgrade your party's overall power

## Getting Started

{{< tabs >}}
{{% tab title="Quick Start" %}}

### Prerequisites

- Python 3.13+
- `uv` package manager ([install uv](https://docs.astral.sh/uv/getting-started/installation/))

### Run the Game

```bash
git clone https://github.com/Midori-AI-OSS/Midori-AI.git
cd Midori-AI/Endless-Idler
uv run main.py
```

The game window will open with the main menu.

{{% /tab %}}
{{% tab title="Alternative Install" %}}

### Using pip

```bash
git clone https://github.com/Midori-AI-OSS/Midori-AI.git
cd Midori-AI/Endless-Idler
pip install -e .
endless-idler
```

{{% /tab %}}
{{< /tabs >}}

## Progression Mechanics

### Experience System

- **Idle EXP** - Earned passively over time based on deployed characters
- **Battle EXP** - Earned from winning fights
- **Shared EXP** - Percentage of experience distributed to non-deployed characters
- **EXP Bonus/Penalty** - Temporary modifiers from in-game events

### Death & Revival

When a character falls in battle:

1. Their death is recorded in the save file
2. A small permanent stat bonus (0.01%) is applied to most stats
3. The character can be redeployed in future battles
4. Excluded stats: EXP, mitigation, vitality

### Tokens & Economy

- **Tokens** - Currency for purchasing characters from the shop
- **Character Cost** - Default cost to recruit a new character
- **Reroll Cost** - Cost to refresh the shop's character offerings
- **Party Level Up** - Invest tokens to increase overall party power

## Save System

The game automatically saves progress to:

```
~/.local/share/Midori AI/Stained Glass Odyssey Idle/save.json
```

Save data includes:

- Token balance and party level
- Character placements (onsite/offsite/standby/bar)
- Character progress and stats
- Death counts and initial stats for revival bonuses
- Idle mode settings (bonus time, shared EXP percentage, risk level)

## Links & Resources

- **Monorepo:** https://github.com/Midori-AI-OSS/Midori-AI
- **Source:** https://github.com/Midori-AI-OSS/Midori-AI/tree/master/Endless-Idler
- **Related Game:** [Stained Glass Odyssey: Endless]({{< relref "stained-glass-odyssey-endless.md" >}}) (Web-based auto-battler)
- **Issues:** https://github.com/Midori-AI-OSS/Midori-AI/issues
- **Discord:** https://discord.gg/xdgCx3VyHU
