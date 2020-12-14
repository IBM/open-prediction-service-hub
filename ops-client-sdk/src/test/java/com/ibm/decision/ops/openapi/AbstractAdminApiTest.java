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

import com.ibm.decision.ops.client.ApiClient;
import com.ibm.decision.ops.client.Configuration;
import com.ibm.decision.ops.client.api.AdminApi;

public abstract class AbstractAdminApiTest {
    public static final String LOCAL_PROVIDER_PATH = "http://localhost:8080/v1";
    final AdminApi api;

    public AbstractAdminApiTest(){
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath(AbstractAdminApiTest.LOCAL_PROVIDER_PATH);
        this.api = new AdminApi(defaultClient);
    }
}
