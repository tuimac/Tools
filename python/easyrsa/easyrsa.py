#!/usr/bin/env python3

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import datetime
import os
import sys

# Static Variables for configuration
## Directory to dump the cert or key file
FILE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

## Expiration(Days)
EXPIRE = 3650

## Key size
KEY_SIZE = 4096

## Common Name
COMMON_NAME = 'tuimac.com'

def create_ca_cert():
    ca_key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = KEY_SIZE,
        backend = default_backend()
    )
    ca_name = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u'JP'),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Tokyo'),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u'Chiyoda-ku'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'My CA'),
        x509.NameAttribute(NameOID.COMMON_NAME, COMMON_NAME),
    ])
    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(ca_name)
        .issuer_name(ca_name)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days = EXPIRE))
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=None),
            critical=True,
        )
        .sign(ca_key, hashes.SHA256(), default_backend())
    )
    with open(os.path.join(FILE_DIR, 'ca.crt'), 'wb') as f:
        f.write(
            ca_cert.public_bytes(encoding=serialization.Encoding.PEM)
        )
    return ca_cert, ca_key

def create_server_key():
    server_key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = KEY_SIZE,
        backend = default_backend()
    )
    with open(os.path.join(FILE_DIR, 'server.key'), 'wb') as f:
        f.write(
            server_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
    return server_key

def create_server_cert(ca_cert, ca_key, server_key):
    server_name = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u'JP'),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Tokyo'),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u'Chiyoda-ku'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'My Organization'),
        x509.NameAttribute(NameOID.COMMON_NAME, COMMON_NAME),
    ])
    server_cert = (
        x509.CertificateBuilder()
        .subject_name(server_name)
        .issuer_name(ca_cert.subject)
        .public_key(server_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days = EXPIRE))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName(COMMON_NAME)]),
            critical=False,
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_encipherment=True,
                key_agreement=False,
                content_commitment=False,
                data_encipherment=False,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True
        )
        .sign(ca_key, hashes.SHA256(), default_backend())
    )
    with open(os.path.join(FILE_DIR, 'server.crt'), 'wb') as f:
        f.write(
            server_cert.public_bytes(encoding=serialization.Encoding.PEM)
        )

if __name__ == '__main__':
    ca_cert, ca_key = create_ca_cert()
    server_key = create_server_key()
    create_server_cert(ca_cert, ca_key, server_key)