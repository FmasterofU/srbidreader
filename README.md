# srbidreader
some old code for automated read of the Serbian ID card


based on CelikApi Windows 1.3.3

extract_data_from_id_card() returns all data extracted from currently inserted ID card, otherwise throws an exception

returned data are separated into three sections (returning tuple):
 - eid_document_data - document metadata (issuer, date of issue, expiry date, ID card number)
 - eid_fixed_personal_data - fixed personal data that cannot be changed without reissue of the ID card (bith, sex, nationality information, name and surname)
 - eid_variable_personal_data - variable information that can be modified though the validity period of the ID card (current residence/address)