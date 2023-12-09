# Eirlys
Discord bot once written in Python, but now rust.

# To add / implement
```
- [ ] Create all anilist functions (Search, User, Affinity, Database)
- [ ] Add Discord Components and incorporate the anilist commands within them
- [X] SQL DB
- [ ] Cache things (Scores, Animes, Mangas)
- [ ] Refactor some of the code (some things are ugly -> get_queries)
- [ ] After finishing the commands, revamp the loggers, so I know which commands have been called
```

# How to use
```
git clone https://github.com/tomosus/eirlys-rs
cd eirlys-rs

touch .env # Creates .env file
Inside of the .env include TOKEN="token" and DB_URL="DB URL (example: postgres://)

cargo run
```