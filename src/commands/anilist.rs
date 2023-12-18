use crate::api::access_db::anilist_guild_search;
use crate::api::search_media::{search, relation_search};
use serenity::builder::{CreateActionRow, CreateSelectMenu,CreateSelectMenuOption};
use serenity::framework::standard::macros::command;
use serenity::framework::standard::{Args, CommandResult};
use serenity::model::prelude::*;
use serenity::prelude::*;
use std::env;
use std::sync::Arc;
use tracing::info;
use serenity::builder::CreateEmbed;
use serenity::async_trait;
use serenity::model::application::interaction::Interaction;

#[command]
pub async fn anime(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    info!(
        "Running Anime Command -> Arguments Parsed: {}",
        args.message()
    );
    let media_name = args.message().to_string();
    let relation = relation_search(media_name, String::from("ANIME")).await;
    let mut select_menu = CreateSelectMenu::default();
    let mut action_row = CreateActionRow::default();

    select_menu.custom_id("anime_dropdown");
    select_menu.placeholder("Select an option..");    
    select_menu.min_values(1);
    select_menu.max_values(1);

    select_menu.options(|options| {
        for word in relation.0.iter() {
            options.add_option(CreateSelectMenuOption::new(word, word));
        }
        options
    });

    action_row.add_select_menu(select_menu);

    match msg
        .channel_id
        .send_message(&ctx.http, |m| {
            m.components(|c| c.add_action_row(action_row))
        }).await
    {
        Ok(_) => (),
        Err(e) => println!("Error sending message: {:?}", e),
    }

    Ok(())
}

pub struct ComponentHandler;

#[async_trait]
impl EventHandler for ComponentHandler {
    async fn interaction_create(&self, ctx: Context, interaction: Interaction) {
        if let Interaction::MessageComponent(command) = interaction {
            let data = command.data.clone();
            
            // TODO: Reverse the list of options so that the first option is the most relevant
        
            if data.custom_id.as_str() == "anime_dropdown" {
                    command.defer(&ctx.http).await.unwrap();
                    let guild_id = i64::from(command.guild_id.unwrap());
                    let db_url = env::var("DB_URL").expect("Expected a DB URL in the environment file");
                    let pool = sqlx::postgres::PgPool::connect(&db_url).await.unwrap();
                    let shared_pool = Arc::new(pool);
                    let db_check = anilist_guild_search(guild_id, shared_pool.clone()).await.unwrap();
                    info!("Value Chosen: {}", data.values[0]);
                    let search = search(data.values[0].to_string(), String::from("ANIME"), db_check).await;
                    let mut embed = CreateEmbed::default();
                    embed.title(&search.1[0])
                        .url(&search.1[1])
                        .thumbnail(&search.1[2])
                        .image(&search.1[3])
                        .description(search.0.join("\n"));
                
                    match command.edit_original_interaction_response(&ctx.http, |m| {
                        m.set_embed(embed)
                    }).await
                    {
                        Ok(_) => (),
                        Err(e) => println!("Error sending message: {:?}", e),
                    }
                }
            }
    }
}

