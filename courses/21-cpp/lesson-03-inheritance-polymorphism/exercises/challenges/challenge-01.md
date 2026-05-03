# 挑战 1：设计一个媒体播放器系统

## 背景
你正在开发一个多媒体播放器应用程序，需要支持多种不同类型的媒体文件（音频、视频、图像等）。每种媒体类型有不同的播放行为和元数据。

## 任务要求

### 1. 设计抽象基类 `MediaFile`
- 包含纯虚函数：
  - `play()` - 播放媒体
  - `getDuration()` - 获取媒体时长（秒）
  - `getFormat()` - 获取媒体格式
  - `displayInfo()` - 显示媒体信息
- 包含受保护的成员变量：
  - `filename` (std::string)
  - `fileSize` (size_t)

### 2. 实现具体的媒体类
创建以下派生类：

**AudioFile 类**
- 额外属性：`bitrate` (int), `sampleRate` (int)
- 支持格式：MP3, WAV, FLAC
- `play()` 方法应输出："Playing audio [filename] at [bitrate] kbps"

**VideoFile 类**
- 额外属性：`resolution` (std::string), `frameRate` (double)
- 支持格式：MP4, AVI, MOV
- `play()` 方法应输出："Playing video [filename] at [resolution] resolution"

**ImageFile 类**
- 额外属性：`width` (int), `height` (int), `colorDepth` (int)
- 支持格式：JPG, PNG, GIF
- 注意：图像文件的 `play()` 方法应该显示而不是播放
- `play()` 方法应输出："Displaying image [filename] ([width]x[height])"

### 3. 实现多态容器
创建一个 `MediaPlayer` 类，包含：
- `std::vector<std::unique_ptr<MediaFile>> playlist`
- `void addMedia(std::unique_ptr<MediaFile> media)`
- `void playAll()` - 播放播放列表中的所有媒体
- `double getTotalDuration()` - 返回播放列表总时长

### 4. 测试你的实现
在 `main()` 函数中：
- 创建不同类型的媒体文件对象
- 将它们添加到播放器中
- 调用 `playAll()` 和 `getTotalDuration()`
- 确保内存正确管理（使用智能指针）

## 额外挑战（可选）
- 添加 `pause()` 和 `stop()` 虚函数
- 实现媒体文件的元数据解析（从文件名推断格式和基本信息）
- 添加错误处理（无效文件格式等）

## 提交要求
- 所有代码放在一个 `.cpp` 文件中
- 使用适当的访问控制（public/protected/private）
- 确保有 virtual 析构函数
- 使用 `override` 关键字
- 包含必要的头文件