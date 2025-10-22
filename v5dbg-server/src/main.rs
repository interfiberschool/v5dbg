use std::time::Duration;

use tokio::{io::{stdin, stdout, AsyncReadExt, AsyncWriteExt}, select, time::sleep};
use vex_v5_serial::{
    Connection,
    serial::{self, SerialError},
};

#[tokio::main]
async fn main() -> Result<(), SerialError> {
    let devices = serial::find_devices()?;

    if devices.len() == 0 {
        panic!("No connected serial devices found!");
    }

    let mut connection = devices[0].connect(Duration::from_secs(10))?;

    let mut stdin = stdin();

    loop {
        let mut program_output = [0; 1024];
        let mut program_input = [0; 1024];
        select! {
            read = connection.read_user(&mut program_output) => {
                if let Ok(size) = read {
                    stdout().write_all(&program_output[..size]).await.unwrap();
                }
            },
            read = stdin.read(&mut program_input) => {
                if let Ok(size) = read {
                    connection.write_user(&program_input[..size]).await.unwrap();
                }
            }
        }

        sleep(Duration::from_millis(10)).await;
    }
}
