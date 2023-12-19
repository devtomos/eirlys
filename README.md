
# Eirlys.rs

Anilist Discord Bot, rewritten in Rust. | First written in Python.

## Features

```markdown
[x] SQL Database integration
[ ] AniList functions (Search, User, Affinity, Database)
[ ] Discord Components integration
[ ] Caching (Scores, Animes, Mangas)
[ ] Code refactoring
[ ] Enhanced logging

# Keys
[x] = Implemented
[ ] = Not Implemented
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/tomosus/eirlys-rs
cd eirlys-rs
```

2. Create a `.env` file:

```bash
touch .env
```

3. Open the `.env` file and add your Discord token and database URL:

```env
TOKEN="your-discord-token"
DB_URL="your-database-url"
```

4. Run the bot:

```bash
cargo run
```

## Project Structure

- `src/api/`: Contains the code for interacting with the AniList API and the database.
- `src/commands/`: Contains the code for handling Discord commands.
- `src/general/`: Contains general utility functions.
