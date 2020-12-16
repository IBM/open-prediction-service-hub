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
package com.ibm.decision.ops.client.model;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.TypeAdapter;
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonToken;
import com.google.gson.stream.JsonWriter;

import java.io.IOException;
import java.math.BigDecimal;
import java.math.BigInteger;

public class AnySerializer extends TypeAdapter<AnyOfintegernumberstringboolean> {
    @Override
    public void write(JsonWriter out, AnyOfintegernumberstringboolean user) throws IOException {
        Object obj = user.getValue();

        if (obj instanceof Integer) {
            out.value(((Integer) obj).intValue());
        } else if (obj instanceof Short) {
            out.value(((Short) obj).shortValue());
        } else if (obj instanceof Byte) {
            out.value(((Byte) obj).byteValue());
        } else if (obj instanceof BigDecimal) {
            out.value(((BigDecimal) obj).doubleValue());
        } else if (obj instanceof BigInteger) {
            out.value(((BigInteger) obj).longValue());
        } else if (obj instanceof Double) {
            out.value(((Double) obj).doubleValue());
        } else if (obj instanceof Float) {
            out.value(((Float) obj).floatValue());
        } else if (obj instanceof Long) {
            out.value(((Long) obj).longValue());
        } else if (obj instanceof Boolean) {
            out.value(((Boolean) obj).booleanValue());
        } else {
            out.value(user.toString());
        }
    }

    @Override
    public AnyOfintegernumberstringboolean read(JsonReader in) throws IOException {
        AnyOfintegernumberstringboolean result = null;

        JsonToken nextToken = in.peek();
        switch (nextToken) {
            case NUMBER:


                String value = in.nextString();
                GsonBuilder builder = new GsonBuilder();
                Gson gson = builder.create();
                Number number = gson.fromJson(value, Number.class);
                result = AnyOfintegernumberstringboolean.build(number);

                break;

            case STRING:
                result = new AnyOfintegernumberstringboolean(in.nextString());
                break;
            case BOOLEAN:
                result = new AnyOfintegernumberstringboolean(in.nextBoolean());
        }

        return result;
    }
}



