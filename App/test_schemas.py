
from schemas import validate_ai_response


def test_valid_response():
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

    assert tulos["success"] is True
    assert tulos["data"]["os_type"] == "Windows 11"
    assert len(tulos["data"]["steps"]) == 2


def test_invalid_response():
    virheellinen = (
        '{"problem": "", "os_type": "Windows 11", "steps": []}'
    )

    tulos = validate_ai_response(virheellinen)

    assert tulos["success"] is False
    assert tulos["data"] is None
    assert tulos["error"] is not None
