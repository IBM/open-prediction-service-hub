package com.ibm.aid.lml.openapi;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.openapitools.client.ApiException;
import org.openapitools.client.model.MetaMLModel;

import java.io.File;
import java.util.Objects;

public class TestRemoveModel extends AbstractAdminApiTest{
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

    @Test
    public void removeModelTest() throws ApiException{
        api.removeModelModelsDelete("miniloan-rfc", null);
        Assert.assertEquals(0, (long) api.getServerStatusStatusGet().getCount());
    }
}
