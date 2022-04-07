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

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.ibm.decision.ops.client.model.Prediction;
import com.ibm.decision.ops.client.model.PredictionResponse;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertNotNull;

public class TestRun {

    MlServiceClient client;

    @Before
    public void init() {
        client = new MlServiceClient();
    }

    @Test
    public void shouldGetAValidPrediction() throws ApiException {
        final String payload = "{\n" +
                "  \"parameters\": [{\n" +
                "    \"name\": \"creditScore\",\n" +
                "    \"value\": 200\n" +
                "  }, {\n" +
                "    \"name\": \"income\",\n" +
                "    \"value\": 35000\n" +
                "  }, {\n" +
                "    \"name\": \"loanAmount\",\n" +
                "    \"value\": 10000\n" +
                "  }, {\n" +
                "    \"name\": \"monthDuration\",\n" +
                "    \"value\": 48\n" +
                "  }, {\n" +
                "    \"name\": \"rate\",\n" +
                "    \"value\": 2\n" +
                "  }],\n" +
                "  \"target\": [{\n" +
                "    \"href\": \"http://0.0.0.0:8080/endpoints/regression\",\n" +
                "    \"rel\": \"endpoint\"\n" +
                "  }]\n" +
                "}";

        GsonBuilder builder = new GsonBuilder();
        Gson gson = builder.create();

        Prediction prediction = gson.fromJson(payload, Prediction.class);

        final PredictionResponse response = client.getRunApi().prediction(prediction);

        assertNotNull(response);
    }
}
