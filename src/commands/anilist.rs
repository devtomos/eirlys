use crate::api::access_db::{anilist_guild_search, anilist_user_search};
use crate::api::search_media::{search, relation_names, user_search};
use serenity::framework::standard::macros::command;
use serenity::framework::standard::{Args, CommandResult};
use serenity::builder::{CreateEmbed, CreateSelectMenuOption, CreateSelectMenuOptions, CreateSelectMenu, CreateActionRow};
use serenity::model::prelude::*;
use serenity::prelude::*;
use serenity::model::gateway::Ready;
use serenity::model::user::OnlineStatus;
use serenity::model::prelude::Activity;
use crate::DatabasePool;
use tracing::info;
use serenity::async_trait;
use serenity::model::application::interaction::Interaction;

// ------------------------------------------------------------------------------------------------------------------------ //

#[command]
pub async fn user(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let mut username = args.message().to_string();
    let data_read = ctx.data.read().await;
    let pool = data_read.get::<DatabasePool>().expect("Expected DatabasePool in TypeMap.");
    let pool = pool.lock().await;

    if username.is_empty() {
        info!("Username Argument is empty, searching in Database.");
        username = anilist_user_search(msg.author.id.into(), (*pool).clone().into()).await.unwrap();
        info!("Username: {}", username);
    } else {
        info!("Username: {}", username);
    }

    let user_search = user_search(username).await;
    
    match msg.channel_id.send_message(&ctx.http, |m| {
        m.embed(|e| {
            e.title(&user_search.1[0])
                .url(&user_search.1[1])
                .thumbnail(&user_search.1[3])
                .image(&user_search.1[2])
                .description(user_search.0.join("\n"))
        })
    }).await
    {
        Ok(_) => (),
        Err(e) => println!("Error sending message: {:?}", e),
    };

    Ok(())
}

// ------------------------------------------------------------------------------------------------------------------------ //

#[command]
pub async fn anime(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let media_name = args.message().to_string();
    info!("Searching for anime with name: {}", media_name);

    let all_media = relation_names(media_name, String::from("ANIME")).await;

    info!("Creating select menu");
    let mut select_menu = CreateSelectMenu::default();
    select_menu.min_values(1);
    select_menu.placeholder("Select an anime");
    select_menu.custom_id("anime_dropdown");
    select_menu.max_values(1);

    info!("Adding options to select menu");
    select_menu.options(|options| {
        for media in all_media.0 {
            let mut create_option = CreateSelectMenuOption::default();
            create_option.label(&media);
            create_option.value(&media);
            options.add_option(create_option);
        }
        options
    });

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
    info!("Message has been sent\n");

    Ok(())
}

// ------------------------------------------------------------------------------------------------------------------------ //

#[command]
pub async fn manga(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let media_name = args.message().to_string();
    info!("Searching for manga with name: {}", media_name);
    
    let all_media = relation_names(media_name, String::from("MANGA")).await;

    info!("Creating select menu");
    let mut select_menu = CreateSelectMenu::default();
    select_menu.min_values(1);
    select_menu.placeholder("Select a manga");
    select_menu.custom_id("manga_dropdown");
    select_menu.max_values(1);

    info!("Adding options to select menu");
    // Set the label as id :: This may not work
    select_menu.options(|options| {
        for media in all_media.0 {
            let mut create_option = CreateSelectMenuOption::default();
            create_option.label(&media);
            create_option.value(&media);
            options.add_option(create_option);
        }
        options
    });

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
    info!("Message has been sent\n");

    Ok(())
}

// ------------------------------------------------------------------------------------------------------------------------ //

pub struct ComponentHandler;
#[async_trait]
impl EventHandler for ComponentHandler {
    async fn ready(&self, ctx: Context, ready: Ready) {
        let activity = Activity::playing("With Rust");
        ctx.set_presence(Some(activity), OnlineStatus::Idle).await;
        info!("{} is connected!", ready.user.name);
    }

    async fn interaction_create(&self, ctx: Context, interaction: Interaction) {
        if let Interaction::MessageComponent(command) = interaction {
            let data = command.data.clone();

            if data.custom_id.as_str() == "anime_dropdown" || data.custom_id.as_str() == "manga_dropdown" {
                info!("Command {:?} was used ", data.custom_id);

                command.defer(&ctx.http).await.unwrap();
                let guild_id = command.guild_id.unwrap();
                let data_read = ctx.data.read().await;
                let pool = data_read.get::<DatabasePool>().expect("Expected DatabasePool in TypeMap.");
                let pool = pool.lock().await;

                info!("Searching for guild with ID: {}", guild_id);

                let db_check = anilist_guild_search(guild_id.into(), (*pool).clone().into()).await.unwrap();
                let mut media_type = "ANIME";

                if data.custom_id.as_str() == "manga_dropdown" {
                    media_type = "MANGA";
                }
                
                info!("Searching for {:?} with name: {}", &media_type, &data.values[0]);
                let search = search(data.values[0].clone(), media_type.to_string(), db_check).await;

                let mut embed = CreateEmbed::default();
                embed.title(&search.1[0])
                    .url(&search.1[1])
                    .thumbnail(&search.1[2])
                    .image(&search.1[3])
                    .description(search.0.join("\n"));

                info!("Created embed");

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
                info!("Message has been edited\n");
            }
        }
    }
}

// ------------------------------------------------------------------------------------------------------------------------ //