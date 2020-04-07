package com.ibm.aid.lml.openapi;

import org.openapitools.client.ApiClient;
import org.openapitools.client.Configuration;
import org.openapitools.client.api.AdminApi;
import org.openapitools.client.api.MlApi;

public class AbstractMLApiTest {
    public static final String LOCAL_PROVIDER_PATH = "http://localhost:8080";
    final MlApi mlApi;
    final AdminApi adminApi;

    public AbstractMLApiTest(){
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath(AbstractMLApiTest.LOCAL_PROVIDER_PATH);
        this.mlApi = new MlApi(defaultClient);
        this.adminApi = new AdminApi(defaultClient);
    }
}
