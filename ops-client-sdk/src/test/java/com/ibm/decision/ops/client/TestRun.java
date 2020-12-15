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
