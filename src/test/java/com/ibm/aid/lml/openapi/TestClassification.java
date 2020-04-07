package com.ibm.aid.lml.openapi;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.openapitools.client.ApiException;
import org.openapitools.client.model.*;

import java.io.File;
import java.util.Objects;

public class TestClassification extends AbstractMLApiTest{
    @Before
    public void init() throws ApiException {
        for (MetaMLModel m : adminApi.getModelsModelsGet()) {
            adminApi.removeModelModelsDelete(m.getName(), m.getVersion());
        }
        Assert.assertEquals(0, (long) adminApi.getServerStatusStatusGet().getCount());

        adminApi.addModelArchivesPost(
                new File(Objects.requireNonNull(getClass().getClassLoader().getResource("miniloan-lr.zip")).getFile()));

        Assert.assertEquals(1, (long) adminApi.getServerStatusStatusGet().getCount());
    }

    /**
     * Predict Proba
     *
     * @throws ApiException if the Api call fails
     */
    @Test
    public void classificationTest() throws ApiException {
        RequestBody requestBody = new RequestBody()
                .modelName("miniloan-lr")
                .modelVersion("v0")
                .addParamsItem(new Parameter().name("creditScore").value("200"))
                .addParamsItem(new Parameter().name("income").value("36000"))
                .addParamsItem(new Parameter().name("loanAmount").value("3000"))
                .addParamsItem(new Parameter().name("monthDuration").value("13"))
                .addParamsItem(new Parameter().name("rate").value("2.6"));

        ClassificationResponse response = mlApi.classificationClassificationPost(requestBody);

        Assert.assertEquals("true", response.getClassificationOutput());
    }


    @After
    public void reInit() throws ApiException {
        for (MetaMLModel m : adminApi.getModelsModelsGet()) {
            adminApi.removeModelModelsDelete(m.getName(), m.getVersion());
        }
        Assert.assertEquals(0, (long) adminApi.getServerStatusStatusGet().getCount());
    }

}
