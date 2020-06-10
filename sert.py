import contextlib
import OpenSSL.crypto
import os
import config

""" Использование:
with pfx_to_pem('foo.pem', 'bar') as cert:
requests.post(url, cert=cert, data=payload)
"""


@contextlib.contextmanager
def pfx_to_pem(pfx_path, pfx_password):
    if os.path.isfile(config.get_setting('Paths', 'PEM_certificate')):
        with open(config.get_setting('Paths', 'PEM_certificate')) as t_pem:
            f_pem = open(t_pem.name, 'wb')
            pfx = open(pfx_path, 'rb').read()
            p12 = OpenSSL.crypto.load_pkcs12(pfx, pfx_password)
            f_pem.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey()))
            f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, p12.get_certificate()))
            ca = p12.get_ca_certificates()
            if ca is not None:
                cs = 1
                for cert in ca:
                    f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
                    cs += 1
                cs = 1
            f_pem.close()
            yield t_pem.name
    else:
        f = open(config.get_setting('Paths', 'PEM_certificate'), 'tw', encoding='utf-8')
        f.close()
        print("Файл сертификата был создан. Необходимо перезапустить программу")
        exitt = input()
        raise SystemExit(1)


if __name__ == '__main__':
    pfx_to_pem("cert.pfx", "123456")
    print('its ok')
