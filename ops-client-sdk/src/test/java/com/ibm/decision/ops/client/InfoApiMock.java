/*
 * IBM Confidential
 * OCO Source Materials
 * 5737-I23
 * Copyright IBM Corp. 2020
 * The source code for this program is not published or otherwise
 * divested of its trade secrets, irrespective of what has
 * been deposited with the U.S Copyright Office.
 */

package com.ibm.decision.ops.client;


import com.ibm.decision.ops.client.api.InfoApi;
import com.ibm.decision.ops.client.model.Capabilities;
import com.ibm.decision.ops.client.model.Capability;
import com.ibm.decision.ops.client.model.ServerInfo;

import java.util.Arrays;

public class InfoApiMock extends InfoApi {
    @Override
    public ServerInfo getInfo() throws ApiException {
        ServerInfo info = new ServerInfo();
        info.setStatus(ServerInfo.StatusEnum.OK);

        return info;
    }

    @Override
    public Capabilities getCapabilities() throws ApiException {
        final Capability[] c = {Capability.INFO, Capability.DISCOVER, Capability.RUN};

        Capabilities capabilities = new Capabilities();
        capabilities.setCapabilities(Arrays.asList(c));

        return capabilities;
    }
}
