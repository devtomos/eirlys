
# Eirlys.rs

Anilist Discord Bot, rewritten in Rust. | First written in Python.

## Features

```markdown
[x] SQL Database integration
[x] AniList functions (Search, User, Affinity, Database) - 90% done
[x] Discord Components integration
[ ] Caching (Scores, Animes, Mangas)
[x] Code refactoring
[x] Enhanced logging

# Keys
[x] = Implemented
[ ] = Not Implemented
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/tmqf/eirlys
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
    - `/anilist_api.rs`: Contains all of the anilist backend functions (search_media, user_search, user_scores, relation_names)
    - `/anilist_queries.rs`: Contains all the queries used for the Anilist API
    - `/database_access.rs`: Contains all of the database functions to connect, update and insert data.

- `src/commands/`: Contains the code for handling Discord commands.
    - `/anilist_commands.rs`: Contains all of the anilist commands, inwhich users can use.
    - `/gen_commands.rs`: Contains generic commands, which users may use at time to time. (Banner, Avatar etc.)
