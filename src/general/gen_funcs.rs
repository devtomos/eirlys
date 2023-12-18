pub fn get_sens(key: &str) -> Option<f64> {
    match key {
        "VALORANT" => Some(0.07),
        "CS2" => Some(0.022),
        "APEX" => Some(0.022),
        "FORTNITE" => Some(0.005555),
        "OVERWATCH" => Some(0.0066),
        "RUST" => Some(0.1125),
        "DESTINY" => Some(0.022),
        _ => None,
    }
}
