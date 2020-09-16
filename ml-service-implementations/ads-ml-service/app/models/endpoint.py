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


import sqlalchemy as sa
import sqlalchemy.orm as orm

import app.db.base_class as base_class


class Endpoint(base_class.Base):
    name = sa.Column('name', sa.NCHAR(length=128), nullable=False)
    deployed_at = sa.Column('deployed_at', sa.DateTime(timezone=True), nullable=False)

    model_id = sa.Column('model_id', sa.Integer, sa.ForeignKey('model.id'))
    model = orm.relationship('Model', back_populates='endpoint', uselist=False)

    binary = orm.relationship('BinaryMlModel', back_populates='endpoint', cascade='all, delete', uselist=False)
