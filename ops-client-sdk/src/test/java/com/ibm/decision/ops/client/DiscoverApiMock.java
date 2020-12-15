/*
 * IBM Confidential
 * OCO Source Materials
 * 5737-I23
 * Copyright IBM Corp. 2020
 * The source code for this program is not published or otherwise
 * divested of its trade secrets, irrespective of what has
 * been deposited with the U.S Copyright Office.
 */

package com.ibm.decision.ops.client;

import com.ibm.decision.ops.client.api.DiscoverApi;
import com.ibm.decision.ops.client.model.Endpoint;
import com.ibm.decision.ops.client.model.Endpoints;
import com.ibm.decision.ops.client.model.Model;
import com.ibm.decision.ops.client.model.Models;

import java.util.Collections;
import java.util.List;

public class DiscoverApiMock extends DiscoverApi {

    @Override
    public Models listModels() throws ApiException {

        List<Model> modelList = MockResources.getResourceList("model.json", Model.class);
        Models models = new Models();
        modelList.forEach(models::addModelsItem);
        return models;
    }

    @Override
    public Model getModelById(String modelId) throws ApiException {
        return MockResources.getResourceList("model.json", Model.class).stream()
                .filter(endpoint -> endpoint.getId().equals(modelId))
                .findFirst()
                .orElse(null);
    }

    @Override
    public Endpoints listEndpoints(String modelId) throws ApiException {
        List<Endpoint> endpointList = MockResources.getResourceList("endpoint.json", Endpoint.class);

        Endpoints endpoints = new Endpoints();

        Endpoint endpoint = endpointList.stream()
                .filter(e -> e.getId().equals(modelId))
                .findFirst().orElse(null);

        if (endpoint == null)
            endpoints.setEndpoints(endpointList);
        else
            endpoints.setEndpoints(Collections.singletonList(endpoint));

        return endpoints;
    }

    @Override
    public Endpoint getEndpointById(String endpointId) throws ApiException {
        return MockResources.getResourceList("endpoint.json", Endpoint.class).stream()
                .filter(endpoint -> endpoint.getId().equals(endpointId))
                .findFirst()
                .orElse(null);
    }
}
