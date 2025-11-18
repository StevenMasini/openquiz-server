"""
Item ABC and concrete implementations for quiz content
Each Item can render itself to HTML
"""

from abc import ABC, abstractmethod
from html import escape
from typing import Dict, Any


class Item(ABC):
    """Base interface for all renderable quiz items"""

    @abstractmethod
    def render(self) -> str:
        """Render this item as HTML"""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization/storage"""
        pass


class TextItem(Item):
    """Simple text content item"""

    def __init__(self, content: str, css_class: str = ""):
        """
        Args:
            content: The text content to display
            css_class: Optional CSS class for styling
        """
        self.content = content
        self.css_class = css_class

    def render(self) -> str:
        """Render as HTML paragraph"""
        # Escape HTML to prevent injection
        safe_content = escape(self.content)
        class_attr = f' class="{escape(self.css_class)}"' if self.css_class else ''
        return f'<p{class_attr}>{safe_content}</p>'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'text',
            'content': self.content,
            'css_class': self.css_class
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TextItem':
        """Create TextItem from dictionary"""
        return cls(
            content=data['content'],
            css_class=data.get('css_class', '')
        )


class ImageItem(Item):
    """Image content item"""

    def __init__(self, url: str, alt: str = "", css_class: str = "", width: str = "", height: str = ""):
        """
        Args:
            url: Image URL
            alt: Alt text for accessibility
            css_class: Optional CSS class for styling
            width: Optional width attribute (e.g., "300px", "100%")
            height: Optional height attribute
        """
        self.url = url
        self.alt = alt
        self.css_class = css_class
        self.width = width
        self.height = height

    def render(self) -> str:
        """Render as HTML img tag"""
        safe_url = escape(self.url)
        safe_alt = escape(self.alt)

        attrs = []
        if self.css_class:
            attrs.append(f'class="{escape(self.css_class)}"')
        if self.width:
            attrs.append(f'width="{escape(self.width)}"')
        if self.height:
            attrs.append(f'height="{escape(self.height)}"')

        attrs_str = ' ' + ' '.join(attrs) if attrs else ''
        return f'<img src="{safe_url}" alt="{safe_alt}"{attrs_str} />'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'image',
            'url': self.url,
            'alt': self.alt,
            'css_class': self.css_class,
            'width': self.width,
            'height': self.height
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ImageItem':
        """Create ImageItem from dictionary"""
        return cls(
            url=data['url'],
            alt=data.get('alt', ''),
            css_class=data.get('css_class', ''),
            width=data.get('width', ''),
            height=data.get('height', '')
        )


class VideoItem(Item):
    """Video content item with optional controls"""

    def __init__(self, url: str, thumbnail: str = "", css_class: str = "", autoplay: bool = False, controls: bool = True):
        """
        Args:
            url: Video URL
            thumbnail: Optional thumbnail/poster image URL
            css_class: Optional CSS class for styling
            autoplay: Whether video should autoplay
            controls: Whether to show video controls
        """
        self.url = url
        self.thumbnail = thumbnail
        self.css_class = css_class
        self.autoplay = autoplay
        self.controls = controls

    def render(self) -> str:
        """Render as HTML video tag"""
        safe_url = escape(self.url)

        attrs = []
        if self.css_class:
            attrs.append(f'class="{escape(self.css_class)}"')
        if self.thumbnail:
            attrs.append(f'poster="{escape(self.thumbnail)}"')
        if self.controls:
            attrs.append('controls')
        if self.autoplay:
            attrs.append('autoplay')

        attrs_str = ' ' + ' '.join(attrs) if attrs else ''
        return f'<video{attrs_str}><source src="{safe_url}" type="video/mp4" />Your browser does not support the video tag.</video>'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'video',
            'url': self.url,
            'thumbnail': self.thumbnail,
            'css_class': self.css_class,
            'autoplay': self.autoplay,
            'controls': self.controls
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VideoItem':
        """Create VideoItem from dictionary"""
        return cls(
            url=data['url'],
            thumbnail=data.get('thumbnail', ''),
            css_class=data.get('css_class', ''),
            autoplay=data.get('autoplay', False),
            controls=data.get('controls', True)
        )


class AudioItem(Item):
    """Audio content item"""

    def __init__(self, url: str, css_class: str = "", autoplay: bool = False, controls: bool = True):
        """
        Args:
            url: Audio URL
            css_class: Optional CSS class for styling
            autoplay: Whether audio should autoplay
            controls: Whether to show audio controls
        """
        self.url = url
        self.css_class = css_class
        self.autoplay = autoplay
        self.controls = controls

    def render(self) -> str:
        """Render as HTML audio tag"""
        safe_url = escape(self.url)

        attrs = []
        if self.css_class:
            attrs.append(f'class="{escape(self.css_class)}"')
        if self.controls:
            attrs.append('controls')
        if self.autoplay:
            attrs.append('autoplay')

        attrs_str = ' ' + ' '.join(attrs) if attrs else ''
        return f'<audio{attrs_str}><source src="{safe_url}" type="audio/mpeg" />Your browser does not support the audio tag.</audio>'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'audio',
            'url': self.url,
            'css_class': self.css_class,
            'autoplay': self.autoplay,
            'controls': self.controls
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AudioItem':
        """Create AudioItem from dictionary"""
        return cls(
            url=data['url'],
            css_class=data.get('css_class', ''),
            autoplay=data.get('autoplay', False),
            controls=data.get('controls', True)
        )


# Factory function to create items from dictionaries
def item_from_dict(data: Dict[str, Any]) -> Item:
    """Factory function to create appropriate Item from dictionary"""
    item_type = data.get('type')

    if item_type == 'text':
        return TextItem.from_dict(data)
    elif item_type == 'image':
        return ImageItem.from_dict(data)
    elif item_type == 'video':
        return VideoItem.from_dict(data)
    elif item_type == 'audio':
        return AudioItem.from_dict(data)
    else:
        raise ValueError(f"Unknown item type: {item_type}")
