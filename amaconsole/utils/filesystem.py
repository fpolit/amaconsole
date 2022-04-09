#!/usr/bin/env python3

from __future__ import annotations

#import os
from typing import Union
from abc import ABC, abstractmethod
from pathlib import Path

class Node(ABC):
    def __init__(self, name: str, parent: Node = None, children: List[Node] = None):
        self.name = name
        self.parent = parent
        self.children = children

        self.path = Path(name)
        if parent:
            parent.add_child(self)
            self.path = parent.path.joinpath(name)

    def add_child(self, node: Union[str, Node]):
        if isinstance(node, Node):
            node.parent = self
        else:
            name = node
            node = Node(name, parent=self)

        self.children.append(node)

    @abstractmethod
    def create(self):
        pass

class FileNode(Node):
    def __init__(self, name: str, parent: Node = None):
        super().__init__(name, parent)

    def create(self):
        self.path.touch(exist_ok=True)


class DirNode(Node):
    def __init__(self, name: str, parent: Node = None, children: List[Node] = None):
        children = children if children else []
        super().__init__(name, parent, children)

    def create(self):
        self.path.mkdir(exist_ok=True)

        for child in self.children:
            child.create()

    def add_file(self, filename: str) -> FileNode:
        filenode = FileNode(name=filename, parent=self)
        return filenode

    def add_subdir(self, sdir: str) -> DirNode:
        dirnode = DirNode(name=sdir, parent=self)
        return dirnode


class FileSystem:
    def __init__(self, root: Path,
                 subdirs: List[str] = None,
                 files: List[str] = None):
        if root.is_file():
            raise Exception(f"root {root} is a file")

        self.root_node = DirNode(name=root)

        subdirs = subdirs if subdirs else []
        files = files if files else []

        for sdir in subdirs:
            DirNode(name=sdir, parent=self)

        for filename in files:
            FileNode(name=filename, parent=self)

    @property
    def path(self) -> Path:
        return self.root_node.path

    def add_node(self, node: Union[FileNode, DirNode]):
        self.add_child(node)

    def add_file(self, filename: str) -> FileNode:
        filenode = self.root_node.add_file(filename)
        return filenode

    def add_subdir(self, sdir: str) -> DirNode:
        dirnode = self.root_node.add_subdir(sdir)
        return dirnode

    def create(self):
        self.root_node.create()
