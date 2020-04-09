package com.ibm.aid.lml;

import com.ibm.aid.lml.models.Status;
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.api.AdminApi;
import org.openapitools.client.api.MlApi;
import org.openapitools.client.model.ServerStatus;

public class MlServiceClient {
    private final String url;
    private final AdminApi adminApi;
    private final MlApi mlApi;

    public MlServiceClient(String url) {
        this.url = url;

        ApiClient apiClient = Configuration.getDefaultApiClient().setBasePath(this.url);

        this.mlApi = new MlApi(apiClient);
        this.adminApi = new AdminApi(apiClient);
    }

    public MlServiceClient() {
        this("http://localhost:8080");
    }

    public Status getStatus() throws ApiException {
        ServerStatus ss = adminApi.getServerStatusStatusGet();
        return new Status(ss.getCount());
    }

}
