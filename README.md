# easy_encode

# type mapping

priority: lowest -> highest

- client -> passed type_mapping{}
- data_store.DEFAULT_ENCODING_TYPE_MAPPING
- data_store -> passed type_mapping{}

# type conversions

priority: lowest -> highest

- easy_encode.data_conversions.TYPE_CONVERSIONS
- client -> passed type_conversions{}
- data_store.DEFAULT_TYPE_CONVERSIONS
- data_store -> passed type_conversions{}
- encoding/decoding_function
