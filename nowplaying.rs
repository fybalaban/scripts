use std::process::Command;

fn main() {
    let output0 = Command::new("/usr/bin/playerctl")
                     .arg("status")
                     .output()
                     .expect("err: call playerctl status");


    let status = String::from_utf8_lossy(&output0.stdout);

    if status == "Playing\n" {
        let output1 = Command::new("/usr/bin/playerctl")
                              .arg("-f")
                              .arg("'{{trunc(xesam:artist, 15)}} - {{trunc(xesam:title,     30)}}'")
                              .arg("metadata")
                              .output()
                              .expect("err: call playerctl metadata");
        let music = &String::from_utf8(output1.stdout).unwrap();
        println!("{}", &music[1..music.len() - 2]);
    } else if status == "Paused\n" {
        println!("Paused\n");
    } else {
        println!("");
    }
}
