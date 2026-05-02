"""
练习3解答：适配器模式实现

适配器模式是一种结构型设计模式，它允许不兼容的接口协同工作。
适配器充当两个不兼容接口之间的桥梁。
"""


from abc import ABC, abstractmethod


# 目标接口（我们需要的接口）
class MediaPlayer(ABC):
    """媒体播放器接口"""

    @abstractmethod
    def play(self, audio_type: str, filename: str):
        pass


# 被适配的类（现有的接口）
class AdvancedMediaPlayer(ABC):
    """高级媒体播放器接口"""

    @abstractmethod
    def play_vlc(self, filename: str):
        pass

    @abstractmethod
    def play_mp4(self, filename: str):
        pass


class VlcPlayer(AdvancedMediaPlayer):
    """VLC播放器实现"""

    def play_vlc(self, filename: str):
        print(f"Playing VLC file: {filename}")

    def play_mp4(self, filename: str):
        # VLC播放器不支持MP4
        pass


class Mp4Player(AdvancedMediaPlayer):
    """MP4播放器实现"""

    def play_vlc(self, filename: str):
        # MP4播放器不支持VLC
        pass

    def play_mp4(self, filename: str):
        print(f"Playing MP4 file: {filename}")


# 适配器类
class MediaAdapter(MediaPlayer):
    """媒体适配器"""

    def __init__(self, audio_type: str):
        self.advanced_media_player = None

        if audio_type.lower() == "vlc":
            self.advanced_media_player = VlcPlayer()
        elif audio_type.lower() == "mp4":
            self.advanced_media_player = Mp4Player()

    def play(self, audio_type: str, filename: str):
        if audio_type.lower() == "vlc":
            self.advanced_media_player.play_vlc(filename)
        elif audio_type.lower() == "mp4":
            self.advanced_media_player.play_mp4(filename)


# 具体的媒体播放器
class AudioPlayer(MediaPlayer):
    """音频播放器（使用适配器）"""

    def play(self, audio_type: str, filename: str):
        # 内置支持MP3播放
        if audio_type.lower() == "mp3":
            print(f"Playing MP3 file: {filename}")
        # 使用适配器处理其他格式
        elif audio_type.lower() in ["vlc", "mp4"]:
            adapter = MediaAdapter(audio_type)
            adapter.play(audio_type, filename)
        else:
            print(f"不支持的音频格式: {audio_type}")


# 测试代码
if __name__ == "__main__":
    audio_player = AudioPlayer()

    # 测试不同格式
    audio_player.play("mp3", "beyond_the_horizon.mp3")
    audio_player.play("mp4", "alone.mp4")
    audio_player.play("vlc", "far_far_away.vlc")
    audio_player.play("avi", "mind_me.avi")  # 不支持的格式