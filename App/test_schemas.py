from schemas import validate_ai_response

vastaus = """
{
    "problem": "Tietokone ei käynnisty",
    "os_type": "Windows 11",
    "steps": [
        "Tarkista virtajohto",
        "Käynnistä tietokone uudelleen"
    ]
}
"""

tulos = validate_ai_response(vastaus)
print(tulos)
print("\nTestataan virheellistä vastausta:")

virheellinen = '{"problem": "", "os_type": "Windows 11", "steps": []}'

print(validate_ai_response(virheellinen))