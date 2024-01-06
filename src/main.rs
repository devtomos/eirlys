mod api;
mod commands;

use std::collections::HashSet;
use std::env;
use std::sync::Arc;

use serenity::client::bridge::gateway::ShardManager;
use serenity::framework::standard::macros::group;
use serenity::framework::StandardFramework;
use serenity::http::Http;
use serenity::prelude::*;
use tracing::error;

use crate::commands::anilist_commands::*;
use crate::commands::gen_commands::*;
use crate::commands::anilist_commands::ComponentHandler;

pub struct ShardManagerContainer;
pub struct DatabasePool;

impl TypeMapKey for ShardManagerContainer {
    type Value = Arc<Mutex<ShardManager>>;
}

impl TypeMapKey for DatabasePool {
    type Value = Arc<Mutex<sqlx::postgres::PgPool>>;
}


// ------------------------------------------------------------------------------------------------------------------------ //

#[group]
#[commands(
    avatar, banner, anime, manga, fifty, user, 
    setup, server_info, server_avatar
)]
struct General;

#[tokio::main]  
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    dotenv::dotenv().expect("Failed to load .env file"); // Load local environment file
    let db_url = env::var("DB_URL").expect("Expected a DB URL in the env file");
    let pool = sqlx::postgres::PgPool::connect(&db_url).await.unwrap();
    let shared_pool = Arc::new(Mutex::new(pool));

    // Initialize the logger
    tracing_subscriber::fmt::init();
    let token = env::var("TOKEN").expect("Expected a token in the environment file");

    let http = Http::new(&token);

    // Fetch the bot's owner and id
    let (owners, _bot_id) = match http.get_current_application_info().await {
        Ok(info) => {
            let mut owners = HashSet::new();
            owners.insert(info.owner.id);

            (owners, info.id)
        }
        Err(why) => panic!("Could not access application info: {:?}", why),
    };

    // Create the framework
    let framework = StandardFramework::new()
        .configure(|c| c.owners(owners).prefix("."))
        .group(&GENERAL_GROUP);

    let intents = GatewayIntents::all();
    let mut client = Client::builder(&token, intents)
        .framework(framework)
        .event_handler(ComponentHandler)
        .await
        .expect("Error creating client");

    {
        let mut data = client.data.write().await;
        data.insert::<ShardManagerContainer>(client.shard_manager.clone());
        data.insert::<DatabasePool>(shared_pool.clone());
    }

    let shard_manager = client.shard_manager.clone();

    tokio::spawn(async move {
        tokio::signal::ctrl_c()
            .await
            .expect("Could not register ctrl+c handler");
        shard_manager.lock().await.shutdown_all().await;
    });

    if let Err(err) = client.start().await {
        error!("Client error: {:?}", err);
    }

    Ok(())
}
