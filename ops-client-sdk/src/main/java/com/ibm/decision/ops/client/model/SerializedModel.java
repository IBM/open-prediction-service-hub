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

import java.util.Objects;

/**
 * SerializedModel
 */
@javax.annotation.Generated(value = "org.openapitools.codegen.languages.JavaClientCodegen", date = "2021-08-09T19:00:53.032+02:00[Europe/Paris]")
public class SerializedModel {
  public static final String SERIALIZED_NAME_FILE_CONTENT_TYPE = "fileContentType";
  @SerializedName(SERIALIZED_NAME_FILE_CONTENT_TYPE)
  private String fileContentType;

  public static final String SERIALIZED_NAME_FILE_NAME = "fileName";
  @SerializedName(SERIALIZED_NAME_FILE_NAME)
  private String fileName;

  public static final String SERIALIZED_NAME_FILE_CONTENT_LENGTH = "fileContentLength";
  @SerializedName(SERIALIZED_NAME_FILE_CONTENT_LENGTH)
  private Long fileContentLength;

  public static final String SERIALIZED_NAME_FILE = "file";
  @SerializedName(SERIALIZED_NAME_FILE)
  private Object file;


  public SerializedModel fileContentType(String fileContentType) {

    this.fileContentType = fileContentType;
    return this;
  }

   /**
   * Get fileContentType
   * @return fileContentType
  **/
  @javax.annotation.Nullable


  public String getFileContentType() {
    return fileContentType;
  }


    public void setFileContentType(String fileContentType) {
    this.fileContentType = fileContentType;
  }


  public SerializedModel fileName(String fileName) {

    this.fileName = fileName;
    return this;
  }

   /**
   * Get fileName
   * @return fileName
  **/
  @javax.annotation.Nullable


  public String getFileName() {
    return fileName;
  }


    public void setFileName(String fileName) {
    this.fileName = fileName;
  }


  public SerializedModel fileContentLength(Long fileContentLength) {

    this.fileContentLength = fileContentLength;
    return this;
  }

   /**
   * Get fileContentLength
   * @return fileContentLength
  **/
  @javax.annotation.Nullable


  public Long getFileContentLength() {
    return fileContentLength;
  }


    public void setFileContentLength(Long fileContentLength) {
    this.fileContentLength = fileContentLength;
  }


  public SerializedModel file(Object file) {

    this.file = file;
    return this;
  }

   /**
   * Get file
   * @return file
  **/


  public Object getFile() {
    return file;
  }


    public void setFile(Object file) {
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
    SerializedModel serializedModel = (SerializedModel) o;
        return Objects.equals(this.fileContentType, serializedModel.fileContentType) &&
        Objects.equals(this.fileName, serializedModel.fileName) &&
        Objects.equals(this.fileContentLength, serializedModel.fileContentLength) &&
        Objects.equals(this.file, serializedModel.file);
  }

  @Override
  public int hashCode() {
    return Objects.hash(fileContentType, fileName, fileContentLength, file);
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class SerializedModel {\n");
    sb.append("    fileContentType: ").append(toIndentedString(fileContentType)).append("\n");
    sb.append("    fileName: ").append(toIndentedString(fileName)).append("\n");
    sb.append("    fileContentLength: ").append(toIndentedString(fileContentLength)).append("\n");
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
