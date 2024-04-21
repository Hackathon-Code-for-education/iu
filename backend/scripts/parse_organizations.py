import time

from beanie import PydanticObjectId
from pydantic import BaseModel, Field
from typing import List, Optional
import xml.etree.ElementTree as ET


# Individual entrepreneur details
# class IndividualEntrepreneur(BaseModel):
#     last_name: Optional[str] = Field(None, validation_alias="IndividualEntrepreneurLastName")
#     first_name: Optional[str] = Field(None, validation_alias="IndividualEntrepreneurFirstName")
#     middle_name: Optional[str] = Field(None, validation_alias="IndividualEntrepreneurMiddleName")
#     address: Optional[str] = Field(None, validation_alias="IndividualEntrepreneurAddress")
#     egr_ip: Optional[str] = Field(None, validation_alias="IndividualEntrepreneurEGRIP")
#     inn: Optional[str] = Field(None, validation_alias="IndividualEntrepreneurINN")
#
#     @classmethod
#     def from_xml(cls, xml: ET.Element) -> Optional["IndividualEntrepreneur"]:
#         data = {}
#         for key, field in cls.model_fields.items():
#             xml_field = xml.find(field.validation_alias or key)
#             if xml_field is not None:
#                 data[field.validation_alias or key] = xml_field.text
#         if not data:
#             return None
#         return cls.model_validate(data)


# Actual education organization details
class ActualEducationOrganization(BaseModel):
    in_registry_id: str | None = Field(..., validation_alias="Id")
    full_name: str | None = Field(..., validation_alias="FullName")
    short_name: str | None = Field(..., validation_alias="ShortName")
    head_edu_org_id: str | None = Field(..., validation_alias="HeadEduOrgId")
    is_branch: bool | None = Field(..., validation_alias="IsBranch")
    post_address: str | None = Field(..., validation_alias="PostAddress")
    phone: str | None = Field(..., validation_alias="Phone")
    fax: Optional[str] | None = Field(None, validation_alias="Fax")
    email: str | None = Field(..., validation_alias="Email")
    website: str | None = Field(..., validation_alias="WebSite")
    ogrn: str | None = Field(..., validation_alias="OGRN")
    inn: str | None = Field(..., validation_alias="INN")
    kpp: str | None = Field(..., validation_alias="KPP")
    head_post: str | None = Field(..., validation_alias="HeadPost")
    head_name: str | None = Field(..., validation_alias="HeadName")
    form_name: str | None = Field(..., validation_alias="FormName")
    kind_name: str | None = Field(..., validation_alias="KindName")
    type_name: str | None = Field(..., validation_alias="TypeName")
    region_name: str | None = Field(..., validation_alias="RegionName")
    federal_district_short_name: str | None = Field(..., validation_alias="FederalDistrictShortName")
    federal_district_name: str | None = Field(..., validation_alias="FederalDistrictName")

    @classmethod
    def from_xml(cls, xml: ET.Element) -> Optional["ActualEducationOrganization"]:
        data = {}
        for key, field in cls.model_fields.items():
            xml_field = xml.find(field.validation_alias or key)
            if xml_field is not None:
                data[field.validation_alias or key] = xml_field.text
        if not data:
            return None
        return cls.model_validate(data)


class ActualEducationOrganizationOut(BaseModel):
    in_registry_id: str | None
    full_name: str | None
    short_name: str | None
    head_edu_org_id: str | None
    is_branch: bool | None
    post_address: str | None
    phone: str | None
    fax: Optional[str] | None
    email: str | None
    website: str | None
    ogrn: str | None
    inn: str | None
    kpp: str | None
    head_post: str | None
    head_name: str | None
    form_name: str | None
    kind_name: str | None
    type_name: str | None
    region_name: str | None
    federal_district_short_name: str | None
    federal_district_name: str | None


class EducationalProgram(BaseModel):
    in_registry_id: str = Field(..., validation_alias="Id")
    # type_name: str | None = Field(..., validation_alias="TypeName")
    edu_level_name: str | None = Field(..., validation_alias="EduLevelName")
    program_name: str | None = Field(..., validation_alias="ProgrammName")
    program_code: str | None = Field(..., validation_alias="ProgrammCode")
    ugs_name: str | None = Field(..., validation_alias="UGSName")
    ugs_code: str | None = Field(..., validation_alias="UGSCode")
    edu_normative_period: str | None = Field(..., validation_alias="EduNormativePeriod")
    qualification: str | None = Field(..., validation_alias="Qualification")

    # is_accredited: bool | None = Field(..., validation_alias="IsAccredited")
    # is_canceled: bool | None = Field(..., validation_alias="IsCanceled")
    # is_suspended: bool | None = Field(..., validation_alias="IsSuspended")

    @classmethod
    def from_xml(cls, xml: ET.Element) -> Optional["EducationalProgram"]:
        data = {}
        for key, field in cls.model_fields.items():
            xml_field = xml.find(field.validation_alias or key)
            if xml_field is not None:
                data[field.validation_alias or key] = xml_field.text
        if not data:
            return None
        return cls.model_validate(data)


class EducationalProgramOut(BaseModel):
    in_registry_id: str
    edu_level_name: str | None
    program_name: str | None
    program_code: str | None
    ugs_name: str | None
    ugs_code: str | None
    edu_normative_period: str | None
    qualification: str | None


class Certificate(BaseModel):
    in_registry_id: str = Field(..., validation_alias="Id")
    is_federal: bool | None = Field(..., validation_alias="IsFederal")
    status_name: str | None = Field(..., validation_alias="StatusName")
    type_name: str | None = Field(..., validation_alias="TypeName")
    region_name: str | None = Field(..., validation_alias="RegionName")
    # region_code: str | None = Field(..., validation_alias="RegionCode")
    federal_district_name: str | None = Field(..., validation_alias="FederalDistrictName")
    # federal_district_short_name: str | None = Field(..., validation_alias="FederalDistrictShortName")
    # reg_number: str | None = Field(..., validation_alias="RegNumber")
    # serial_number: str | None = Field(..., validation_alias="SerialNumber")
    # form_number: str | None = Field(..., validation_alias="FormNumber")
    # issue_date: str | None = Field(..., validation_alias="IssueDate")
    # end_date: str | None = Field(..., validation_alias="EndDate")
    # control_organ: str | None = Field(..., validation_alias="ControlOrgan")
    # post_address: str | None = Field(..., validation_alias="PostAddress")
    # edu_org_full_name: str | None = Field(..., validation_alias="EduOrgFullName")
    # edu_org_short_name: str | None = Field(..., validation_alias="EduOrgShortName")
    # edu_org_inn: str | None = Field(..., validation_alias="EduOrgINN")
    # edu_org_kpp: str | None = Field(..., validation_alias="EduOrgKPP")
    # edu_org_ogrn: str | None = Field(..., validation_alias="EduOrgOGRN")
    # individual_entrepreneur: IndividualEntrepreneur | None
    actual_education_organization: ActualEducationOrganization | None
    educational_programs: List[EducationalProgram] = []

    @classmethod
    def from_xml(cls, xml: ET.Element) -> Optional["Certificate"]:
        data = {}
        for key, field in cls.model_fields.items():
            if key in ("educational_programs", "individual_entrepreneur", "actual_education_organization"):
                continue

            xml_field = xml.find(field.validation_alias or key)
            if xml_field is not None:
                data[field.validation_alias or key] = xml_field.text

        # individual_entrepreneur = xml.find("IndividualEntrepreneur")
        # if individual_entrepreneur is not None:
        #     data["individual_entrepreneur"] = IndividualEntrepreneur.from_xml(individual_entrepreneur)

        actual_education_organization = xml.find("ActualEducationOrganization")
        if actual_education_organization is not None:
            data["actual_education_organization"] = ActualEducationOrganization.from_xml(actual_education_organization)

        educational_programs = []
        for educational_program in xml.findall(".//EducationalProgram"):
            program = EducationalProgram.from_xml(educational_program)
            educational_programs.append(program)

        data["educational_programs"] = educational_programs

        if not data:
            return None
        return cls.model_validate(data)


class CertificateOut(BaseModel):
    in_registry_id: str
    logo: PydanticObjectId | None = None
    is_federal: bool | None
    status_name: str | None
    type_name: str | None
    region_name: str | None
    federal_district_name: str | None
    actual_education_organization: ActualEducationOrganizationOut | None
    educational_programs: List[EducationalProgramOut] = []


# Wrapper for the complete data
class Certificates(BaseModel):
    certificates: List[CertificateOut]


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Parse organizations")
    parser.add_argument(
        "--input",
        type=argparse.FileType("r"),
        help="Input file from https://obrnadzor.gov.ru/otkrytoe-pravitelstvo/opendata/7701537808-raoo/",
        default="data.xml",
    )
    parser.add_argument("--output", type=argparse.FileType("w"), help="Output file", default="data.json")
    _start = time.perf_counter()
    args = parser.parse_args()

    certificates = []
    for event, elem in ET.iterparse(args.input):
        if elem.tag == "Certificate":
            certificate = Certificate.from_xml(elem)
            # игнорировать организацию если нет программ высшего образования
            if (
                not certificate.actual_education_organization
                or certificate.actual_education_organization.type_name
                != "Образовательная организация высшего образования"
                or certificate.status_name == "Недействующее"
                or certificate.actual_education_organization.region_name
                == "образовательные учреждения, находящиеся за пределами Российской Федерации"
            ):
                elem.clear()
                continue

            certificates.append(CertificateOut.model_validate(certificate, from_attributes=True))
            elem.clear()

    args.output.write(Certificates(certificates=certificates).model_dump_json(indent=2))


if __name__ == "__main__":
    main()
