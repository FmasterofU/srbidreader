import ctypes
import pathlib
from enum import IntEnum
import json

EID_MAX_DocRegNo = 9
EID_MAX_DocumentType = 2
EID_MAX_IssuingDate = 10
EID_MAX_ExpiryDate = 10
EID_MAX_IssuingAuthority = 100
EID_MAX_DocumentSerialNumber = 10
EID_MAX_ChipSerialNumber = 14

class EID_DOCUMENT_DATA(ctypes.Structure):
    _fields_ = [
        ("docRegNo", ctypes.c_char*EID_MAX_DocRegNo),
        ("docRegNoSize", ctypes.c_int),
        ("documentType", ctypes.c_char*EID_MAX_DocumentType),
        ("documentTypeSize", ctypes.c_int),
        ("issuingDate", ctypes.c_char*EID_MAX_IssuingDate),
        ("issuingDateSize", ctypes.c_int),
        ("expiryDate", ctypes.c_char*EID_MAX_ExpiryDate),
        ("expiryDateSize", ctypes.c_int),
        ("issuingAuthority", ctypes.c_char*EID_MAX_IssuingAuthority),
        ("issuingAuthoritySize", ctypes.c_int),
        ("documentSerialNumber", ctypes.c_char*EID_MAX_DocumentSerialNumber),
        ("documentSerialNumberSize", ctypes.c_int),
        ("chipSerialNumber", ctypes.c_char*EID_MAX_ChipSerialNumber),
        ("chipSerialNumberSize", ctypes.c_int)
    ]

EID_MAX_PersonalNumber = 13
EID_MAX_Surname = 200
EID_MAX_GivenName = 200
EID_MAX_ParentGivenName = 200
EID_MAX_Sex = 2
EID_MAX_PlaceOfBirth = 200
EID_MAX_StateOfBirth = 200
EID_MAX_DateOfBirth = 10
EID_MAX_CommunityOfBirth = 200
EID_MAX_StatusOfForeigner = 200
EID_MAX_NationalityFull = 200

class EID_FIXED_PERSONAL_DATA(ctypes.Structure):
    _fields_ = [
        ("personalNumber", ctypes.c_char*EID_MAX_PersonalNumber),
        ("personalNumberSize", ctypes.c_int),
        ("surname", ctypes.c_char*EID_MAX_Surname),
        ("surnameSize", ctypes.c_int),
        ("givenName", ctypes.c_char*EID_MAX_GivenName),
        ("givenNameSize", ctypes.c_int),
        ("parentGivenName", ctypes.c_char*EID_MAX_ParentGivenName),
        ("parentGivenNameSize", ctypes.c_int),
        ("sex", ctypes.c_char*EID_MAX_Sex),
        ("sexSize", ctypes.c_int),
        ("placeOfBirth", ctypes.c_char*EID_MAX_PlaceOfBirth),
        ("placeOfBirthSize", ctypes.c_int),
        ("stateOfBirth", ctypes.c_char*EID_MAX_StateOfBirth),
        ("stateOfBirthSize", ctypes.c_int),
        ("dateOfBirth", ctypes.c_char*EID_MAX_DateOfBirth),
        ("dateOfBirthSize", ctypes.c_int),
        ("communityOfBirth", ctypes.c_char*EID_MAX_CommunityOfBirth),
        ("communityOfBirthSize", ctypes.c_int),
        ("statusOfForeigner", ctypes.c_char*EID_MAX_StatusOfForeigner),
        ("statusOfForeignerSize", ctypes.c_int),
        ("nationalityFull", ctypes.c_char*EID_MAX_NationalityFull),
        ("nationalityFullSize", ctypes.c_int),
    ]

EID_MAX_State = 100
EID_MAX_Community = 200
EID_MAX_Place = 200
EID_MAX_Street = 200
EID_MAX_HouseNumber = 20
EID_MAX_HouseLetter = 8
EID_MAX_Entrance = 10
EID_MAX_Floor = 6
EID_MAX_ApartmentNumber = 12
EID_MAX_AddressDate = 10
EID_MAX_AddressLabel = 60

class EID_VARIABLE_PERSONAL_DATA(ctypes.Structure):
    _fields_ = [
        ("state", ctypes.c_char*EID_MAX_State),
        ("stateSize", ctypes.c_int),
        ("community", ctypes.c_char*EID_MAX_Community),
        ("communitySize", ctypes.c_int),
        ("place", ctypes.c_char*EID_MAX_Place),
        ("placeSize", ctypes.c_int),
        ("street", ctypes.c_char*EID_MAX_Street),
        ("streetSize", ctypes.c_int),
        ("houseNumber", ctypes.c_char*EID_MAX_HouseNumber),
        ("houseNumberSize", ctypes.c_int),
        ("houseLetter", ctypes.c_char*EID_MAX_HouseLetter),
        ("houseLetterSize", ctypes.c_int),
        ("entrance", ctypes.c_char*EID_MAX_Entrance),
        ("entranceSize", ctypes.c_int),
        ("floor", ctypes.c_char*EID_MAX_Floor),
        ("floorSize", ctypes.c_int),
        ("apartmentNumber", ctypes.c_char*EID_MAX_ApartmentNumber),
        ("apartmentNumberSize", ctypes.c_int),
        ("addressDate", ctypes.c_char*EID_MAX_AddressDate),
        ("addressDateSize", ctypes.c_int),
        ("addressLabel", ctypes.c_char*EID_MAX_AddressLabel),
        ("addressLabelSize", ctypes.c_int)
    ]

class ID_card_type(IntEnum):
    EID_CARD_ID2008 = 1
    EID_CARD_ID2014 = 2
    EID_CARD_IF2020 = 3 # ID for foreigners

class response_codes(IntEnum):
    EID_OK = 0
    EID_E_GENERAL_ERROR = -1
    EID_E_INVALID_PARAMETER = -2
    EID_E_VERSION_NOT_SUPPORTED = -3
    EID_E_NOT_INITIALIZED = -4
    EID_E_UNABLE_TO_EXECUTE = -5
    EID_E_READER_ERROR = -6
    EID_E_CARD_MISSING = -7
    EID_E_CARD_UNKNOWN = -8
    EID_E_CARD_MISMATCH = -9
    EID_E_UNABLE_TO_OPEN_SESSION = -10
    EID_E_DATA_MISSING = -11
    EID_E_CARD_SECFORMAT_CHECK_ERROR = -12
    EID_E_SECFORMAT_CHECK_CERT_ERROR = -13
    EID_E_INVALID_PASSWORD = -14
    EID_E_PIN_BLOCKED = -15


CELIK_API_VERSION = 3


class Celik:
    def __init__(self):
        system_type_str = str(ctypes.sizeof(ctypes.c_voidp) * 8) + "-bit"
        libname = pathlib.Path().absolute() / system_type_str / "CelikApi.dll"
        self.api = ctypes.CDLL(str(libname))
    def __enter__(self):
        response = self.api.EidStartup(CELIK_API_VERSION)
        if response != response_codes.EID_OK.value:
            raise Exception("Čelik startup error.")
        return self.api
    def __exit__(self, exception_type, exception_value, exception_traceback):
        response = self.api.EidCleanup()
        if response != response_codes.EID_OK.value:
            raise Exception("Čelik cleanup error.")

class ID_card:
    def __init__(self, celik, smart_card_reader_id = b'', busy_wait = False, wait_for = 0):
        self.celik = celik
        self.smart_card_reader_device_name = smart_card_reader_id
    def __enter__(self):
        c_id_card_type = ctypes.c_int(0)
        device_name = ctypes.create_string_buffer(self.smart_card_reader_device_name)
        response = celik.EidBeginRead(device_name, ctypes.byref(c_id_card_type))
        if response != response_codes.EID_OK.value:
            raise Exception("ID card begin read error.")
        if c_id_card_type.value not in iter(ID_card_type):
            print("Wrong ID card or the ID card has not been inserted.") #temporary
        else: #temporary, until proper handling
            self.id_card_type = ID_card_type(c_id_card_type.value)
        return self
    def __exit__(self, exception_type, exception_value, exception_traceback):
        response = self.celik.EidEndRead()
        if response != response_codes.EID_OK.value:
            raise Exception("Čelik end read error.")
    def extract_data_from_id_card(self):
        eid_document_data = EID_DOCUMENT_DATA()
        response = celik.EidReadDocumentData(ctypes.byref(eid_document_data))
        if response != response_codes.EID_OK.value:
            raise Exception("Error on read of ID Document data.")
        eid_fixed_personal_data = EID_FIXED_PERSONAL_DATA()
        response = celik.EidReadFixedPersonalData(ctypes.byref(eid_fixed_personal_data))
        if response != response_codes.EID_OK.value:
            raise Exception("Error on read of ID Fixed Personal Data.")
        eid_variable_personal_data = EID_VARIABLE_PERSONAL_DATA()
        response = celik.EidReadVariablePersonalData(ctypes.byref(eid_variable_personal_data))
        if response != response_codes.EID_OK.value:
            raise Exception("Error on read of ID Variable Personal Data")
        return self.__resize_eid_structure(eid_document_data), self.__resize_eid_structure(eid_fixed_personal_data), self.__resize_eid_structure(eid_variable_personal_data)
    def _resize_ctypes_char_array(self, old_array, new_size):
        new_array_type = ctypes.c_char * new_size
        new_array = new_array_type()
        min_size = min(len(old_array), new_size)
        ctypes.memmove(new_array, old_array, min_size)
        return new_array
    def __resize_eid_structure(self, eid_structure):
        for field, _ in eid_structure._fields_:
            if isinstance(getattr(eid_structure, field), (bytes)):
                setattr(eid_structure, field, bytes(self._resize_ctypes_char_array(getattr(eid_structure, field), getattr(eid_structure, field + "Size"))))
        return eid_structure

def ctypes_structure_to_dict(structure_instance):
    result = {}
    for field, _ in structure_instance._fields_:
        if isinstance(getattr(structure_instance, field), (bytes, bytearray)):
            result[field] = getattr(structure_instance, field).decode()
        else:
            result[field] = getattr(structure_instance, field)
    return result

def print_eid_document_data(eid_document_data):
    print("docRegNo (" + str(eid_document_data.docRegNoSize) + " bytes): " + eid_document_data.docRegNo.decode() + '\n', \
        "documentType (" + str(eid_document_data.documentTypeSize) + " bytes): " + eid_document_data.documentType.decode() + '\n', \
        "issuingDate (" + str(eid_document_data.issuingDateSize) + " bytes): " + eid_document_data.issuingDate.decode() + '\n', \
        "expiryDate (" + str(eid_document_data.expiryDateSize) + " bytes): " + eid_document_data.expiryDate.decode() + '\n', \
        "issuingAuthority (" + str(eid_document_data.issuingAuthoritySize) + " bytes): " + eid_document_data.issuingAuthority.decode() + '\n', \
        "documentSerialNumber (" + str(eid_document_data.documentSerialNumberSize) + " bytes): " + eid_document_data.documentSerialNumber.decode() + '\n', \
        "chipSerialNumber (" + str(eid_document_data.chipSerialNumberSize) + " bytes): " + eid_document_data.chipSerialNumber.decode())

def print_eid_fixed_personal_data(eid_fixed_personal_data):
    print("personalNumber (" + str(eid_fixed_personal_data.personalNumberSize) + " bytes) : " + eid_fixed_personal_data.personalNumber.decode() + '\n', \
        "surname (" + str(eid_fixed_personal_data.surnameSize) + " bytes) : " + eid_fixed_personal_data.surname.decode() + '\n', \
        "givenName (" + str(eid_fixed_personal_data.givenNameSize) + " bytes) : " + eid_fixed_personal_data.givenName.decode() + '\n', \
        "parentGivenName (" + str(eid_fixed_personal_data.parentGivenNameSize) + " bytes) : " + eid_fixed_personal_data.parentGivenName.decode() + '\n', \
        "sex (" + str(eid_fixed_personal_data.sexSize) + " bytes) : " + eid_fixed_personal_data.sex.decode() + '\n', \
        "placeOfBirth (" + str(eid_fixed_personal_data.placeOfBirthSize) + " bytes) : " + eid_fixed_personal_data.placeOfBirth.decode() + '\n', \
        "stateOfBirth (" + str(eid_fixed_personal_data.stateOfBirthSize) + " bytes) : " + eid_fixed_personal_data.stateOfBirth.decode() + '\n', \
        "dateOfBirth (" + str(eid_fixed_personal_data.dateOfBirthSize) + " bytes) : " + eid_fixed_personal_data.dateOfBirth.decode() + '\n', \
        "communityOfBirth (" + str(eid_fixed_personal_data.communityOfBirthSize) + " bytes) : " + eid_fixed_personal_data.communityOfBirth.decode() + '\n', \
        "statusOfForeigner (" + str(eid_fixed_personal_data.statusOfForeignerSize) + " bytes) : " + eid_fixed_personal_data.statusOfForeigner.decode() + '\n', \
        "nationalityFull (" + str(eid_fixed_personal_data.nationalityFullSize) + " bytes) : " + eid_fixed_personal_data.nationalityFull.decode())

def print_eid_variable_personal_data(eid_variable_personal_data):
    print("state (" + str(eid_variable_personal_data.stateSize) + " bytes) : " + eid_variable_personal_data.state.decode() + '\n', \
        "community (" + str(eid_variable_personal_data.communitySize) + " bytes) : " + eid_variable_personal_data.community.decode() + '\n', \
        "place (" + str(eid_variable_personal_data.placeSize) + " bytes) : " + eid_variable_personal_data.place.decode() + '\n', \
        "street (" + str(eid_variable_personal_data.streetSize) + " bytes) : " + eid_variable_personal_data.street.decode() + '\n', \
        "houseNumber (" + str(eid_variable_personal_data.houseNumberSize) + " bytes) : " + eid_variable_personal_data.houseNumber.decode() + '\n', \
        "houseLetter (" + str(eid_variable_personal_data.houseLetterSize) + " bytes) : " + eid_variable_personal_data.houseLetter.decode() + '\n', \
        "entrance (" + str(eid_variable_personal_data.entranceSize) + " bytes) : " + eid_variable_personal_data.entrance.decode() + '\n', \
        "floor (" + str(eid_variable_personal_data.floorSize) + " bytes) : " + eid_variable_personal_data.floor.decode() + '\n', \
        "apartmentNumber (" + str(eid_variable_personal_data.apartmentNumberSize) + " bytes) : " + eid_variable_personal_data.apartmentNumber.decode() + '\n', \
        "addressDate (" + str(eid_variable_personal_data.addressDateSize) + " bytes) : " + eid_variable_personal_data.addressDate.decode() + '\n', \
        "addressLabel (" + str(eid_variable_personal_data.addressLabelSize) + " bytes) : " + eid_variable_personal_data.addressLabel.decode())

if __name__ == "__main__":
    with Celik() as celik:
        eid_document_data, eid_fixed_personal_data, eid_variable_personal_data = None, None, None
        with ID_card(celik) as id_card:
            eid_document_data, eid_fixed_personal_data, eid_variable_personal_data = id_card.extract_data_from_id_card()
        #eid_document_data.docRegNo=b"010111111"
        #eid_fixed_personal_data.personalNumber=b"1111111111100"
        data = {
            "eid_document_data" : ctypes_structure_to_dict(eid_document_data),
            "eid_fixed_personal_data" : ctypes_structure_to_dict(eid_fixed_personal_data),
            "eid_variable_personal_data" : ctypes_structure_to_dict(eid_variable_personal_data)
        }
        print(json.dumps(data))
        print_eid_document_data(eid_document_data)
        print_eid_fixed_personal_data(eid_fixed_personal_data)
        print_eid_variable_personal_data(eid_variable_personal_data)
        #buffer = ctypes.create_string_buffer(2000)
        #print(str(buffer.raw, encoding="utf-8"))
        
