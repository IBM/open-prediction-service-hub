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
