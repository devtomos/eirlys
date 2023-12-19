use crate::api::access_db::anilist_guild_search;
use crate::api::search_media::{search, relation_names};
use serenity::framework::standard::macros::command;
use serenity::framework::standard::{Args, CommandResult};
use serenity::builder::{CreateEmbed, CreateSelectMenuOption, CreateSelectMenuOptions, CreateSelectMenu, CreateActionRow};
use serenity::model::prelude::*;
use serenity::prelude::*;
use std::env;
use std::sync::Arc;
use tracing::info;
use serenity::async_trait;
use serenity::model::application::interaction::Interaction;

#[command]
pub async fn anime(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let media_name = args.message().to_string();
    let all_media = relation_names(media_name, String::from("ANIME")).await;

    let mut select_menu = CreateSelectMenu::default();
    let options = CreateSelectMenuOptions::default();
    select_menu.min_values(1);
    select_menu.placeholder("Select an anime");
    select_menu.custom_id("anime_dropdown");
    select_menu.max_values(1);

    // Set the label as    
    select_menu.options(|options| {
        for media in all_media.0 {
            let mut create_option = CreateSelectMenuOption::default();
            create_option.label(&media);
            create_option.value(&media);
            options.add_option(create_option);
        }
        options
    });

    info!("Options: {:?}", options);

    let mut action_row = CreateActionRow::default();
    let act = action_row.add_select_menu(select_menu);

    match msg.channel_id.send_message(&ctx.http, |m| {
            m.components(|c| {
                c.add_action_row(act.to_owned())
            })
    }).await
    {
        Ok(_) => (),
        Err(e) => println!("Error sending message: {:?}", e),
    };

    Ok(())
}


pub struct ComponentHandler;

#[async_trait]
impl EventHandler for ComponentHandler {
    async fn interaction_create(&self, ctx: Context, interaction: Interaction) {
        if let Interaction::MessageComponent(command) = interaction {
            let data = command.data.clone();

            if data.custom_id.as_str() == "anime_dropdown" || data.custom_id.as_str() == "manga_dropdown" {
                command.defer(&ctx.http).await.unwrap();
                let guild_id = command.guild_id.unwrap();
                let db_url = env::var("DB_URL").expect("Expected a DB URL in the environment file");
                let pool = sqlx::postgres::PgPool::connect(&db_url).await.unwrap();
                let shared_pool = Arc::new(pool);
                let db_check = anilist_guild_search(guild_id.into(), shared_pool.clone()).await.unwrap();
                let mut media_type = "ANIME";

                if data.custom_id.as_str() == "manga_dropdown" {
                    media_type = "MANGA";
                }

                let search = search(data.values[0].clone(), media_type.to_string(), db_check).await;

                let mut embed = CreateEmbed::default();
                embed.title(&search.1[0])
                    .url(&search.1[1])
                    .thumbnail(&search.1[2])
                    .image(&search.1[3])
                    .description(search.0.join("\n"));

                match command
                    .edit_original_interaction_response(&ctx.http, |response| {
                        response
                            .add_embed(embed)
                    })
                    .await
                {
                    Ok(_) => (),
                    Err(e) => println!("Error sending message: {:?}", e),
                };
            }
        }
    }
}
