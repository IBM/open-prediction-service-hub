# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.IBM Confidential
#


import sqlalchemy as sql
import sqlalchemy.orm as sql_orm

import app.db.base_class as base_class


class Endpoint(base_class.Base):
    id = sql.Column('id', sql.Integer, sql.ForeignKey('model.id'),
                    nullable=False, unique=True, index=True, primary_key=True)
    name = sql.Column('name', sql.NCHAR(length=128), nullable=False)
    deployed_at = sql.Column('deployed_at', sql.DateTime(timezone=True), nullable=False)

    model = sql_orm.relationship('Model', back_populates='endpoint', uselist=False)
    binary = sql_orm.relationship('BinaryMlModel', back_populates='endpoint', cascade='all, delete', uselist=False)
