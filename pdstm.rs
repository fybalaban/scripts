//
//      yigid balaban <fyb@fybx.dev>            2024
//      please don't stop the music
//
//      description
//      this fella won't let the music stop! depends on playerctl
//      rustc pdstm.rs
//      use bash: while true; ./pdstm; sleep 1; done

use std::process::Command;

macro_rules! noop {
    () => ();
}

fn main() {
    let output = Command::new("playerctl")
                     .arg("status")
                     .output()
                     .expect("err: call playerctl status");

    let status = String::from_utf8_lossy(&output.stdout);

    match status.trim() {
        "Paused" => {
            let _ = Command::new("playerctl")
                .arg("play")
                .output();
        }
        _ => {
            noop!();
        }
    }
}
