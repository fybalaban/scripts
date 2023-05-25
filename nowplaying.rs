/*
 *      Ferit Yiğit BALABAN,    <fybalaban@fybx.dev>
 *      nowplaying.rs           2023
 */

use std::process::Command;

fn main() {
    let output0 = Command::new("playerctl")
                     .arg("status")
                     .output()
                     .expect("err: call playerctl status");

    let status = String::from_utf8_lossy(&output0.stdout);

    match status.trim() {
        "Playing" => {
            let output1 = Command::new("playerctl")
                              .arg("-f")
                              .arg("{{trunc(xesam:artist, 15)}} - {{trunc(xesam:title, 30)}}")
                              .arg("metadata")
                              .output()
                              .expect("err: call playerctl metadata");
            let music = String::from_utf8(output1.stdout).unwrap();
            let music = music.replace("&", "&amp;");
            println!("{}", music);
        }
        "Paused" => {
            println!("Paused");
        }
        _ => {
            println!("");
        }
    }
}
