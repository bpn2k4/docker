import datetime
from re import match as re_match
from xmlrpc.client import Boolean
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.x509.base import Certificate
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.x509.oid import NameOID

root_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=3072,
    backend=default_backend()
)

subject = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u"Self TLS"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Self TLS. Inc")
])
issuer = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u"Unknown"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Unknown")
])
root_certificate = x509 \
    .CertificateBuilder() \
    .subject_name(subject) \
    .issuer_name(issuer) \
    .public_key(root_private_key.public_key()) \
    .serial_number(x509.random_serial_number()) \
    .not_valid_before(datetime.datetime.now()) \
    .not_valid_after(datetime.datetime.now() + datetime.timedelta(days=3650)) \
    .sign(root_private_key, SHA256(), default_backend())

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=3072,
    backend=default_backend()
)

csr = x509.CertificateSigningRequestBuilder() \
    .subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u"*")
    ])) \
    .sign(private_key, SHA256(), default_backend())
certificate = x509.CertificateBuilder() \
    .subject_name(csr.subject) \
    .issuer_name(root_certificate.issuer) \
    .public_key(csr.public_key()).serial_number(x509.random_serial_number()) \
    .not_valid_before(datetime.datetime.now()) \
    .not_valid_after(datetime.datetime.now() + datetime.timedelta(days=3650)) \
    .add_extension(x509.SubjectAlternativeName([x509.DNSName(u"*")]), critical=False) \
    .sign(root_private_key, SHA256(), default_backend())

print("ROOT_PRIVATE_KEY")
print(
    root_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
)
with open('rootCA.key', "wb") as file:
  file.write(root_private_key.private_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PrivateFormat.PKCS8,
      encryption_algorithm=serialization.NoEncryption()
  ))


print("ROOT_CERTIFICATE")
print(
    root_certificate.public_bytes(
        serialization.Encoding.PEM
    ).decode('utf-8')
)
with open("rootCA.crt", "wb") as file:
  file.write(certificate.public_bytes(serialization.Encoding.PEM))


print("PRIVATE_KEY_HOST")
print(
    private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
)

with open('host.key', "wb") as file:
  file.write(private_key.private_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PrivateFormat.PKCS8,
      encryption_algorithm=serialization.NoEncryption()
  ))


print("CERTIFICATE_HOST")
print(
    certificate.public_bytes(
        serialization.Encoding.PEM
    ).decode('utf-8')
)

with open("host.crt", "wb") as file:
  file.write(certificate.public_bytes(serialization.Encoding.PEM))
