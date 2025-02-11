# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import pkg_resources as pkgr

import tlscanary.cert as cert


def test_cert_instance_with_pem():
    """Cert instances can process PEM and DER certificates"""

    # Create an instance from PEM data
    pem_cert_file = pkgr.resource_filename(__name__, "files/mozilla.org.pem")
    assert os.path.isfile(pem_cert_file)
    with open(pem_cert_file, "rb") as f:
        # Test from bytes object
        pem = cert.Cert(f.read())
    assert type(pem) is cert.Cert, "can open PEM content"

    # Create an instance from DER data
    der_cert_file = pkgr.resource_filename(__name__, "files/mozilla.org.der")
    assert os.path.isfile(der_cert_file)
    with open(pem_cert_file, "rb") as f:
        # Test from list of int
        der_data = list(f.read())
        der = cert.Cert(der_data)
    assert type(der) is cert.Cert, "can open DER content"

    assert pem.as_pem() == der.as_pem(), "PEM conversions are identical"
    assert pem.as_der() == der.as_der(), "DER conversions are identical"

    # Now assuming that all instances have identical content
    assert der.signature_hash_algorithm() == "sha256", "SIGNATURE_HASH_ALGORITHM extracts fine"
    assert der.subject_alt_name() == "mozilla.org,www.mozilla.org", "SUBJECT_ALTERNATIVE_NAME OID extracts fine"
    assert der.ext_key_usage() == "serverAuth,clientAuth", "EXTENDED_KEY_USAGE OID extracts fine"
