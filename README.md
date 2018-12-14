ALL CRITEO DATASETS ARE LICENSED BY CRITEO. CONTACT THEM FOR PERSONAL ACCESS TO THE DATA

## Criteo Conversion Dataset
http://labs.criteo.com/2013/12/download-conversion-logs-dataset/
~1.5 Gb, 15mil clicks

Dataset construction:

The dataset consists of a portion of Criteo's traffic over a period of two months.
Each row corresponds to a display ad served by Criteo and subsequently clicked by the user.
The first column is the timestamp (in seconds) of the click relative to the beginning of the period.
The second column indicates the timestamp of the conversion. If no conversion occured, this field is blank.
The dataset has been subsampled in order to reduce its size.

There are 8 features taking integer values (mostly count features) and 9 categorical features.
The values of the categorical features have been hashed onto 32 bits for anonymization purposes.
The semantic of these features is undisclosed. Some features may have missing values.

The rows are chronologically ordered.
The campaignId column (needed to filter the recent campaigns) is column #13.

Format:

The columns are tab separated with the following schema:
<click timestamp> <conversion timestamp> <integer feature 1> ... <integer feature 8> <categorical feature 1> ... <categorical feature 9>

When a value is missing, the field is just empty.


## Criteo TB Dataset
NC: there is no timestamp available. the highest grain date is 'day'

See http://labs.criteo.com/2013/12/download-terabyte-click-logs-2/

You likely need a license for the data. Contact Criteo before downloading or using their data.
```
for i in {0..23}; do
    curl http://azuremlsampleexperiments.blob.core.windows.net/criteo/day_${i}.gz | \
        gzip -d | wormhole/bin/convert.dmlc -data_in stdin -format_in criteo \
        -data_out day_${i} -format_out libsvm
done
```