from ctypes import Array, byref, c_char, memset, sizeof
from ctypes import c_int, c_void_p, POINTER
from ctypes.wintypes import *
from enum import Enum
import ctypes
import sys

from PIL import Image
from io import BytesIO
import requests

BI_RGB = 0
DIB_RGB_COLORS = 0 

'''
    GOT EXE EXTRACTOR CODE FROM
    https://pythonassets.com/posts/extract-icon-from-executable-file-windows/
'''

class ICONINFO(ctypes.Structure):
    _fields_ = [
        ("fIcon", BOOL),
        ("xHotspot", DWORD),
        ("yHotspot", DWORD),
        ("hbmMask", HBITMAP),
        ("hbmColor", HBITMAP)
    ]

class RGBQUAD(ctypes.Structure):
    _fields_ = [
        ("rgbBlue", BYTE),
        ("rgbGreen", BYTE),
        ("rgbRed", BYTE),
        ("rgbReserved", BYTE),
    ]

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", DWORD),
        ("biWidth", LONG),
        ("biHeight", LONG),
        ("biPlanes", WORD),
        ("biBitCount", WORD),
        ("biCompression", DWORD),
        ("biSizeImage", DWORD),
        ("biXPelsPerMeter", LONG),
        ("biYPelsPerMeter", LONG),
        ("biClrUsed", DWORD),
        ("biClrImportant", DWORD)
    ]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", RGBQUAD * 1),
    ]


shell32 = ctypes.WinDLL("shell32", use_last_error=True)
user32 = ctypes.WinDLL("user32", use_last_error=True)
gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)

gdi32.CreateCompatibleDC.argtypes = [HDC]
gdi32.CreateCompatibleDC.restype = HDC
gdi32.GetDIBits.argtypes = [
    HDC, HBITMAP, UINT, UINT, LPVOID, c_void_p, UINT
]
gdi32.GetDIBits.restype = c_int
gdi32.DeleteObject.argtypes = [HGDIOBJ]
gdi32.DeleteObject.restype = BOOL
shell32.ExtractIconExW.argtypes = [
    LPCWSTR, c_int, POINTER(HICON), POINTER(HICON), UINT
]
shell32.ExtractIconExW.restype = UINT
user32.GetIconInfo.argtypes = [HICON, POINTER(ICONINFO)]
user32.GetIconInfo.restype = BOOL
user32.DestroyIcon.argtypes = [HICON]
user32.DestroyIcon.restype = BOOL


class IconSize(Enum):
    SMALL = 1
    LARGE = 2

    @staticmethod
    def to_wh(size: "IconSize") -> tuple[int, int]:
        """
        Return the actual (width, height) values for the specified icon size.
        """
        size_table = {
            IconSize.SMALL: (16, 16),
            IconSize.LARGE: (32, 32)
        }
        return size_table[size]

def rgba_to_img(bits):
    icon_size = IconSize.LARGE
    w, h = IconSize.to_wh(icon_size)

    # Create a new image with RGBA mode
    image = Image.new("RGBA", (w, h))

    # Set pixels for the image
    for row in range(h):
        for col in range(w):
            index = row * w * 4 + col * 4
            b, g, r, a = bits[index:index + 4]
            # PIL expects the color in RGBA format
            color = (r, g, b, a)
            image.putpixel((col, row), color)

    return image

def extract_exe_icon(filename: str, size: IconSize) -> Array[c_char]:
    """
    Extract the icon from the specified `filename`, which might be
    either an executable or an `.ico` file.
    """
    dc: HDC = gdi32.CreateCompatibleDC(0)
    if dc == 0:
        raise ctypes.WinError()

    hicon: HICON = HICON()
    extracted_icons: UINT = shell32.ExtractIconExW(
        filename,
        0,
        byref(hicon) if size == IconSize.LARGE else None,
        byref(hicon) if size == IconSize.SMALL else None,
        1
    )
    if extracted_icons != 1:
        raise ctypes.WinError()

    def cleanup() -> None:
        if icon_info.hbmColor != 0:
            gdi32.DeleteObject(icon_info.hbmColor)
        if icon_info.hbmMask != 0:
            gdi32.DeleteObject(icon_info.hbmMask)
        user32.DestroyIcon(hicon)

    icon_info: ICONINFO = ICONINFO(0, 0, 0, 0, 0)
    if not user32.GetIconInfo(hicon, byref(icon_info)):
        cleanup()
        raise ctypes.WinError()

    w, h = IconSize.to_wh(size)
    bmi: BITMAPINFO = BITMAPINFO()
    memset(byref(bmi), 0, sizeof(bmi))
    bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = w
    bmi.bmiHeader.biHeight = -h
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biCompression = BI_RGB
    bmi.bmiHeader.biSizeImage = w * h * 4
    bits = ctypes.create_string_buffer(bmi.bmiHeader.biSizeImage)
    copied_lines = gdi32.GetDIBits(
        dc, icon_info.hbmColor, 0, h, bits, byref(bmi), DIB_RGB_COLORS
    )
    if copied_lines == 0:
        cleanup()
        raise ctypes.WinError()

    cleanup()

    return rgba_to_img(bits)


def requestIcon(url):
    # free google API
    url = f"https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url={url}&size=64"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    img.load() # required for img.split()

    # Check if the image has an alpha channel
    if img.mode == 'RGBA':
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3]) # 3 is the alpha channel
    else:
        background = img

    return background


def get_icon(path, link):
    if link:
        if path[:4] == 'www.':
            path = 'https://' + path

        elif path[:8] != 'https://':
            path = 'https://' + path

        img = requestIcon(path)
    elif path[-4:] == ".exe":
        img = extract_exe_icon(path, IconSize.LARGE)
    else:
        print("Invalid path.")
        raise Exception("Invalid Path.")
    return img
