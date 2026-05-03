// solution-03.rs - 高级模式匹配：状态机和错误处理

fn main() {
    // 高级练习：实现一个文件处理器状态机
    #[derive(Debug, Clone)]
    enum FileProcessorState {
        Idle,
        Reading { filename: String, bytes_read: usize },
        Processing { data: Vec<u8>, progress: f32 },
        Writing { filename: String, bytes_written: usize },
        Completed { result: String },
        Error { message: String, retry_count: u32 },
    }

    impl FileProcessorState {
        fn next_state(self) -> Self {
            match self {
                FileProcessorState::Idle => {
                    println!("准备读取文件");
                    FileProcessorState::Reading {
                        filename: "data.txt".to_string(),
                        bytes_read: 0,
                    }
                }
                FileProcessorState::Reading { filename, bytes_read } => {
                    if bytes_read < 1000 {
                        println!("读取文件 {}: {} bytes", filename, bytes_read);
                        FileProcessorState::Reading {
                            filename,
                            bytes_read: bytes_read + 250,
                        }
                    } else {
                        println!("完成读取文件 {}", filename);
                        FileProcessorState::Processing {
                            data: vec![1; 1000], // 模拟数据
                            progress: 0.0,
                        }
                    }
                }
                FileProcessorState::Processing { data, progress } => {
                    if progress < 1.0 {
                        let new_progress = progress + 0.25;
                        println!("处理数据: {:.0}%", new_progress * 100.0);
                        FileProcessorState::Processing { data, progress: new_progress }
                    } else {
                        println!("处理完成");
                        FileProcessorState::Writing {
                            filename: "output.txt".to_string(),
                            bytes_written: 0,
                        }
                    }
                }
                FileProcessorState::Writing { filename, bytes_written } => {
                    if bytes_written < 500 {
                        println!("写入文件 {}: {} bytes", filename, bytes_written);
                        FileProcessorState::Writing {
                            filename,
                            bytes_written: bytes_written + 125,
                        }
                    } else {
                        println!("写入完成");
                        FileProcessorState::Completed {
                            result: "File processed successfully".to_string(),
                        }
                    }
                }
                FileProcessorState::Completed { result } => {
                    println!("最终结果: {}", result);
                    FileProcessorState::Idle
                }
                FileProcessorState::Error { message, retry_count } => {
                    if retry_count < 3 {
                        println!("重试错误 (尝试 {}): {}", retry_count + 1, message);
                        FileProcessorState::Error {
                            message,
                            retry_count: retry_count + 1,
                        }
                    } else {
                        println!("放弃重试: {}", message);
                        FileProcessorState::Completed {
                            result: "Failed after retries".to_string(),
                        }
                    }
                }
            }
        }
    }

    // 模拟运行状态机
    let mut current_state = FileProcessorState::Idle;
    for step in 0..15 {
        println!("\n--- 步骤 {} ---", step);
        current_state = current_state.next_state();
        if matches!(current_state, FileProcessorState::Idle) && step > 0 {
            break;
        }
    }

    // 错误处理示例
    use std::io::{self, Read};
    use std::fs::File;

    fn safe_file_operation(filename: &str) -> Result<String, Box<dyn std::error::Error>> {
        let mut file = File::open(filename)?;
        let mut contents = String::new();
        file.read_to_string(&mut contents)?;
        Ok(contents)
    }

    fn handle_file_result(filename: &str) {
        match safe_file_operation(filename) {
            Ok(contents) => {
                println!("文件 '{}' 读取成功，长度: {}", filename, contents.len());
                // 进一步处理内容
                match contents.trim().parse::<i32>() {
                    Ok(number) => println!("解析为数字: {}", number),
                    Err(_) => println!("内容不是有效数字"),
                }
            }
            Err(error) => {
                // 使用模式匹配处理不同类型的错误
                if let Some(io_error) = error.downcast_ref::<io::Error>() {
                    match io_error.kind() {
                        io::ErrorKind::NotFound => println!("文件未找到: {}", filename),
                        io::ErrorKind::PermissionDenied => println!("权限不足: {}", filename),
                        _ => println!("IO错误: {:?}", io_error),
                    }
                } else {
                    println!("其他错误: {}", error);
                }
            }
        }
    }

    println!("\n=== 错误处理测试 ===");
    handle_file_result("nonexistent.txt");
    handle_file_result("existing_but_invalid.txt"); // 假设存在但内容无效
}