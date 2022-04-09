#!/usr/bin/env python3

import os
import uuid
import tempfile

from unittest import TestCase
from datetime import timedelta
from amaconsole.utils import (
    FileSystem,
    FileNode,
    DirNode
)

class TestUtilsFilesystem(TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp() # base directory
        self.tmpdirnode = DirNode(self.tmpdir)

    def test_filenode_creation_without_parent(self):
        filename = uuid.uuid4().hex
        filepath = os.path.join(self.tmpdir, filename)
        filenode = FileNode(filepath)

        self.assertFalse(os.path.isfile(filepath))
        filenode.create()
        self.assertTrue(os.path.isfile(filepath))

    def test_filenode_creation_with_parent(self):
        filename = uuid.uuid4().hex
        filenode = FileNode(name=filename, parent=self.tmpdirnode)

        filepath = os.path.join(str(self.tmpdirnode.path), filename)

        self.assertFalse(os.path.isfile(filepath))
        filenode.create()
        self.assertTrue(os.path.isfile(filepath))

    def test_dirnode_creation_without_parent(self):
        dirname = uuid.uuid4().hex
        dirpath = os.path.join(self.tmpdir, dirname)
        dirnode = DirNode(dirpath)

        self.assertFalse(os.path.isdir(dirpath))
        dirnode.create()
        self.assertTrue(os.path.isdir(dirpath))

    def test_dirnode_creation_with_parent(self):
        dirname = uuid.uuid4().hex
        dirnode = DirNode(name=dirname, parent=self.tmpdirnode)
        dirpath = os.path.join(str(self.tmpdirnode.path), dirname)

        self.assertFalse(os.path.isdir(dirpath))
        dirnode.create()
        self.assertTrue(os.path.isdir(dirpath))

    def test_filesystem_creation(self):
        # root
        # |- file
        # |- dir
        #   |- subfile

        rootdirname = uuid.uuid4().hex
        rootdirpath = self.tmpdirnode.path.joinpath(rootdirname)

        fs = FileSystem(root=rootdirpath)

        filename = uuid.uuid4().hex
        filenode = fs.add_file(filename)

        dirname = uuid.uuid4().hex
        dirnode = fs.add_subdir(dirname)

        subfilename = uuid.uuid4().hex
        subfilenode = dirnode.add_file(subfilename)

        self.assertFalse(os.path.isdir(str(fs.path)))
        self.assertFalse(os.path.isfile(str(filenode.path)))
        self.assertFalse(os.path.isdir(str(dirnode.path)))
        self.assertFalse(os.path.isfile(str(subfilenode.path)))

        fs.create()

        self.assertTrue(os.path.isdir(str(fs.path)))
        self.assertTrue(os.path.isfile(str(filenode.path)))
        self.assertTrue(os.path.isdir(str(dirnode.path)))
        self.assertTrue(os.path.isfile(str(subfilenode.path)))
