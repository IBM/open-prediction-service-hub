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
import com.ibm.decision.ops.client.model.Feature;
import com.ibm.decision.ops.client.model.MLSchema;

import java.io.File;
import java.util.List;
import java.util.Objects;

public class TestGetModels extends AbstractAdminApiTest{

    @Before
    public void init() throws ApiException {
        for (MLSchema m : api.getModelsModelsGet()) {
            api.removeModelModelsDelete(m.getName(), m.getVersion());
        }
        Assert.assertEquals(0, (long) api.getServerStatusStatusGet().getModelCount());

        api.addModelModelsPost(
                new File(Objects.requireNonNull(getClass().getClassLoader().getResource( "miniloan-rfc.zip")).getFile()));

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
     * Get Models
     *
     * Returns the list of ML models.
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void getModelTest() throws ApiException {

        List<MLSchema> response = api.getModelsModelsGet();

        MLSchema miniloanRfc = response.get(0);

        Assert.assertEquals("miniloan-rfc", miniloanRfc.getName());
        Assert.assertEquals("v0", miniloanRfc.getVersion());
        Assert.assertEquals("predict_proba", miniloanRfc.getMethodName());

        List<Feature> inputSchema = miniloanRfc.getInputSchema();

        Assert.assertEquals((new Feature().name("creditScore").order(0).type("int64")), inputSchema.get(0));
        Assert.assertEquals((new Feature().name("income").order(1).type("float32")), inputSchema.get(1));
        Assert.assertEquals((new Feature().name("loanAmount").order(2).type("float64")), inputSchema.get(2));
        Assert.assertEquals((new Feature().name("monthDuration").order(3).type("float64")), inputSchema.get(3));
        Assert.assertEquals((new Feature().name("rate").order(4).type("float64")), inputSchema.get(4));

        Assert.assertEquals("Loan approval", miniloanRfc.getMetadata().getDescription());
        Assert.assertEquals("ke", miniloanRfc.getMetadata().getAuthor());
        Assert.assertEquals("accuracy", miniloanRfc.getMetadata().getMetrics().get(0).getName());
    }
}
