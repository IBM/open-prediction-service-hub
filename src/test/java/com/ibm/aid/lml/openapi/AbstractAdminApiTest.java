package com.ibm.aid.lml.openapi;

import org.openapitools.client.ApiClient;
import org.openapitools.client.Configuration;
import org.openapitools.client.api.AdminApi;

public abstract class AbstractAdminApiTest {
    public static final String LOCAL_PROVIDER_PATH = "http://localhost:8080";
    final AdminApi api;

    public AbstractAdminApiTest(){
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath(AbstractAdminApiTest.LOCAL_PROVIDER_PATH);
        this.api = new AdminApi(defaultClient);
    }
}
