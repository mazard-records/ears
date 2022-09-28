from enum import Enum
from typing import List, Optional

from pydantic import AnyHttpUrl, BaseModel


class ElementType(str, Enum):
    button = "button"
    context = "context"
    divider = "divider"
    image = "image"
    markdown = "mrkdown"
    plain_text = "plain_text"
    section = "section"


class Style(str, Enum):
    danger = "danger"
    primary = "primary"


class Block(BaseModel):
    type: ElementType


class Blocks(BaseModel):
    blocks: List[Block]


class Element(object):
    pass


class PlainText(Block):
    type: ElementType = ElementType.plain_text
    emoji: bool = True
    text: str


class Button(Block):
    type: ElementType = ElementType.button
    style: Style = Style.primary
    text: PlainText
    value: str


class Image(Block, Element):
    type: ElementType = ElementType.image
    alt_text: Optional[str] = None
    image_url: AnyHttpUrl


class Markdown(Block, Element):
    type: ElementType = ElementType.markdown
    text: str


class Context(Block):
    type: ElementType = ElementType.context
    elements: List[Element]


class Section(Block):
    type: ElementType = ElementType.section
    text: Markdown
    accessory: Optional[Image] = None


class Actions(Block):
    type: str = "actions"
    elements: List[Button]