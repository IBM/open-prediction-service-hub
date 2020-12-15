/*
 * IBM Confidential
 * OCO Source Materials
 * 5737-I23
 * Copyright IBM Corp. 2019, 2020
 * The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
 */

package com.ibm.decision.ops.client;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class MockResources {

    public static final String resourceRoot = "mock";

    public static final String[] resourceModels = {"regression"};

    public static final Gson gson = new GsonBuilder().create();

    public static <T> List<T> getResourceList(String resourceFile, Class<T> valueType) throws ApiException {
        List<T> resourceList = new ArrayList<>();

        for (String resourceModel : MockResources.resourceModels) {
            resourceList.add(getResourceModel(resourceModel, resourceFile, valueType));
        }
        return resourceList;
    }

    public static <T> T getResourceModel(String resourceModel, String resourceFile, Class<T> valueType) throws ApiException {
        ClassLoader classLoader = MockResources.class.getClassLoader();

        String resourcePath = MockResources.resourceRoot + "/" + resourceModel + "/" + resourceFile;
        try (InputStream inputStream = classLoader.getResourceAsStream(resourcePath)) {
            if (inputStream != null) {
                return gson.fromJson(new InputStreamReader(inputStream), valueType);
            }
        } catch (Exception e) {
            throw new ApiException(e);
        }

        return null;
    }
}
