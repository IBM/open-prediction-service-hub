/*
 * Copyright 2020 IBM
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * <p>
 * http://www.apache.org/licenses/LICENSE-2.0
 * <p>
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.IBM Confidential
 */

package com.ibm.decision.ops.client;

import com.ibm.decision.ops.client.model.Capabilities;
import com.ibm.decision.ops.client.model.Capability;
import com.ibm.decision.ops.client.model.ServerInfo;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class TestServerInfo {

    MlServiceClient client;

    @Before
    public void init() {
        client = new MlServiceClient();
    }

    /**
     * Test Server Status
     */
    @Test
    public void serverInfoTest() throws ApiException {
        ServerInfo response = client.getInfoApi().getInfo();
        assertEquals(ServerInfo.StatusEnum.OK, response.getStatus());
    }

    /**
     * Test Server Capabilities
     */
    @Test
    public void serverCapabilitiesTest() throws ApiException {
        Capabilities response = client.getInfoApi().getCapabilities();
        assertTrue(response.getCapabilities().contains(Capability.INFO));
        assertTrue(response.getCapabilities().contains(Capability.DISCOVER));
        assertTrue(response.getCapabilities().contains(Capability.RUN));
    }
}
