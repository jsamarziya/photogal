# Copyright (C) 2018 The Photogal Team.
#
# This file is part of Photogal.
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

from flask import Flask

app = Flask('photogal', instance_relative_config=True)
app.logger.debug("Instance path is %s", app.instance_path)
app.config.from_object('photogal.config')
app.config.from_pyfile('photogal.cfg', silent=True)
app.config.from_envvar('PHOTOGAL_CONFIG', silent=True)
app.logger.debug("Configuration is %s", app.config)

from photogal.database import db

db.create_all()

app.logger.info("photogal started")