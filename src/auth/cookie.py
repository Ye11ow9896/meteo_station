import http.cookies
from datetime import datetime
from email.utils import format_datetime
from typing import Optional, Union, Literal


class Cookie:
    def set_cookie(
            self,
            key: str,
            value: str = "",
            max_age: Optional[int] = None,
            expires: Optional[Union[datetime, str, int]] = None,
            path: str = "/",
            domain: Optional[str] = None,
            secure: bool = False,
            httponly: bool = False,
            samesite: Optional[Literal["lax", "strict", "none"]] = "lax",
    ) -> None:
        """"""
        cookie = http.cookies.SimpleCookie()
        cookie[key] = value
        if max_age is not None:
            cookie[key]["max-age"] = max_age
        if expires is not None:
            if isinstance(expires, datetime):
                cookie[key]["expires"] = format_datetime(expires, usegmt=True)
            else:
                cookie[key]["expires"] = expires
        if path is not None:
            cookie[key]["path"] = path
        if domain is not None:
            cookie[key]["domain"] = domain
        if secure:
            cookie[key]["secure"] = True
        if httponly:
            cookie[key]["httponly"] = True
        if samesite is not None:
            assert samesite.lower() in [
                "strict",
                "lax",
                "none",
            ], "samesite must be either 'strict', 'lax' or 'none'"
            cookie[key]["samesite"] = samesite
        cookie_val = cookie.output(header="").strip()
        self.raw_headers.append((b"set-cookie", cookie_val.encode("latin-1")))
