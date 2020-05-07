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
