"""Assume an AWS role with a SAML assertion and write temporary credentials.

The script intentionally does not store a SAML assertion in source. Provide one with
--saml-assertion-file, AWS_SAML_ASSERTION, or paste it into the hidden prompt.
"""

import argparse
import base64
import configparser
import getpass
import os
from pathlib import Path
from typing import NamedTuple
from xml.etree import ElementTree

import boto3

DEFAULT_REGION = "us-east-1"
DEFAULT_PROFILE = "default"
DEFAULT_PRINCIPAL_NAME = "AzureAD"


class AccountRole(NamedTuple):
    label: str
    account_id: str
    role_name: str


class SamlRole(NamedTuple):
    role_arn: str
    principal_arn: str


ACCOUNT_ROLES: dict[str, AccountRole] = {
    "1": AccountRole(
        "paice-dev-nonprd",
        "863518450240",
        "assessments-genai_lead_developer_role",
    ),
    "2": AccountRole(
        "itec-pearsonauthoringframework-nonprd",
        "928847295959",
        "assessments-genai_developer_role",
    ),
    "3": AccountRole("contentmlresearch-sand", "164861018542", "PCMPowerUser"),
    "4": AccountRole(
        "itec-pearsonauthoringframework-prd",
        "288076569742",
        "assessments-genai_developer_role",
    ),
    "5": AccountRole("connexus-api-sand", "975049995604", "PVSSoftwareEngineers"),
    "6": AccountRole("connexus-apiint-nonprod", "533267312739", "PCMPowerUser"),
    "7": AccountRole("connectionseducation-prod", "098412817288", "PCMReadOnly"),
}


def _aws_dir() -> Path:
    return Path.home() / ".aws"


def _read_ini(path: Path) -> configparser.ConfigParser:
    parser = configparser.ConfigParser()
    if path.exists():
        parser.read(path, encoding="utf-8")
    return parser


def _write_ini(parser: configparser.ConfigParser, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        parser.write(handle)


def load_saml_assertion(args: argparse.Namespace) -> str:
    if args.saml_assertion_file:
        return Path(args.saml_assertion_file).read_text(encoding="utf-8").strip()

    value = os.getenv(args.saml_assertion_env)
    if value:
        return value.strip()

    return getpass.getpass("Paste SAML assertion: ").strip()


def parse_saml_roles(saml_assertion: str) -> list[SamlRole]:
    decoded = base64.b64decode(saml_assertion).decode("utf-8")
    root = ElementTree.fromstring(decoded)
    roles: list[SamlRole] = []
    for attribute in root.iter("{urn:oasis:names:tc:SAML:2.0:assertion}Attribute"):
        if (
            attribute.attrib.get("Name")
            != "https://aws.amazon.com/SAML/Attributes/Role"
        ):
            continue
        for value in attribute:
            parts = [part.strip() for part in (value.text or "").split(",")]
            if len(parts) != 2:
                continue
            role_arn = next((part for part in parts if ":role/" in part), None)
            principal_arn = next(
                (part for part in parts if ":saml-provider/" in part), None
            )
            if role_arn and principal_arn:
                roles.append(SamlRole(role_arn, principal_arn))
    return roles


def account_for_role(role: SamlRole) -> AccountRole | None:
    role_prefix = "arn:aws:iam::"
    role_account_id = role.role_arn.removeprefix(role_prefix).split(":", 1)[0]
    role_name = role.role_arn.rsplit("/", 1)[-1]
    for account in ACCOUNT_ROLES.values():
        if account.account_id == role_account_id and account.role_name == role_name:
            return account
    return None


def resolve_account_role(args: argparse.Namespace) -> AccountRole:
    if args.account_id and args.role_name:
        return AccountRole("custom", args.account_id, args.role_name)
    if args.account_choice:
        return ACCOUNT_ROLES[args.account_choice]

    print("Available accounts:")
    for key, account in ACCOUNT_ROLES.items():
        print(f"  {key}: {account.label} - {account.account_id} ({account.role_name})")
    choice = input("Select your account (1-7): ").strip()
    if choice not in ACCOUNT_ROLES:
        raise SystemExit(f"Unknown account choice: {choice}")
    return ACCOUNT_ROLES[choice]


def assume_role_with_saml(
    account: AccountRole,
    saml_assertion: str,
    *,
    principal_arn: str | None,
    duration_seconds: int,
    region: str,
) -> dict:
    role_arn = f"arn:aws:iam::{account.account_id}:role/{account.role_name}"
    principal = principal_arn or (
        f"arn:aws:iam::{account.account_id}:saml-provider/{DEFAULT_PRINCIPAL_NAME}"
    )
    sts_client = boto3.client("sts", region_name=region)
    response = sts_client.assume_role_with_saml(
        RoleArn=role_arn,
        PrincipalArn=principal,
        SAMLAssertion=saml_assertion,
        DurationSeconds=duration_seconds,
    )
    return response["Credentials"]


def validate_requested_role(
    account: AccountRole, principal_arn: str | None, saml_roles: list[SamlRole]
) -> str | None:
    requested_role_arn = f"arn:aws:iam::{account.account_id}:role/{account.role_name}"
    requested_principal_arn = principal_arn or (
        f"arn:aws:iam::{account.account_id}:saml-provider/{DEFAULT_PRINCIPAL_NAME}"
    )
    for role in saml_roles:
        if (
            role.role_arn == requested_role_arn
            and role.principal_arn == requested_principal_arn
        ):
            return None

    lines = [
        "The SAML assertion does not contain the requested AWS role/principal pair.",
        f"Requested: {requested_role_arn},{requested_principal_arn}",
        "Roles available in this assertion:",
    ]
    for role in saml_roles:
        account_match = account_for_role(role)
        hint = f" ({account_match.label})" if account_match else ""
        lines.append(f"  - {role.role_arn},{role.principal_arn}{hint}")
    return "\n".join(lines)


def write_aws_profile(profile: str, region: str, credentials: dict) -> None:
    aws_dir = _aws_dir()
    credentials_path = aws_dir / "credentials"
    config_path = aws_dir / "config"

    credentials_ini = _read_ini(credentials_path)
    if not credentials_ini.has_section(profile):
        credentials_ini.add_section(profile)
    credentials_ini[profile]["aws_access_key_id"] = credentials["AccessKeyId"]
    credentials_ini[profile]["aws_secret_access_key"] = credentials["SecretAccessKey"]
    credentials_ini[profile]["aws_session_token"] = credentials["SessionToken"]
    _write_ini(credentials_ini, credentials_path)

    config_ini = _read_ini(config_path)
    section = "default" if profile == "default" else f"profile {profile}"
    if not config_ini.has_section(section):
        config_ini.add_section(section)
    config_ini[section]["region"] = region
    _write_ini(config_ini, config_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Write AWS credentials for Bedrock by assuming a SAML-backed role.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--account-choice", choices=sorted(ACCOUNT_ROLES))
    parser.add_argument("--account-id", help="AWS account id for a custom account/role")
    parser.add_argument("--role-name", help="AWS role name for a custom account/role")
    parser.add_argument("--principal-arn", help="Custom SAML provider ARN")
    parser.add_argument(
        "--profile",
        default=DEFAULT_PROFILE,
        help="AWS profile to write credentials into",
    )
    parser.add_argument("--region", default=DEFAULT_REGION, help="AWS region to write")
    parser.add_argument(
        "--duration-seconds",
        type=int,
        default=28_800,
        help="Requested STS session duration",
    )
    parser.add_argument(
        "--saml-assertion-file", help="File containing a SAML assertion"
    )
    parser.add_argument(
        "--saml-assertion-env",
        default="AWS_SAML_ASSERTION",
        help="Environment variable containing a SAML assertion",
    )
    parser.add_argument(
        "--list-assertion-roles",
        action="store_true",
        help="Print AWS roles in the SAML assertion and exit without calling STS",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate the selected account/role against the assertion and exit without calling STS",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if bool(args.account_id) != bool(args.role_name):
        parser.error("--account-id and --role-name must be provided together")

    saml_assertion = load_saml_assertion(args)
    if not saml_assertion:
        raise SystemExit("No SAML assertion provided")

    try:
        saml_roles = parse_saml_roles(saml_assertion)
    except Exception as exc:
        raise SystemExit(f"Could not parse SAML assertion: {exc}") from exc
    if not saml_roles:
        raise SystemExit("No AWS role attributes found in SAML assertion")
    if args.list_assertion_roles:
        for role in saml_roles:
            account_match = account_for_role(role)
            hint = f" ({account_match.label})" if account_match else ""
            print(f"{role.role_arn},{role.principal_arn}{hint}")
        return

    account = resolve_account_role(args)
    validation_error = validate_requested_role(account, args.principal_arn, saml_roles)
    if validation_error:
        raise SystemExit(validation_error)
    if args.validate_only:
        print(
            f"SAML assertion contains {account.label} ({account.account_id}/{account.role_name})."
        )
        return

    credentials = assume_role_with_saml(
        account,
        saml_assertion,
        principal_arn=args.principal_arn,
        duration_seconds=args.duration_seconds,
        region=args.region,
    )
    write_aws_profile(args.profile, args.region, credentials)

    print(
        f"AWS profile '{args.profile}' configured for {account.label} ({account.role_name})."
    )
    print(f"Credentials expire at {credentials['Expiration']}.")
    if args.profile == "default":
        print("Default AWS profile updated; no AWS_PROFILE override is needed.")
        print(
            "If AWS_PROFILE is already set in this shell, remove it before running Bedrock:"
        )
        print("Remove-Item Env:AWS_PROFILE -ErrorAction SilentlyContinue")
    else:
        print("Use this PowerShell session setup before running Bedrock:")
        print(f'$env:AWS_PROFILE = "{args.profile}"')
    print(f'$env:AWS_REGION = "{args.region}"')


if __name__ == "__main__":
    main()
