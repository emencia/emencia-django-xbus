# -*- coding: UTF-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Import from the Standard Library
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='emencia-django-xbus',
    version='0.1',
    packages=['xbus'],
    license='GPLv3+',
    install_requires=['msgpack-python', 'zmq_rpc', 'django-extensions'],
)
