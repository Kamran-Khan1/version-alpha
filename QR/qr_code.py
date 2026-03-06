import segno

slts_qrcode = segno.make_qr("https://docs.google.com/forms/d/e/1FAIpQLSfC-LTrG_dnNol1XaBRj-0S_d-OjyG0gby5X4cza-NePDRcsQ/viewform?usp=publish-editor")

slts_qrcode.save(
    "user-response.png",
    scale=5,
    light="lightblue",
)

