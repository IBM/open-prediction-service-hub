/*
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

package com.ibm.decision.ops.client;

import com.ibm.decision.ops.client.model.*;
import org.junit.Before;
import org.junit.Test;

import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

public class TestDiscover {
    MlServiceClient client;

    @Before
    public void init() {
        client = new MlServiceClient();
    }

    @Test
    public void getModelsTest() throws ApiException {

        Models response = client.getDiscoverApi().listModels();

        Model loan_approval_rfr = response.getModels().stream().filter(m -> m.getName().equals("[RandomForestRegressor] loan approval example")).findFirst().get();


        assertNotNull(loan_approval_rfr);

        Model loan_approval_rfr_by_id = client.getDiscoverApi().getModelById(loan_approval_rfr.getId());

        assertEquals(loan_approval_rfr, loan_approval_rfr_by_id);

        assertEquals("v1", loan_approval_rfr.getVersion());

        List<Feature> inputSchema = loan_approval_rfr.getInputSchema();

        assertEquals((new Feature().name("creditScore").order(0).type("float")), inputSchema.get(0));
        assertEquals((new Feature().name("income").order(1).type("float")), inputSchema.get(1));
        assertEquals((new Feature().name("loanAmount").order(2).type("float")), inputSchema.get(2));
        assertEquals((new Feature().name("monthDuration").order(3).type("float")), inputSchema.get(3));
        assertEquals((new Feature().name("rate").order(4).type("float")), inputSchema.get(4));

        assertEquals("Evaluation of yearlyReimbursement", loan_approval_rfr.getMetadata().get("description"));
    }

    @Test
    public void getEndpointsTest() throws ApiException {

        Models models = client.getDiscoverApi().listModels();

        Model model = models.getModels().stream().filter(m -> m.getName().equals("[RandomForestRegressor] loan approval example")).findFirst().get();

        assertNotNull(model);

        Endpoints endpoints = client.getDiscoverApi().listEndpoints(model.getId());

        assertNotNull(endpoints);

        assertEquals(1, endpoints.getEndpoints().size());

        Endpoint endpoint = endpoints.getEndpoints().get(0);

        assertNotNull(endpoint);

        final String model_endpoint_href = model.getLinks().stream().filter(link -> link.getRel().equals("endpoint")).findFirst().get().getHref();
        final String model_self_href = model.getLinks().stream().filter(link -> link.getRel().equals("self")).findFirst().get().getHref();

        final String endpoint_model_href = endpoint.getLinks().stream().filter(link -> link.getRel().equals("model")).findFirst().get().getHref();
        final String endpoint_self_href = endpoint.getLinks().stream().filter(link -> link.getRel().equals("self")).findFirst().get().getHref();

        assertEquals(model_endpoint_href, endpoint_self_href);
        assertEquals(model_self_href, endpoint_model_href);
    }
}
