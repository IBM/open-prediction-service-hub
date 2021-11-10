# Open Prediction Service HUB

## 2.5.0 _2021/11/09_

* [ADSML-137] Add max supported file size for upload ML model

## 2.4.3 _2021/10/19_

* [ADSML-245] WhiteSource scan finds multiple CVE in ads-ml-service repo
* [ADSML-252] Update environment.yml for sklean-service (CVE fix)
* [ADSML-253] ads-ml-service should handle both http and https requests

## 2.4.2 _2021/10/18_

* [ADSML-225] Update database migration for endpoint metadata

## 2.4.1 _2021/10/11_

* [ADSML-235] Install ads-ml-service in the new Fyre env and update installation docs

## 2.4.0 _2021/10/08_

* [ADSML-225] Add metadata in endpoints (PATCH method)

## 2.3.0 _2021/10/06_

* [ADSML-225] Add metadata in endpoints

## 2.2.1 _2021/08/18_

* [ADSML-198] Refine image push configuration
* [ADSML-200] Update https configuration for ads-ml-service

## 2.2.0 _2021/06/23_
* [ADSML-102] Added support for uploading serialised model
* [ADSML-115] Updated Notebooks to work with ads-ml-service
* [ADSML-125] Updated third-party dependencies
* [ADSML-145] Fixed upload of serialized PMML model should not accept only file with "pmml" extension

## 2.1.0 _2021/03/29_

* Added the manage capicity description of supported input, output and binary models
* Added creating of endpoints by uploading binary models
* [ADSML-69] Added cache on loading models in prediction calls
* Added explanation service technical contribution

## 2.0.2 _2021/01/28_

* [ADSML-70] removed credentials reference, they weren't valid anyway

## 2.0.1

* Updated some dependencies due to vulnerability issues in sagemaker service

## 2.0.0

* Releasing OPS v2

## 0.1.0

* RTC-130468 Refactor OPS project structure and naming
* RTC-130348 Add cache for OPS model storage

## 0.0.2

* RTC-130175 Reduce the docker image size of the ads-ml-service

## 0.0.1

* Added changelog
* Makefile test use dev image instead of master
