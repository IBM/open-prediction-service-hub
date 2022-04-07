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

import com.ibm.decision.ops.client.api.RunApi;
import com.ibm.decision.ops.client.model.Link;
import com.ibm.decision.ops.client.model.Prediction;
import com.ibm.decision.ops.client.model.PredictionResponse;

public class RunApiMock extends RunApi {
    @Override
    public PredictionResponse prediction(Prediction prediction) throws ApiException {
        Link link = prediction.getTarget().stream().filter(l -> l.getRel().equals("endpoint")).findFirst().get();

        String endpointId = link.getHref().substring(link.getHref().lastIndexOf("/") + 1);

        return MockResources.getResourceModel(endpointId, "prediction.json", PredictionResponse.class);
    }
}
