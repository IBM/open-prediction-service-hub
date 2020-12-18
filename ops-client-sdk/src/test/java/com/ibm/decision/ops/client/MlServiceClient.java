/*
 * Copyright 2020 IBM
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * <p>
 * http://www.apache.org/licenses/LICENSE-2.0
 * <p>
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.IBM Confidential
 */
package com.ibm.decision.ops.client;

import com.ibm.decision.ops.client.api.DiscoverApi;
import com.ibm.decision.ops.client.api.InfoApi;
import com.ibm.decision.ops.client.api.RunApi;

public class MlServiceClient {
    private final InfoApi infoApi;
    private final DiscoverApi discoverApi;
    private final RunApi runApi;

    public MlServiceClient() {

        this.infoApi = new InfoApiMock();
        this.discoverApi = new DiscoverApiMock();
        this.runApi = new RunApiMock();
    }


    public DiscoverApi getDiscoverApi() {
        return discoverApi;
    }

    public InfoApi getInfoApi() {
        return infoApi;
    }

    public RunApi getRunApi() {
        return runApi;
    }
}
