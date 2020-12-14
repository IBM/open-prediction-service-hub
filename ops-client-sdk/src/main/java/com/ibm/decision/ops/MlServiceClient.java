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
package com.ibm.decision.ops;

import com.ibm.decision.ops.models.Status;
import com.ibm.decision.ops.client.ApiClient;
import com.ibm.decision.ops.client.ApiException;
import com.ibm.decision.ops.client.Configuration;
import com.ibm.decision.ops.client.api.AdminApi;
import com.ibm.decision.ops.client.api.MlApi;
import com.ibm.decision.ops.client.model.ServerStatus;

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
        this("http://localhost:8080/v1");
    }

    public Status getStatus() throws ApiException {
        ServerStatus ss = adminApi.getServerStatusStatusGet();
        return new Status(ss.getModelCount());
    }

}
