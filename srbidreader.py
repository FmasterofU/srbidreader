import ctypes
import pathlib
from enum import IntEnum
import json

_FAKE_CELIK = False

EID_MAX_DocRegNo = 9
EID_MAX_DocumentType = 2
EID_MAX_IssuingDate = 10
EID_MAX_ExpiryDate = 10
EID_MAX_IssuingAuthority = 100
EID_MAX_DocumentSerialNumber = 10
EID_MAX_ChipSerialNumber = 14


class EID_DOCUMENT_DATA(ctypes.Structure):
    _fields_ = [
        ("docRegNo", ctypes.c_char * EID_MAX_DocRegNo),
        ("docRegNoSize", ctypes.c_int),
        ("documentType", ctypes.c_char * EID_MAX_DocumentType),
        ("documentTypeSize", ctypes.c_int),
        ("issuingDate", ctypes.c_char * EID_MAX_IssuingDate),
        ("issuingDateSize", ctypes.c_int),
        ("expiryDate", ctypes.c_char * EID_MAX_ExpiryDate),
        ("expiryDateSize", ctypes.c_int),
        ("issuingAuthority", ctypes.c_char * EID_MAX_IssuingAuthority),
        ("issuingAuthoritySize", ctypes.c_int),
        ("documentSerialNumber", ctypes.c_char * EID_MAX_DocumentSerialNumber),
        ("documentSerialNumberSize", ctypes.c_int),
        ("chipSerialNumber", ctypes.c_char * EID_MAX_ChipSerialNumber),
        ("chipSerialNumberSize", ctypes.c_int),
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
        ("personalNumber", ctypes.c_char * EID_MAX_PersonalNumber),
        ("personalNumberSize", ctypes.c_int),
        ("surname", ctypes.c_char * EID_MAX_Surname),
        ("surnameSize", ctypes.c_int),
        ("givenName", ctypes.c_char * EID_MAX_GivenName),
        ("givenNameSize", ctypes.c_int),
        ("parentGivenName", ctypes.c_char * EID_MAX_ParentGivenName),
        ("parentGivenNameSize", ctypes.c_int),
        ("sex", ctypes.c_char * EID_MAX_Sex),
        ("sexSize", ctypes.c_int),
        ("placeOfBirth", ctypes.c_char * EID_MAX_PlaceOfBirth),
        ("placeOfBirthSize", ctypes.c_int),
        ("stateOfBirth", ctypes.c_char * EID_MAX_StateOfBirth),
        ("stateOfBirthSize", ctypes.c_int),
        ("dateOfBirth", ctypes.c_char * EID_MAX_DateOfBirth),
        ("dateOfBirthSize", ctypes.c_int),
        ("communityOfBirth", ctypes.c_char * EID_MAX_CommunityOfBirth),
        ("communityOfBirthSize", ctypes.c_int),
        ("statusOfForeigner", ctypes.c_char * EID_MAX_StatusOfForeigner),
        ("statusOfForeignerSize", ctypes.c_int),
        ("nationalityFull", ctypes.c_char * EID_MAX_NationalityFull),
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
        ("state", ctypes.c_char * EID_MAX_State),
        ("stateSize", ctypes.c_int),
        ("community", ctypes.c_char * EID_MAX_Community),
        ("communitySize", ctypes.c_int),
        ("place", ctypes.c_char * EID_MAX_Place),
        ("placeSize", ctypes.c_int),
        ("street", ctypes.c_char * EID_MAX_Street),
        ("streetSize", ctypes.c_int),
        ("houseNumber", ctypes.c_char * EID_MAX_HouseNumber),
        ("houseNumberSize", ctypes.c_int),
        ("houseLetter", ctypes.c_char * EID_MAX_HouseLetter),
        ("houseLetterSize", ctypes.c_int),
        ("entrance", ctypes.c_char * EID_MAX_Entrance),
        ("entranceSize", ctypes.c_int),
        ("floor", ctypes.c_char * EID_MAX_Floor),
        ("floorSize", ctypes.c_int),
        ("apartmentNumber", ctypes.c_char * EID_MAX_ApartmentNumber),
        ("apartmentNumberSize", ctypes.c_int),
        ("addressDate", ctypes.c_char * EID_MAX_AddressDate),
        ("addressDateSize", ctypes.c_int),
        ("addressLabel", ctypes.c_char * EID_MAX_AddressLabel),
        ("addressLabelSize", ctypes.c_int),
    ]


class ID_card_type(IntEnum):
    EID_CARD_ID2008 = 1
    EID_CARD_ID2014 = 2
    EID_CARD_IF2020 = 3  # ID for foreigners


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
        if _FAKE_CELIK:
            return

        system_type_str = str(ctypes.sizeof(ctypes.c_voidp) * 8) + "-bit"
        libname = pathlib.Path().absolute() / system_type_str / "CelikApi.dll"
        self.api = ctypes.CDLL(str(libname))

    def __enter__(self):
        if _FAKE_CELIK:
            return

        response = self.api.EidStartup(CELIK_API_VERSION)
        if response != response_codes.EID_OK.value:
            raise Exception("Čelik startup error: " + str(response))
        return self.api

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if _FAKE_CELIK:
            return

        response = self.api.EidCleanup()
        if response != response_codes.EID_OK.value:
            raise Exception("Čelik cleanup error: " + str(response))


class ID_card:

    def __init__(self, celik, smart_card_reader_id=b"", busy_wait=False, wait_for=0):
        self.celik = celik
        self.smart_card_reader_device_name = smart_card_reader_id

    def __enter__(self):
        if _FAKE_CELIK:
            return self

        c_id_card_type = ctypes.c_int(0)
        device_name = ctypes.create_string_buffer(self.smart_card_reader_device_name)
        response = self.celik.EidBeginRead(device_name, ctypes.byref(c_id_card_type))
        if response != response_codes.EID_OK.value:
            raise Exception("ID card begin read error.")
        self.id_card_type = ID_card_type(c_id_card_type.value)
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if _FAKE_CELIK:
            return self

        response = self.celik.EidEndRead()
        if response != response_codes.EID_OK.value:
            raise Exception("Čelik end read error: " + str(response))

    def extract_data_from_id_card(self):
        if _FAKE_CELIK:
            return (
                EID_DOCUMENT_DATA(),
                EID_FIXED_PERSONAL_DATA(),
                EID_VARIABLE_PERSONAL_DATA(),
            )

        eid_document_data = EID_DOCUMENT_DATA()
        response = self.celik.EidReadDocumentData(ctypes.byref(eid_document_data))
        if response != response_codes.EID_OK.value:
            raise Exception("Error on read of ID Document data: " + str(response))
        eid_fixed_personal_data = EID_FIXED_PERSONAL_DATA()
        response = self.celik.EidReadFixedPersonalData(
            ctypes.byref(eid_fixed_personal_data)
        )
        if response != response_codes.EID_OK.value:
            raise Exception("Error on read of ID Fixed Personal Data: " + str(response))
        eid_variable_personal_data = EID_VARIABLE_PERSONAL_DATA()
        response = self.celik.EidReadVariablePersonalData(
            ctypes.byref(eid_variable_personal_data)
        )
        if response != response_codes.EID_OK.value:
            raise Exception(
                "Error on read of ID Variable Personal Data: " + str(response)
            )
        return (
            self.__resize_eid_structure(eid_document_data),
            self.__resize_eid_structure(eid_fixed_personal_data),
            self.__resize_eid_structure(eid_variable_personal_data),
        )

    def _resize_ctypes_char_array(self, old_array, new_size):
        new_array_type = ctypes.c_char * new_size
        new_array = new_array_type()
        min_size = min(len(old_array), new_size)
        ctypes.memmove(new_array, old_array, min_size)
        return new_array

    def __resize_eid_structure(self, eid_structure):
        for field, _ in eid_structure._fields_:
            if isinstance(getattr(eid_structure, field), (bytes)):
                setattr(
                    eid_structure,
                    field,
                    bytes(
                        self._resize_ctypes_char_array(
                            getattr(eid_structure, field),
                            getattr(eid_structure, field + "Size"),
                        )
                    ),
                )
        return eid_structure


def ctypes_structure_to_dict(structure_instance):
    result = {}
    for field, _ in structure_instance._fields_:
        if isinstance(getattr(structure_instance, field), (bytes, bytearray)):
            result[field] = getattr(structure_instance, field).decode()
        else:
            result[field] = getattr(structure_instance, field)
    return result


def read_data():
    with Celik() as celik:
        with ID_card(celik) as id_card:
            eid_dd, eid_fpd, eid_vpd = id_card.extract_data_from_id_card()
            return {
                "documentData": ctypes_structure_to_dict(eid_dd),
                "fixedPersonalData": ctypes_structure_to_dict(eid_fpd),
                "variablePersonalData": ctypes_structure_to_dict(eid_vpd),
            }


def _start_http_server(port):
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class RequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            try:
                data = read_data()
                response_body = json.dumps(data).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(response_body)))
                self.end_headers()
                self.wfile.write(response_body)
            except Exception as e:
                error_message = f"Error: {e}".encode()
                self.send_response(500)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(error_message)))
                self.end_headers()
                self.wfile.write(error_message)

    server_address = ("", port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()


def main(args):
    if len(args) > 1 and args[1] == "http":
        _start_http_server(13765)
    else:
        try:
            data = read_data()
            print(json.dumps(data, indent=4, ensure_ascii=False))
            return 0
        except Exception as e:
            print(f"Error: {e}")
            return 1


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
