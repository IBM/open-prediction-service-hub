package com.ibm.aid.lml.openapi;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.openapitools.client.ApiException;
import org.openapitools.client.model.Feature;
import org.openapitools.client.model.MetaMLModel;

import java.io.File;
import java.util.List;
import java.util.Objects;

public class TestGetModels extends AbstractAdminApiTest{

    @Before
    public void init() throws ApiException {
        for (MetaMLModel m : api.getModelsModelsGet()) {
            api.removeModelModelsDelete(m.getName(), m.getVersion());
        }
        Assert.assertEquals(0, (long) api.getServerStatusStatusGet().getCount());

        api.addModelArchivesPost(
                new File(Objects.requireNonNull(getClass().getClassLoader().getResource( "miniloan-rfc.zip")).getFile()));

        Assert.assertEquals(1, (long) api.getServerStatusStatusGet().getCount());
    }

    @After
    public void reInit() throws ApiException {
        for (MetaMLModel m : api.getModelsModelsGet()) {
            api.removeModelModelsDelete(m.getName(), m.getVersion());
        }
        Assert.assertEquals(0, (long) api.getServerStatusStatusGet().getCount());
    }

    /**
     * Get Models
     *
     * Returns the list of ML models.
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void getModelTest() throws ApiException {

        List<MetaMLModel> response = api.getModelsModelsGet();

        MetaMLModel miniloanRfc = response.get(0);

        Assert.assertEquals("miniloan-rfc", miniloanRfc.getName());
        Assert.assertEquals("v0", miniloanRfc.getVersion());
        Assert.assertEquals("predict_proba", miniloanRfc.getMethodName());
        Assert.assertEquals(MetaMLModel.TypeEnum.PREDICT_PROBA, miniloanRfc.getType());

        List<Feature> inputSchema = miniloanRfc.getInputSchema();

        Assert.assertEquals((new Feature().name("creditScore").order(0).type("int64")), inputSchema.get(0));
        Assert.assertEquals((new Feature().name("income").order(1).type("float32")), inputSchema.get(1));
        Assert.assertEquals((new Feature().name("loanAmount").order(2).type("float64")), inputSchema.get(2));
        Assert.assertEquals((new Feature().name("monthDuration").order(3).type("float64")), inputSchema.get(3));
        Assert.assertEquals((new Feature().name("rate").order(4).type("float64")), inputSchema.get(4));

        Assert.assertEquals("Loan approval", miniloanRfc.getMetadata().getDescription());
        Assert.assertEquals("ke", miniloanRfc.getMetadata().getAuthor());
        Assert.assertEquals("accuracy", miniloanRfc.getMetadata().getMetrics().get(0).getName());
    }
}
