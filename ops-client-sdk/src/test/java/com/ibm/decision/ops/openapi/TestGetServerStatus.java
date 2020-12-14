/**
 * Copyright 2020 IBM
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.IBM Confidential
 */
package com.ibm.decision.ops.openapi;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import com.ibm.decision.ops.client.ApiException;
import com.ibm.decision.ops.client.model.MLSchema;
import com.ibm.decision.ops.client.model.ServerStatus;

import java.io.File;
import java.util.Objects;

public class TestGetServerStatus extends AbstractAdminApiTest {

    @Before
    public void init() throws ApiException {
        for (MLSchema m : api.getModelsModelsGet()) {
            api.removeModelModelsDelete(m.getName(), m.getVersion());
        }
        Assert.assertEquals(0, (long) api.getServerStatusStatusGet().getModelCount());

        api.addModelModelsPost(
                new File(Objects.requireNonNull(getClass().getClassLoader().getResource("miniloan-rfc.zip")).getFile()));

        Assert.assertEquals(1, (long) api.getServerStatusStatusGet().getModelCount());
    }

    @After
    public void reInit() throws ApiException {
        for (MLSchema m : api.getModelsModelsGet()) {
            api.removeModelModelsDelete(m.getName(), m.getVersion());
        }
        Assert.assertEquals(0, (long) api.getServerStatusStatusGet().getModelCount());
    }

    /**
     * Get Server Status
     *
     * @throws ApiException if the Api call fails
     */
    @Test
    public void getServerStatusTest() throws ApiException {

        ServerStatus response = api.getServerStatusStatusGet();
        Assert.assertEquals(1, (long) response.getModelCount());
    }
}
