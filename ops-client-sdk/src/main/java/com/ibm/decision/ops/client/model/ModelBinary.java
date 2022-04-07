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

import com.google.gson.annotations.SerializedName;

import java.io.File;
import java.util.Objects;

/**
 * ModelBinary
 */
@javax.annotation.Generated(value = "org.openapitools.codegen.languages.JavaClientCodegen", date = "2021-08-09T19:00:53.032+02:00[Europe/Paris]")
public class ModelBinary {
  public static final String SERIALIZED_NAME_INPUT_DATA_STRUCTURE = "input_data_structure";
  @SerializedName(SERIALIZED_NAME_INPUT_DATA_STRUCTURE)
  private ModelInput inputDataStructure;

  public static final String SERIALIZED_NAME_OUTPUT_DATA_STRUCTURE = "output_data_structure";
  @SerializedName(SERIALIZED_NAME_OUTPUT_DATA_STRUCTURE)
  private ModelOutput outputDataStructure;

  public static final String SERIALIZED_NAME_FORMAT = "format";
  @SerializedName(SERIALIZED_NAME_FORMAT)
  private ModelWrapper format;

  public static final String SERIALIZED_NAME_FILE = "file";
  @SerializedName(SERIALIZED_NAME_FILE)
  private File file;


  public ModelBinary inputDataStructure(ModelInput inputDataStructure) {

    this.inputDataStructure = inputDataStructure;
    return this;
  }

   /**
   * Get inputDataStructure
   * @return inputDataStructure
  **/
  @javax.annotation.Nullable


  public ModelInput getInputDataStructure() {
    return inputDataStructure;
  }


    public void setInputDataStructure(ModelInput inputDataStructure) {
    this.inputDataStructure = inputDataStructure;
  }


  public ModelBinary outputDataStructure(ModelOutput outputDataStructure) {

    this.outputDataStructure = outputDataStructure;
    return this;
  }

   /**
   * Get outputDataStructure
   * @return outputDataStructure
  **/
  @javax.annotation.Nullable


  public ModelOutput getOutputDataStructure() {
    return outputDataStructure;
  }


    public void setOutputDataStructure(ModelOutput outputDataStructure) {
    this.outputDataStructure = outputDataStructure;
  }


  public ModelBinary format(ModelWrapper format) {

    this.format = format;
    return this;
  }

   /**
   * Get format
   * @return format
  **/
  @javax.annotation.Nullable


  public ModelWrapper getFormat() {
    return format;
  }


    public void setFormat(ModelWrapper format) {
    this.format = format;
  }


  public ModelBinary file(File file) {

    this.file = file;
    return this;
  }

   /**
   * Get file
   * @return file
  **/


  public File getFile() {
    return file;
  }


    public void setFile(File file) {
    this.file = file;
  }


  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    ModelBinary modelBinary = (ModelBinary) o;
        return Objects.equals(this.inputDataStructure, modelBinary.inputDataStructure) &&
        Objects.equals(this.outputDataStructure, modelBinary.outputDataStructure) &&
        Objects.equals(this.format, modelBinary.format) &&
        Objects.equals(this.file, modelBinary.file);
  }

  @Override
  public int hashCode() {
    return Objects.hash(inputDataStructure, outputDataStructure, format, file);
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class ModelBinary {\n");
    sb.append("    inputDataStructure: ").append(toIndentedString(inputDataStructure)).append("\n");
    sb.append("    outputDataStructure: ").append(toIndentedString(outputDataStructure)).append("\n");
    sb.append("    format: ").append(toIndentedString(format)).append("\n");
    sb.append("    file: ").append(toIndentedString(file)).append("\n");
    sb.append("}");
    return sb.toString();
  }

  /**
   * Convert the given object to string with each line indented by 4 spaces
   * (except the first line).
   */
  private String toIndentedString(Object o) {
    if (o == null) {
      return "null";
    }
    return o.toString().replace("\n", "\n    ");
  }

}
