# Statbot: NFL Player Data Discord Bot

Statbot is a Discord bot designed to bring NFL fans closer to the game by providing instant access to both current and historical player data. Whether you're looking for the latest stats on your favorite quarterback or diving into historical performances, Statbot has you covered.

## Features

- **Current Player Stats**: Get the latest stats for any active NFL player.
- **Historical Data**: Dive deep into the historical performance of players, comparing different eras of the NFL.
- **Player Comparisons**: Directly compare stats between two players. *** Coming Soon ***
- **Interactive Charts**: Visual representations of player stats over time. *** Coming Soon ***

## Getting Started

### Prerequisites

- Discord account
- Permission to add bots to a Discord server

### Installation

1. Invite Statbot to your Discord server by clicking on this https://discord.com/api/oauth2/authorize?client_id=1159784834458206278&permissions=277025512512&scope=bot(#).
2. Ensure you have the necessary permissions on your Discord server to add bots.
3. Follow the on-screen instructions to authorize Statbot on your server.

### Configuration

- Use `$statbothelp` for help using Statbot.

## Commands

- `$statbot <player_name> <week_of_season> <recap> <year>`: Fetches all stats for the specified player for any week and year.
- `$statbot <player_name> <week_of_season> <specific_stat> <year>`: Fetches a specific stat for the specified player for any week and year.
- `!compare <player1_name> <player2_name>`: Compares stats between two players. *** Coming Soon ***
- `$statbothelp`: Lists all the available commands and their usage.
- `$statlist`: Lists all specific stats. Can use recap in $statbot command to get all stats

## Usage Example

User: $statbot Geno Smith 17 passing_yards 2023
Statbot: Geno Smith Passing Yards
Passing Yards: 290.00


## Acknowledgments

- NFL for the player data
- Discord.py for the bot framework
- Our community of NFL fans
