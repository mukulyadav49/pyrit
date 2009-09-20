#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    Copyright 2008, 2009, Lukas Lueg, lukas.lueg@gmail.com
#
#    This file is part of Pyrit.
#
#    Pyrit is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Pyrit is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Pyrit.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup, Extension
from distutils.unixccompiler import UnixCCompiler
import subprocess
import re

UnixCCompiler.src_extensions.append('.S')

try:
    svn_info = subprocess.Popen(('svn', 'info'), \
                                stdout=subprocess.PIPE).stdout.read()
    version_string = '0.2.5-dev (svn r%i)' % \
                    int(re.compile('Revision: ([0-9]*)').findall(svn_info)[0])
except:
    version_string = '0.2.5-dev'
EXTRA_COMPILE_ARGS = ['-DVERSION="%s"' % version_string]


cpu_extension = Extension(name='cpyrit._cpyrit_cpu',
                    sources = ['cpyrit/_cpyrit_cpu.c',
                               'cpyrit/_cpyrit_cpu_sse2.S'],
                    libraries = ['ssl'],
                    extra_compile_args=EXTRA_COMPILE_ARGS)

setup_args = dict(
        name = 'Pyrit',
        version = '0.2.5',
        description = 'GPU-accelerated attack against WPA-PSK authentication',
        license = 'GNU General Public License v3',
        author = 'Lukas Lueg',
        author_email = 'lukas.lueg@gmail.com',
        url = 'http://pyrit.googlecode.com',
        packages = ['cpyrit'],
        py_modules = ['pyrit_cli', 'cpyrit.cpyrit',
                      'cpyrit.util', 'cpyrit.pckttools'],
        scripts = ['pyrit'],
        ext_modules = [cpu_extension],
        options = {'install': {'optimize': 1}})

if __name__ == '__main__':
    setup(**setup_args)
