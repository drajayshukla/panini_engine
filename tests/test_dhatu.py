import pytest
from logic.dhatu_processor import DhatuDiagnostic

@pytest.mark.parametrize("upadesha, expected_action, expected_tags", [
    ("डुकृञ्", "कृ", {"डु-It (1.3.5)", "ञ्-It (1.3.3)"}),
    ("णीञ्", "नी", {"ञ्-It (1.3.3)"}),
    ("नदिँ", "नन्द्", {"इँ-It (1.3.2)"}),
    ("विदिँ", "विन्द्", {"इँ-It (1.3.2)"}),
    ("मुचिँ", "मुन्च्", {"इँ-It (1.3.2)"}), 
    ("ष्मि", "स्मि", set()), 
    # Nad: 'a~' is removed, so it becomes Halanta 'nad'
    ("णदँ", "नद्", {"अँ-It (1.3.2)"}),
    ("णिदिँ", "निन्द्", {"ञि-It (1.3.5)", "इँ-It (1.3.2)"}),
    # Bhid: 'ir' removal prevents Num
    ("भिदिँर्", "भिद्", {"ir-It (Vartika)"}) 
])
def test_dhatu_diagnostic_flow(upadesha, expected_action, expected_tags):
    diag = DhatuDiagnostic(upadesha)
    final_root = diag.get_final_root()
    assert final_root == expected_action

    if expected_tags:
        found = any(any(tag.split()[0] in t for t in diag.it_tags) for tag in expected_tags)
        assert found, f"Missing tags for {upadesha}. Got: {diag.it_tags}"

def test_initial_exception_bali_yah():
    diag = DhatuDiagnostic("ष्ठिवुँ")
    assert diag.get_final_root() == "ष्ठिव्"
