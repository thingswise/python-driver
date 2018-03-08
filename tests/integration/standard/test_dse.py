# Copyright DataStax, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    import unittest2 as unittest
except ImportError:
    import unittest  # noqa

from tests.integration import is_dse, use_cluster, CLUSTER_NAME, dseonly
from cassandra.cluster import Cluster


@dseonly
class DseCCMClusterTest(unittest.TestCase):
    """
    This class can be executed setting the DSE_VERSION variable, for example:
    DSE_VERSION=5.1.4 python2.7 -m nose tests/integration/standard/test_dse.py --nocapture
    """
    @classmethod
    def setUpClass(cls):
        if not is_dse():
            return
        use_cluster(CLUSTER_NAME, [3], dse_cluster=True, dse_options={})

    def test_connect(self):
        """
        Test to ensure that the driver can connect to DSE and execute queries

        @since 3.14
        @jira_ticket PYTHON-894
        @expected_result results are fetched

        @test_category connection
        """
        cluster = Cluster()
        session = cluster.connect()
        result = session.execute("SELECT * from system.local")
        self.assertIsNotNone(result)

    @classmethod
    def tearDownClass(cls):
        if not is_dse():
            return
