package com.ibm.aid.lml.openapi;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.openapitools.client.ApiException;
import org.openapitools.client.model.MetaMLModel;

import java.io.File;
import java.util.List;
import java.util.Objects;

public class TestAddModel extends AbstractAdminApiTest {

    @Before
    public void init() throws ApiException {
        for (MetaMLModel m : api.getModelsModelsGet()) {
            api.removeModelModelsDelete(m.getName(), m.getVersion());
        }
        Assert.assertEquals(0, (long) api.getServerStatusStatusGet().getCount());
    }

    @After
    public void reInit() throws ApiException {
        for (MetaMLModel m : api.getModelsModelsGet()) {
            api.removeModelModelsDelete(m.getName(), m.getVersion());
        }
        Assert.assertEquals(0, (long) api.getServerStatusStatusGet().getCount());
    }

    /**
     * Add Model
     *
     * @throws ApiException if the Api call fails
     */
    @Test
    public void addModelTest() throws ApiException {

        api.addModelArchivesPost(
                new File(Objects.requireNonNull(getClass().getClassLoader().getResource( "miniloan-rfc.zip")).getFile()));

        List<MetaMLModel> response = api.getModelsModelsGet();

        Assert.assertEquals(1, (long) api.getServerStatusStatusGet().getCount());
    }


}
